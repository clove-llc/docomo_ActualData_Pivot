from google.cloud import bigquery

class BigQueryClient:
    def __init__(
        self,
        gcp_project_id: str,
        dataset_id: str,
    ):
        self.client = bigquery.Client(project=gcp_project_id)
        self.dataset_ref = f"{gcp_project_id}.{dataset_id}"