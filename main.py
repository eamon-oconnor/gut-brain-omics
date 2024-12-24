"""
docstring placeholder
"""

from modules import utils
import argparse
import pandas as pd


def get_fh_argparse():
    """
    Get file handle command line options using argparse
    @param: NoneType
    @return: ArgumentParser
    """

    parser = argparse.ArgumentParser(
        description="Provide a CSV file of phenotypes and genera"
    )

    parser.add_argument(
        "-i",
        "--infile",
        dest="infile",
        type=str,
        help="Path to file to open",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        type=str,
        help="Path to directory to write results to",
        required=True,
    )

    # Execute parse_args() method
    return parser.parse_args()


def main():
    """ main """

    # Get infile and out directory from cdl
    args = get_fh_argparse()
    csv_fh = args.infile
    result_dir = args.outdir

    # Convert csv to df
    df = pd.read_csv(csv_fh)

    # Loop through df rows
    for index, row in df.iterrows():
        