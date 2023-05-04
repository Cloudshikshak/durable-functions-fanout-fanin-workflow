import os, requests, json, logging
from azure.storage.blob import ContainerClient

def main(imageName: str) -> str:
    storage_connection_string = os.environ["AzureWebJobsStorage"]
    container = ContainerClient.from_connection_string(conn_str=storage_connection_string, container_name="cat-images")
    blob_client = container.get_blob_client(imageName)
    
    headers = {'Ocp-Apim-Subscription-Key': os.environ["COMPUTER_VISION_API_KEY"], 'Content-Type': 'application/octet-stream'}
    
    response = requests.post('https://'+os.environ["COMPUTER_VISION_RESOURCE_NAME"]+'.cognitiveservices.azure.com/vision/v3.2/analyze?visualFeatures=Objects&language=en&model-version=latest', headers=headers, data=blob_client.download_blob().readall())
    analysis_result = json.loads(response.text)
    
    # Check if the image contains cat
    image_contains_cat = False
    if 'objects' in analysis_result:
        for object in analysis_result['objects']:
            if object['object'] == 'cat':
                image_contains_cat = True
                break

    analysis_result['contains_cat'] = image_contains_cat
    analysis_result['image_name'] = imageName
    return analysis_result
    