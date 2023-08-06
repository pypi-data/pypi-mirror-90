from typing import Union, List, Dict
from soco_encoders.model_loaders import EncoderLoader
from soco_encoders.models.module_bases import BaseEncoder
from collections import OrderedDict
from soco_encoders.http.config import EnvVars
import pickle as pkl

class MyModel(object):
    def __init__(self):
        self.models = OrderedDict()

    def load_model(self, model_id):
        if len(self.models) > EnvVars.MAX_NUM_MODEL:
            self.models.popitem(last=False)

        if model_id not in self.models:
            m = EncoderLoader.load_model('pretrain-models', model_id, EnvVars.USE_GPU, EnvVars.REGION)
            self.models[model_id] = m

        return self.models[model_id]

    def predict(self, model_id: str, text: Union[List[str], str], batch_size: int=10,
                mode: str = BaseEncoder.DEFAULT, kwargs: Dict = None):
        if type(text) is str:
            text = [text]

        if not kwargs:
            kwargs = None

        if mode == BaseEncoder.TSCORE and kwargs is None:
            kwargs = {'start_symbol': '<a>', 'end_symbol': '</a>', 'return_meta': True,
                      'min_threshold': 1e-2,
                      'top_k': 500,
                      'to_sparse': 'csr',
                      'term_batch_size': 3000,
                      'force_seq_len': -1,
                      'approx_padding': False,
                      'mask_padding': True
                      }

        m = self.load_model(model_id)
        f = m.encode(text, show_progress_bar=True, batch_size=batch_size, mode=mode, args=kwargs)
        if type(f) is tuple:
            f, meta = f
            for row_id in range(f.shape[0]):
                coo_row = f[row_id].tocoo()
                terms = []
                for col_id, v in zip(coo_row.col, coo_row.data):
                    terms.append({'score': float(v), 'term': meta['vocab'][col_id]})
                terms = sorted(terms, key=lambda x: x['score'] * -1)
                return terms
        else:
            f = f.tolist()
            return f


if __name__ == '__main__':

    x1 = '<a>刘强东是一个著名企业家。</a> 他创建了京东。'
    print(MyModel().predict('bert-base-zh-distill', x1, 'tscore', None))
    print(MyModel().predict('bert-base-zh-mean-tokens', x1))
