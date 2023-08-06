# -*- coding: utf-8 -*-
print(f"{'@'*50} {__file__}")

# ============================================================ APIs.
from idebug._print import *



# ============================================================ MAIN.
if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    timeline(__file__)
    pp.pprint(dir())
