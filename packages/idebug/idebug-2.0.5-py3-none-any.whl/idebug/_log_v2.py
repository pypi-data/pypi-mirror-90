# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, date
import re
import logging

import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
# ============================================================ Project.
# ============================================================ My-Library.
from ipy import inumber
# ============================================================ Constant.




# ============================================================
import os

try:
    os.environ['LOG_PATH']
except Exception as e:
    print(f"""
        Read README.md
        You must setup LOG_PATH.
        {e}
    """)
    raise


#============================================================
"""ModuleInspector."""
#============================================================
try:
    path = os.environ['LOG_PATH']
    print(f"os.environ['LOG_PATH'] : {os.environ['LOG_PATH']}")
except Exception as e:
    print(f"""{'#'*50} {__name__}
        = = = = = ModuleInspector Error = = = = =

        To SetUp os.environ['LOG_PATH'] is compulsory in order to use idebug package.

        Please setup below in the terminal :
            export LOG_PATH=your_logs_location
        Or, you could setup LOG_PATH in the jupyter notebook like below :
            %env LOG_PATH=your_logs_location

        LOG_PATH is just a folder's path but not a file's path.
        Filename will be automatically created by datetime.
    """)
    raise
else:
    if os.path.isfile(path):
        path = os.path.dirname(path)
    t = datetime.today().isoformat(sep='T', timespec='hours')
    try:
        # os.makedirs(f"{path}/{t[:10]}")
        os.makedirs(path)
    except Exception as e:
        pass
    finally:
        LOG_FILE_PATH = f"{path}/{t[:10]}.log"
        print(f"LOG_FILE_PATH : {LOG_FILE_PATH}")
#============================================================
"""Loggers."""
#============================================================
def get_level():
    try:
        return os.environ['LOG_LEVEL']
        return lv
    except Exception as e:
        return logging.DEBUG
    else:
        if lv == 'DEBUG': return logging.DEBUG
        elif lv == 'INFO': return logging.INFO
        elif lv == 'WARNING': return logging.WARNING
        elif lv == 'ERROR': return logging.ERROR
        else: return logging.CRITICAL

def _console_():
    try:
        return int(os.environ['CONSOLE_LOGGER'])
    except Exception as e:
        return 0

"""Formatter."""
BASE_FMT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
basefmt = logging.Formatter(fmt=BASE_FMT)

logging.basicConfig(level=logging.DEBUG,
                    format=BASE_FMT,
                    # datefmt='%Y-%m-%d %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')

"""consoleLogger.
LogFile과 Console에 동시에 찍고 싶을때 사용.
"""
consoleLogger = logging.getLogger('console')
consoleLogger.setLevel(get_level())
sh = logging.StreamHandler()
sh.setFormatter(fmt=basefmt)
consoleLogger.addHandler(sh)

"""lineLogger.
LogFile에서만 찍어야 하고, 라인 구분자가 필요할 때 사용.
"""
lineLogger = logging.getLogger('line')
lineLogger.setLevel(get_level())
fh = logging.FileHandler(filename=LOG_FILE_PATH, mode='a')
fh.setFormatter(fmt=basefmt)
lineLogger.addHandler(fh)

"""valueLogger.
"""
valueLogger = logging.getLogger('value')
valueLogger.setLevel(get_level())
fh = logging.FileHandler(filename=LOG_FILE_PATH, mode='a')
valuefmt = logging.Formatter(fmt='%(message)s')
fh.setFormatter(fmt=valuefmt)
valueLogger.addHandler(fh)


#============================================================
"""Base Printers."""
#============================================================
def debug(v):
    valueLogger.debug(f'debug:{v}')
    valueLogger.info(f'info:{v}')
    consoleLogger.debug(f'c-debug:{v}')

#============================================================
"""Level-DEBUG :: LoopPrinter."""
#============================================================
def loop(i, len, vars, location, linetp='-', console=None):
    # msg = f"{linetp * 50} {i}/{len} | {vars} | {location}"
    msg = f"{i}/{len} | {vars} | {location}"
    if _console_():
        consoleLogger.info(msg=msg)
    else:
        lineLogger.info(msg=msg)
#============================================================
"""Level-DEBUG :: ValuePrinter."""
#============================================================
def _print_dict_(d):
    for k, v in d.items():
        valueLogger.debug(f"{'-'*50}\n{k} : {v}")

p_hidden = re.compile('^__.*')
def clsattrs(cls, deep=False, console=False, reg='_*df_*|data'):
    p_skip = re.compile(reg)
    try:
        whour = f"{'-'*50} cls : {cls.__class__.__name__}"
        attrs = dir(cls)
        if not deep:
            attrs = [e for e in attrs if p_hidden.match(e) is None]
        for attr in attrs:
            try:
                v = getattr(cls, attr)
                if p_skip.search(attr) is None:
                    if isinstance(v, dict):
                        printer(f"{whour}\na : {attr}\nt : {type(v)}\nv : {v}")
                        if console: pp.pprint(v)
                    else:
                        printer(f"{whour}\na : {attr}\nt : {type(v)}\nv : {v}")
                        if console: print(f"{whour}\na : {attr}\nt : {type(v)}\nv : {v}")
                else:
                    printer(f"{whour}\na : {attr}\nv : 생략.\nt : {type(v)}")
                    if console: print(f"{whour}\na : {attr}\nv : 생략.\nt : {type(v)}")
            except Exception as e:
                pass
    except Exception as e:
        exception(locals(), f"{__name__}.clsattrs")

def printdf(df, slen=50, console=False):
    if df is None:
        printer(locals())
        if console: print(locals())
    else:
        printer(f"\n{'* '*25} df.dtypes :\n{df.dtypes}")
        if console: print(f"\n{'* '*25} df.dtypes :\n{df.dtypes}")

        if len(df) > slen:
            printer(f"\n{'* '*25} df.head({slen}) :\n{df.head(slen)}")
            printer(f"\n{'* '*25} df.tail({slen}) :\n{df.tail(slen)}")
            if console: print(f"\n{'* '*25} df.head({slen}) :\n{df.head(slen)}")
            if console: print(f"\n{'* '*25} df.tail({slen}) :\n{df.tail(slen)}")
        else:
            printer(f"\n{'* '*25} df :\n{df}")
            if console: print(f"\n{'* '*25} df :\n{df}")

def printli(li, slen=10, console=False):
    printer(f"len : {len(li)}")
    if len(li) > slen:
        printer(f"li[:{slen}] :\n{li[:slen]}")
        if console: pp.pprint(li[:slen])
        printer(f"li[{-1*slen}:] :\n{li[-1*slen:]}")
        if console: pp.pprint(li[-1*slen:])
    else:
        printer(li)
        pp.pprint(li)

def printreport(f):
    def func(*args, **kwargs):
        print(f"\n{'*'*50} {f.__module__}.{f.__qualname__}")
        return f(*args, **kwargs)
    return func
#============================================================
"""Level-INFO :: ."""
#============================================================

#============================================================
"""Level-WARNING :: ."""
#============================================================
def warn(msg, f):
    """
    msg : Message
    f : Function
    """
    loc = f"{f.__module__}.{f.__qualname__}"
    if isinstance(msg, dict):
        lineLogger.warning(msg=loc)
        for k, v in msg.items():
            valueLogger.warning(msg=f"{k} : {v}")
    else:
        lineLogger.warning(msg=f"{loc} | {msg}")
#============================================================
"""Level-ERROR :: ."""
#============================================================
def error(e, f):
    """
    msg : Message
    f : Function
    """
    loc = f"{f.__module__}.{f.__qualname__}"
    if isinstance(msg, dict):
        lineLogger.error(msg=loc)
        for k, v in msg.items():
            valueLogger.error(msg=f"{k} : {v}")
    else:
        lineLogger.error(msg=f"{loc} | {msg}")

def exception(v, location=None):
    if isinstance(v, dict):
        msg = f"{'#'*50} {location}"
        consoleLogger.error(msg)
        _print_dict_(v)
    else:
        msg = f"{'#'*50} {location}\n{v}"
        consoleLogger.error(msg)
#============================================================
"""Level-CRITICAL :: ."""
#============================================================
#============================================================
"""ValuePrinter."""
#============================================================


def _console_dict_(d):
    for k, v in d.items():
        consoleLogger.debug(f"{'-'*50}\n{k} : {v}")

def printer(v, console=False):
    if isinstance(v, dict):
        _print_dict_(v)
    else:
        valueLogger.debug(v)

def console(v):
    if isinstance(v, dict):
        _console_dict_(d)
    else:
        consoleLogger.debug(v)
#============================================================
"""Level-INFO :: Function Printer."""
#============================================================
def fruntime(f):
    def _fruntime_(*args, **kwargs):
        start_dt = datetime.now()
        msg = f"{'+'*50} {f.__module__}.{f.__qualname__}"
        lineLogger.debug(msg)

        rv = f(*args, **kwargs)

        delta = (datetime.now() - start_dt).total_seconds()
        timeexp, unit = inumber.convert_timeunit(delta)
        msg = f"{'+ '*25} {f.__module__}.{f.__qualname__} | Runtime : {timeexp} ({unit})"
        lineLogger.debug(msg)
        return rv
    return _fruntime_

def utest(f):
    def _utest_(*args, **kwargs):
        start_dt = datetime.now()
        msg = f"{'='*50} {f.__module__}.{f.__qualname__}"
        lineLogger.debug(msg)

        rv = f(*args, **kwargs)

        timeexp, unit = inumber.convert_timeunit(
                        (datetime.now() - start_dt).total_seconds())
        msg = f"{'= '*25} {f.__module__}.{f.__qualname__} | Runtime : {timeexp} ({unit})"
        lineLogger.debug(msg)
        return rv
    return _utest_
