import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests.auth import HTTPBasicAuth


class RelocateJobsIndex:
    def __init__(self):
        self.index = "relocatejobs"
        self.client = OpenSearch(
            hosts=[{
                "host": "https://vpc-relocatejobs-anqymoss6yzmvsu432ckyyuyau.us-east-2.es.amazonaws.com", 
                "port": 443
            }],
            http_auth=HTTPBasicAuth("opensearch", os.environ.get('OPENSEARCH_PASSWORD')),
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

    def add_job(self, job_id, main_text):
        doc = {
            "job_id": job_id,
            "main_text": main_text
        }
        response = self.client.index(index=self.index, body=doc)
        return response

    def search_jobs(self, query_text):
        body = {
            "query": query_text
        }
        return self.client.search(index=self.index, body=body)
