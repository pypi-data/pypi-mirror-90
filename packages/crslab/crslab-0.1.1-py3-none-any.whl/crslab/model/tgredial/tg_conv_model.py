# @Time   : 2020/12/9
# @Author : Yuanhang Zhou
# @Email  : sdzyh002@gmail.com

# UPDATE:
# @Time   : 2021/1/2, 2020/12/15, 2021/1/4
# @Author : Xiaolei Wang, Yuanhang Zhou, Yuanhang Zhou
# @Email  : wxl1999@foxmail.com, sdzyh002@gmail, sdzyh002@gmail.com

import os

import torch
from torch.nn import CrossEntropyLoss
from transformers import GPT2LMHeadModel

from crslab.model.base_model import BaseModel
from .resource import resources
from ...config import MODEL_PATH
from ...data import dataset_language_map


class TGConvModel(BaseModel):
    """This model was proposed in Towards topic-guided conversational recommender system
        
    Attributes:
        context_truncate: A integer indicating the length of dialogue context
        response_truncate: A integer indicating the length of dialogue response
        pad_id: A integer indicating the id of padding token
    """
    def __init__(self, opt, device, vocab, side_data):
        """

        Args:
            opt (dict): A dictionary record the hyper parameters
            device (torch.device): A variable indicating which device to place the data and model
            vocab (dict): A dictionary record the vocabulary information
            side_data (dict): A dictionary record the side data
        """
        self.context_truncate = opt['context_truncate']
        self.response_truncate = opt['response_truncate']
        self.pad_id = vocab['pad']

        language = dataset_language_map[opt['dataset']]
        dpath = os.path.join(MODEL_PATH, "tgredial", language)
        resource = resources[language]
        super(TGConvModel, self).__init__(opt, device, dpath, resource)

    def build_model(self):
        """build model"""
        self.model = GPT2LMHeadModel.from_pretrained(os.path.join(self.dpath, 'gpt2'))
        self.loss = CrossEntropyLoss(ignore_index=self.pad_id)

    def converse(self, batch, mode):
        if mode == 'test' or mode == 'infer':
            enhanced_context = batch[1]
            return self.generate(enhanced_context)
        else:
            enhanced_input_ids = batch[0]
            # torch.tensor's shape = (bs, seq_len, v_s); tuple's length = 12
            lm_logits = self.model(enhanced_input_ids).logits

            # index from 1 to self.reponse_truncate is valid response
            loss = self.calculate_loss(
                lm_logits[:, -self.response_truncate:-1, :],
                enhanced_input_ids[:, -self.response_truncate + 1:])

            pred = torch.max(lm_logits, dim=2)[1]  # [bs, seq_len]
            pred = pred[:, -self.response_truncate:]

            return loss, pred

    def generate(self, context):
        """
        Args:
            context: torch.tensor, shape=(bs, context_turncate)

        Returns:
            generated_response: torch.tensor, shape=(bs, reponse_turncate-1)
        """
        generated_response = []
        former_hidden_state = None
        context = context[..., -self.response_truncate + 1:]

        for i in range(self.response_truncate - 1):
            outputs = self.model(context, former_hidden_state)  # (bs, c_t, v_s),
            last_hidden_state, former_hidden_state = outputs.logits, outputs.past_key_values

            next_token_logits = last_hidden_state[:, -1, :]  # (bs, v_s)
            preds = next_token_logits.argmax(dim=-1).long()  # (bs)

            context = preds.unsqueeze(1)
            generated_response.append(preds)

        generated_response = torch.stack(generated_response).T

        return generated_response

    def calculate_loss(self, logit, labels):
        """
        Args:
            preds: torch.FloatTensor, shape=(bs, response_truncate, vocab_size)
            labels: torch.LongTensor, shape=(bs, response_truncate)

        """

        loss = self.loss(logit.reshape(-1, logit.size(-1)), labels.reshape(-1))
        return loss
