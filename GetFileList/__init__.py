import os
from azure.storage.blob import ContainerClient

def main(name: str) -> list:
    storage_connection_string = os.environ["AzureWebJobsStorage"]
    container = ContainerClient.from_connection_string(conn_str=storage_connection_string, container_name="cat-images")
    blob_list = container.list_blobs()
    results = []
    for blob in blob_list:
        results.append(blob.name)
    return results