# @Time   : 2020/11/22
# @Author : Kun Zhou
# @Email  : francis_kun_zhou@163.com

# UPDATE:
# @Time   : 2020/11/24, 2020/12/24
# @Author : Kun Zhou, Xiaolei Wang
# @Email  : francis_kun_zhou@163.com, wxl1999@foxmail.com

from loguru import logger

from .conversation import *
from .kbrd import *
from .kgsf import *
from .policy import *
from .recommendation import *
from .redial import *
from .tgredial import *

Model_register_table = {
    'KGSF': KGSFModel,
    'KBRD': KBRDModel,
    'TGRec': TGRecModel,
    'TGConv': TGConvModel,
    'TGPolicy': TGPolicyModel,
    'ReDialRec': ReDialRecModel,
    'ReDialConv': ReDialConvModel,
    'GPT2': GPT2Model,
    'Transformer': TransformerModel,
    'ConvBERT': ConvBERTModel,
    'ProfileBERT': ProfileBERTModel,
    'TopicBERT': TopicBERTModel,
    'PMI': PMIModel,
    'MGCG': MGCGModel,
    'BERT': BERTModel,
    'SASREC': SASRECModel,
    'GRU4REC': GRU4RECModel,
    'Popularity': PopularityModel,
    'TextCNN': TextCNNModel
}


def get_model(config, model_name, device, vocab, side_data=None):
    if model_name in Model_register_table:
        model = Model_register_table[model_name](config, device, vocab, side_data)
        logger.info(f'[Build model {model_name}]')
        return model
    else:
        raise NotImplementedError('Model [{}] has not been implemented'.format(model_name))
