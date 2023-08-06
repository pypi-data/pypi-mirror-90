import os
import datetime as dt

def walk_dir(target_dir, return_file_name=False, return_dir_name=False):
    for dir_path, _, file_list in os.walk(target_dir):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            rtn = [full_path]
            if return_file_name:
                rtn.append(file_name)
            if return_dir_name:
                rtn.append(dir_path)
            yield rtn[0] if len(rtn) == 1 else rtn

def timedelta2string(delta, fmt=None):
    if fmt is None:
        fmt = lambda h, m, s: f'{h:02d}:{m:02d}:{s:02d}'
    total_seconds = delta.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 24)
    hours, minutes, seconds = map(int, (hours, minutes, seconds))
    return fmt(hours, minutes, seconds)

def td2s(delta, fmt=None):
    return timedelta2string(delta, fmt)

class TimeCost:
    def __init__(self, msg='Time Cost', verbose=True, verbose_fmt=None):
        self.ts = None
        self.verbose = verbose
        self.msg = msg
        self.verbose_fmt = verbose_fmt or (lambda msg, tts: f'{msg}: {tts}s')

    def __enter__(self):
        self.ts = dt.datetime.now()

    def __exit__(self, *args):
        self.ts = dt.datetime.now() - self.ts
        if self.verbose:
            print(self.verbose_fmt(self.msg, self.ts.total_seconds()))
