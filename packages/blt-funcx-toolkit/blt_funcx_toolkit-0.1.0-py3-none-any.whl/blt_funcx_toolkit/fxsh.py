"""
FuncX Shell - `fxsh`

Use FuncX to open a virtual
    interactive session on a FuncX endpoint.

Any commands input will be forwarded to the
    endpoint using `subprocess.check_output`

Has only been tested with Linux-based endponits
"""

import argparse
import sys

from blt_funcx_toolkit.execution import fxsh
from blt_funcx_toolkit.config import blt_endpoints
from blt_funcx_toolkit.version import VERSION


def cli_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint-name",
                        "-ep",
                        type=str,
                        help="Endpoint to open interactive session on",
                        default="blt_small",
                        choices=list(blt_endpoints.keys()))
    parser.add_argument("--verbose",
                        "-v",
                        action="store_true",
                        help="Enable verbose output",
                        default=False)
    parser.add_argument("--version",
                        action="store_true",
                        help="Print version number and exit",
                        default=False)
    args = parser.parse_args()
    if args.version:
        print(f"blt-funcx-toolkit version: {VERSION}")
        sys.exit(0)

    fxsh(endpoint_name=args.endpoint_name, print_wait=args.verbose)


if __name__ == '__main__':
    cli_run()
