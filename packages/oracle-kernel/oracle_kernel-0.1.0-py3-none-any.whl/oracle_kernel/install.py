import os
import sys
import json
import base64
import argparse

from IPython.utils.tempdir import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager

kernel_logo = b'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'
kernel_json = {"argv":[sys.executable, "-m", "oracle_kernel", "-f", "{connection_file}"],
               "display_name":"Oracle",
               "language":"sql"}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        with open(os.path.join(td, 'logo-64x64.png'), 'wb') as f:
            f.write(base64.b64decode(kernel_logo))
        print('Installing Jupyter Oracle kernel spec.')
        KernelSpecManager().install_kernel_spec(td, 'Oracle', user=user, replace=True, prefix=prefix)

def _is_root():
    try:
        return os.geteuid()==0
    except AttributeError:
        return False

def main(argv=None):
    parser = argparse.ArgumentParser(description='Install Jupyter KernelSpec for Oracle Kernel.')
    prefix_locations = parser.add_mutually_exclusive_group()
    prefix_locations.add_argument('--user',
                                  help='Install Jupyter Oracle KernelSpec in user homedirectory.',
                                  action='store_true')
    prefix_locations.add_argument('--sys-prefix',
                                  help='Install Jupyter Oracle KernelSpec in sys.prefix. Useful in conda / virtualenv',
                                  action='store_true',
                                  dest='sys_prefix')
    prefix_locations.add_argument('--prefix',
                                  help='Install Jupyter Oracle KernelSpec in this prefix',
                                  default=None)
    args = parser.parse_args(argv)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)

if __name__ == '__main__':
    main()
