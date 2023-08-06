import sys
import shutil
import re
import time
from addict import Dict

symbols = Dict({
        'prev_line': '\033[F',
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'yellow': '\033[93m',
        'magenta': '\033[95m',
        'grey' : '\033[90m',
        'black' : '\033[90m',
        'default' : '\033[99m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    })

def format_time(t):
    return time.strftime("%H:%M:%S", time.gmtime(t))

def format_str(fmt, s, end=None):
    if end is None:
        end = symbols.end
    if isinstance(fmt, list):
        return ''.join([symbols[f] for f in fmt]) + str(s) + end
    return symbols[fmt] + str(s) + end

# =========================================================
#  Source: https://stackoverflow.com/questions/2186919
#  Author: John Machin
# =========================================================
strip_ANSI_escape_sequences_sub = re.compile(r"""
    \x1b     # literal ESC
    \[       # literal [
    [;\d]*   # zero or more digits or semicolons
    [A-Za-z] # a letter
    """, re.VERBOSE).sub
def strip_ANSI_escape_sequences(s):
    return strip_ANSI_escape_sequences_sub("", s)
# =========================================================

def len_ANSI(msg):
    return len(strip_ANSI_escape_sequences(msg))

class qqdm():
    def __init__(self, iterable, dynamic_ncols=True, **kwargs):
        self.fp = sys.stderr
        # self.tqdm = tqdm(iterable, dynamic_ncols=True, **kwargs)
        # self.tqdm = iterabletime.strftime("%H:%M:%S", time.gmtime())
        self.dynamic_ncols = dynamic_ncols
        self.iterable = iterable
        self.iter = iter(self.iterable)
        self.counter = 0
        self.ncols = 20
        self.bar = ''
        self.prefix = ''
        self.postfix = ''
        self.msg = ''
        self._msg = ''
        self.default_kv_format = format_str(['blue'], '{key}: ') + '{value}'
        self.ctrls = Dict({
            'default': 'default',
            'end': 'end'
        })

    def set_ctrls_by_dict(self, dct):
        for k, v in dct.items():
            self.set_ctrls(k, v)

    def set_ctrls(self, k, v):
        self.ctrls[k] = v

    def __len__(self):
        return len(self.iterable)

    def __iter__(self):
        # for i in self.tqdm:
            # yield i
        self.start_time = time.time()
        return self

    def get_ncols(self):
        if self.dynamic_ncols:
            return shutil.get_terminal_size()[0]
        else:
            return self.ncols

    def __next__(self):
        elapsed = time.time() - self.start_time
        persent = self.counter / len(self)
        remaining = elapsed * (1 / persent - 1) if self.counter != 0 else 0
        spd_msg = f'{self.counter / elapsed:.2f}it/s'


        elapsed = format_time(elapsed)
        remaining = format_time(remaining)
        
        ncols = self.get_ncols()
        bar_ncols = ncols - 9
        bar = format_str('green', '#') * int(persent * bar_ncols)
        bar = self.fill(bar, ' ', bar_ncols)
        # self.add(format_str(['yellow', 'bold'], 'Iteration'))
        # self.add([format_str(['cyan', ], 'Iteration: '), f'{self.counter} /{format_str("yellow",len(self))}'])
        # self.add([format_str(['cyan', ], 'Elapsed: '), f'{elapsed} <{format_str("yellow",remaining)}'])

        iter_msg = f'{self.counter}/{format_str("yellow",len(self))}'
        time_msg = f'{elapsed} <{format_str("yellow",remaining)}'
        if self.counter != 0:
            self.add(self.fill('', '-'))
            self.add(f'{"Iter":^{len_ANSI(iter_msg)+2}s}'
                f'{"Elapsed Time":^{len_ANSI(time_msg)+2}s}'
                f'{"Speed":^{len_ANSI(spd_msg)+2}s}')
            # self.add(self.fill('', '-'))
            self.add(f'{iter_msg:^{len(iter_msg)+2}s}'
                f'{time_msg: ^{len(time_msg)+2}s}'
                f'{spd_msg: ^{len(spd_msg)+2}s}')
            self.bar = f'{persent*100: >5.1f}% |{bar}|'
        try:
            ret = next(self.iter)
            self.update()
            self.counter += 1
            return ret
        except:
            self.update()
            self.fp.write('\n')
            self.fp.flush()
            raise StopIteration
        
    def _add_str(self, msg):
        return msg

    def _add_list(self, msg):
        return ''.join([str(s) for s in msg])

    def _add_dict(self, msg, kv_format):
        if kv_format is None:
            kv_format = self.default_kv_format
        ret = '\n'.join([kv_format.format(key=k, value=v)
         for k, v in msg.items()])
        return ret

    def add(self, msg, kv_format=None, place_holder=None):
        if isinstance(msg, str):
            _msg = self._add_str(msg)
        elif isinstance(msg, list):
            _msg = self._add_list(msg)
        elif isinstance(msg, dict):
            _msg = self._add_dict(msg, kv_format)
        else:
            _msg = str(msg)
        # update self.msg
        if len(self.msg) > 0:
            self.msg = self.msg + '\n' + _msg
        else:
            self.msg = _msg

    def fill(self, msg, token=' ', maxcols=None):
        if maxcols is None:
            maxcols = shutil.get_terminal_size()[0]
        # return f'{msg:<{maxcols}}'
        exp = maxcols - len_ANSI(msg)
        return f'{msg}{token*exp}'

    def update(self, *args):
        # flush the msg
        self.msg = self.prefix + self.msg + self.postfix
        if len(self._msg) > 0:
            n_line = self._msg.count('\n')
        else:
            n_line = 0
        _msg_filled = [self.fill(m) for m in self.msg.split('\n')]
        _msg = '\n'.join(_msg_filled)
        self._msg = n_line * symbols.prev_line + _msg + '\n' + self.bar
        self.fp.write(self._msg)
        self.fp.flush()
        self.msg = ''

__all__ = [
    'qqdm',
    'format_str'
]
