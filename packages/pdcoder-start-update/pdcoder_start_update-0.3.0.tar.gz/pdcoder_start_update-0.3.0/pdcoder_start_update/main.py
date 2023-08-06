

import sys
import os
from .Versions import VersionManager


# def find_arg(args, flag):
#     try:
#         idx = args.index(flag)
#         find = args[idx+1]
#         return find
#     except ValueError:
#         pass

#     return None


def main():
    vm = VersionManager()
    if vm.has_updated():
        print(f'发现新版本，开始更新')
        vm.start_update()
        print(f'更新完成()')

    # args = sys.argv

    # dir = find_arg(args, '-dir')
    # if dir:
    #     os.system(f'pdcoder -dir {dir}')

    os.system(f'pdcoder')

    sys.exit()


if __name__ == "__main__":
    pass
