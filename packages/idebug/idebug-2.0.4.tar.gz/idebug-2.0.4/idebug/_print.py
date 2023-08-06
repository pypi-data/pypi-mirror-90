# -*- coding: utf-8 -*-
# print(f"{'@'*50} {__file__}")
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)

# ============================================================
from datetime import datetime
def now():
    return datetime.now()


def timeline(loc, msg=''):
    print(f"{now()} | {loc} | {msg}")

def timelineDict(loc, obj):
    timeline(loc, f"{obj}.__dict__:")
    pp.pprint(obj.__dict__)

def dictValue(loc, msg, dic):
    timeline(loc, msg)
    pp.pprint(dic)

def params(loc, **kw):
    _msg = f"params: {_get_params(**kw)}"
    timeline(loc, _msg)


def _get_params(**kw):
    notPrinted = ['self', '__class__','funcloc']
    return {k:v for k,v in kw.items() if k not in notPrinted}
def get_params(**kw):
    _get_params(**kw)


def exception(loc, e, msg=''):
    print(f"{now()} | Error | {loc} | {e} | {msg}")

def moduleGubun(_file_):
    print(f"{'@'*50} {_file_}")

def PartGubun(partnm):
    print(f"\n\n{'='*100} {partnm}")

def SectionGubun(sectnm):
    print(f"\n{'-'*100} {sectnm}")


def _dict(obj, loc=None):
    try:
        if loc is None:
            print(f"\n\n{'-'*50} {obj}.__dict__:")
        else:
            timeline(loc, f"{obj}.__dict__:")
        pp.pprint(obj.__dict__)
    except Exception as e:
        print(f"{'#'*50} {__name__}.{inspect.stack()[0][3]} | e: {e}")

def _dir(obj):
    try:
        print(f"\n\n{'-'*50} dir({obj}):")
        pp.pprint(dir(obj))
    except Exception as e:
        print(f"{'#'*50} {__name__}.{inspect.stack()[0][3]} | e: {e}")

def loop(loc, i, _len, msg=''):
    print(f"{now()} | {loc} {'-'*50} {i}/{_len} | {msg}")

def value(v):
    if isinstance(v, dict):
        pp.pprint(v)
    else:
        print(v)

def valueWithGubun(v, sectnm):
    SectionGubun(sectnm)
    value(v)

def valueLoc(v, loc, msg):
    print(f"{loc} | {msg}")
    value(v)

def viewLoopingData(data):
    _len = len(data)
    for i, d in enumerate(data, start=1):
        print('\n')
        loop('', i, _len)
        for k, v in d.items():
            print(f"{k}: {v}")



# ============================================================ Decorator.
from datetime import datetime
def _convert_timeunit(seconds):
    sec = 1
    msec = sec / 1000
    min = sec * 60
    hour = min * 60

    t = seconds
    if t < sec:
        unit = 'msec'
        t = t / msec
    elif sec <= t <= min:
        unit = 'secs'
    elif min < t <= hour:
        unit = 'mins'
        t = t / min
    else:
        unit = 'hrs'
        t = t / hour

    return round(t, 1), unit

def utestfunc(f):
    def _utestfunc(*args, **kwargs):
        start_dt = datetime.now()
        loc = f"{f.__module__}.{f.__qualname__}"
        line = f"{'='*100}"
        print(f"\n\n\n{line}\n{datetime.now()} | {loc} | {args} | {kwargs}")


        rv = f(*args, **kwargs)


        timeExp, unit = _convert_timeunit(
                        (datetime.now() - start_dt).total_seconds())

        print(f"\n{datetime.now()} | {loc} | Runtime: {timeExp} ({unit})")

        return rv
    return _utestfunc
