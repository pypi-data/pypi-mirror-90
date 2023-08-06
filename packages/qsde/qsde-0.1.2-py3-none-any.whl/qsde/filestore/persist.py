import logging
from typing import Optional, Tuple, Iterable
from datetime import datetime

import pandas as pd
from google.cloud import storage

logger = logging.getLogger(__name__)

PARTITION_BY = {"Y": "%Y", "M": "%Y/%m", "D": "%Y/%m/%d"}
REFERENCE_PERIOD = "reference_period"


def persist_timeseries_to_gcp_storage(
    df: pd.DataFrame,
    bucket_name: str,
    file_name: str,
    partition_by: str,
    client: Optional[storage.Client],
) -> bool:
    if client is None:
        client = storage.Client()

    bucket: storage.Bucket = client.bucket(bucket_name)
    for blob_name, data in group_timeseries_by_partition(df, file_name, partition_by):
        blob = bucket.blob(blob_name)
        blob.upload_from_string(data.to_csv(None, index=False), client=client)
    return True


def group_timeseries_by_partition(
    df: pd.DataFrame,
    file_name: str,
    partition_by: str,
) -> Iterable[Tuple[str, pd.DataFrame]]:
    if partition_by not in PARTITION_BY:
        raise NotImplementedError(f"partition_by must be in {PARTITION_BY}")

    if REFERENCE_PERIOD not in df:
        raise ValueError(
            f"DataFrame df must be a timeseries with a column named '{REFERENCE_PERIOD}'."
        )

    df[REFERENCE_PERIOD] = pd.to_datetime(
        df[REFERENCE_PERIOD], infer_datetime_format=True, errors="raise"
    )
    df["reference_period_str"] = df[REFERENCE_PERIOD].dt.strftime(
        PARTITION_BY[partition_by]
    )

    for partition_name, group in df.groupby("reference_period_str"):
        group.drop(columns=["reference_period_str"], inplace=True)
        group.reset_index(drop=True, inplace=True)
        yield (f"{partition_name}/{file_name}.csv", group)

