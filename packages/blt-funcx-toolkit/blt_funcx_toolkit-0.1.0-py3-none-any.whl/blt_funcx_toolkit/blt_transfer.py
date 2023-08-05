import argparse
import sys

from blt_funcx_toolkit.version import VERSION
from blt_funcx_toolkit.transfer import upload_file_to_blt, download_file_from_blt


def cli_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--upload",
                        action="store_true",
                        default=False,
                        help="Use upload mode")
    parser.add_argument("-d",
                        "--download",
                        action="store_true",
                        default=False,
                        help="Use download mode")
    parser.add_argument("-l",
                        "--local-path",
                        type=str,
                        default=None,
                        help="Specify Local Path")
    parser.add_argument("-r",
                        "--remote-path",
                        type=str,
                        default=None,
                        help="Specify Remote (BLT) Path")
    parser.add_argument(
        "-n",
        "--username",
        type=str,
        default=None,
        help="Specify BLT username. Required if different from local username."
    )
    parser.add_argument("-k",
                        "--private-key",
                        type=str,
                        default=None,
                        help="Specify private key location. Optional")
    parser.add_argument("--version",
                        action="store_true",
                        help="Print version number and exit",
                        default=False)
    args = parser.parse_args()

    if args.version:
        print(f"blt-funcx-toolkit version: {VERSION}")
        sys.exit(0)

    if args.upload and args.download:
        print("ERROR: Cannot upload and download together.")
        sys.exit(1)

    if args.upload:
        upload_file_to_blt(local_path=args.local_path,
                           remote_path=args.remote_path,
                           username=args.username)
    elif args.download:
        download_file_from_blt(local_path=args.local_path,
                               remote_path=args.remote_path,
                               username=args.username)
    else:
        print("WARN: No action specified. Exiting.")


if __name__ == '__main__':
    cli_run()
