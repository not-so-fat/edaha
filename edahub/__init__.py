import pandas

from .logic.project import EDAHub
from .logic import pandas_csv


def read_csv(buffer_or_filepath, **kwargs) -> pandas.DataFrame:
    """
    Load CSV as pandas.DataFrame with Int64 / datetime64 column inference
    Args:
        buffer_or_filepath: 1st argument for pandas.read_csv
        **kwargs: Arbitrary keyword arguments for pandas.read_csv

    Returns:
        pandas.DataFrame
    """
    return pandas_csv.read_csv(buffer_or_filepath, **kwargs)
