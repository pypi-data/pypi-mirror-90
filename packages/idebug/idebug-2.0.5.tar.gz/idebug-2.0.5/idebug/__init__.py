# -*- coding: utf-8 -*-
print(f"{'@'*50} {__file__}")

# ============================================================ APIs.
from idebug._print import *
from idebug._print import (
    _dict,
    _dir,
    utestfunc,
)
[ 'PartGubun',
  'SectionGubun',
  '_dict',
  '_dir',
  'dictValue',
  'exception',
  'get_params',
  'loop',
  'moduleGubun',
  'now',
  'params',
  'timeline',
  'timelineDict',
  'utestfunc',
  'value',
  'valueLoc',
  'valueWithGubun',
  'viewLoopingData']


# ============================================================ MAIN.
if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    timeline(__file__)
    pp.pprint(dir())
