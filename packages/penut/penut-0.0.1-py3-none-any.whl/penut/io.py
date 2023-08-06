import os
import json

def dump_json(obj, fpath, encoding='UTF-8', is_ascii=False, indent=4):
    with open(fpath, 'w', encoding=encoding) as f:
        json.dump(obj, f, ensure_ascii=is_ascii, indent=indent)

def load_json(fpath, encoding='UTF-8'):
    with open(fpath, 'r', encoding=encoding) as f:
        return json.load(f)

def dump_pkl(obj, fpath):
    import pickle as pk
    with open(fpath, 'wb') as f:
        pk.dump(obj, f)

def load_pkl(fpath):
    import pickle as pk
    with open(fpath, 'rb') as f:
        return pk.load(f)

def dump_npy(obj, fpath):
    import numpy as np
    np.save(fpath, obj)

def load_npy(fpath):
    import numpy as np
    return np.load(fpath)

def dump_csv(obj, fpath, header=False, index=False):
    pd = load_pandas()
    pd.DataFrame(obj).to_csv(fpath, header=header, index=index)

def load_csv(fpath, header=None):
    pd = load_pandas()
    return pd.read_csv(fpath, header=header)

def load_pandas():
    try:
        import pandas as pd
        return pd
    except ModuleNotFoundError:
        raise RuntimeError('Pandas is not installed!')

def load(fpath, **kwargs):
    load_dict = {
        '.json': load_json,
        '.pkl': load_pkl,
        '.npy': load_npy,
        '.csv': load_csv
    }
    _, ext = os.path.splitext(fpath)
    return load_dict[ext](fpath, **kwargs)

def dump(obj, fpath, **kwargs):
    dump_dict = {
        '.json': dump_json,
        '.pkl': dump_pkl,
        '.npy': dump_npy,
        '.csv': dump_csv
    }
    _, ext = os.path.splitext(fpath)
    return dump_dict[ext](obj, fpath, **kwargs)

def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)
