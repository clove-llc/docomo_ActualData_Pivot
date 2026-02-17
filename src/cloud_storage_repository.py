import logging
from io import BytesIO

import pandas as pd
from google.cloud import storage

logger = logging.getLogger(__name__)


class CloudStorageRepository:
    def __init__(self, client: storage.Client):
        self._client = client

    def fetch_excel_file(self, bucket_name: str, blob_name: str) -> pd.ExcelFile:
        logger.info(
            "Cloud Storage からイベント実績 Excel をダウンロードします: %s", blob_name
        )

        blob = self._client.bucket(bucket_name).blob(blob_name)
        file_bytes = blob.download_as_bytes()

        logger.info("ダウンロード完了。ExcelFile オブジェクトを生成します。")

        return pd.ExcelFile(BytesIO(file_bytes))
