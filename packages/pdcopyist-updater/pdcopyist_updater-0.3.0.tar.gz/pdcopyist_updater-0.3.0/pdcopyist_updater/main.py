

import sys
import os
from .Versions import VersionManager


def find_arg(args, flag, return_value=True):
    try:
        idx = args.index(flag)

        if return_value:
            return True, args[idx+1]
        return idx >= 0, None
    except ValueError:
        pass

    return False, None


def main():
    usepip = False
    args = sys.argv

    has, _ = find_arg(args, '-linkpip', return_value=False)
    if has:
        usepip = True

    vm = VersionManager(usepip)
    if vm.has_updated():
        print(f'发现新版本，开始更新')
        vm.start_update()
        print(f'更新完成()')

    os.system(VersionManager.m_pkg_name)

    sys.exit()


if __name__ == "__main__":
    main()
