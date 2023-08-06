"""Console script for chinadaily."""
import argparse
import sys
from datetime import datetime

from .constants import CLI_DATE_FORMAT, CLI_MONTH_FORMAT, CLI_YEAR_FORMAT
from .chinadaily import download


# todo(@yarving): auto generate version number
def get_version():
    """Get version number"""
    return '0.1.7'


def get_parser():
    """Get argument parser"""
    parser = argparse.ArgumentParser("China Daily newspaper downloader")
    parser.add_argument(
        'date', nargs='*',
        type=lambda s: datetime.strptime(s, CLI_DATE_FORMAT),
        help="default as today, multiple dates separated by blank")
    parser.add_argument(
        "-m", "--month",
        type=lambda s: datetime.strptime(s, CLI_MONTH_FORMAT),
        help="download a month's newspaper")
    parser.add_argument(
        "-y", "--year",
        type=lambda s: datetime.strptime(s, CLI_YEAR_FORMAT),
        help="download a year's newspaper")
    parser.add_argument(
        '-v', '--version',
        action='version', version=get_version(), help='Display version')
    parser.add_argument(
        "-f", "--force", help="force to re-write", action="store_true", default=False)

    return parser


def main():
    """Console script for chinadaily."""
    parser = get_parser()
    args = parser.parse_args()

    dates = args.date if args.date else [datetime.now()]
    for date in dates:
        download(date, force=args.force)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
