import requests



def createJSONPostRequest(aspace_url,api_key,json_payload):
    headers = {
        'Content-Type': 'application/json',
        'apikey':api_key
    }
    aspace_response = requests.post(aspace_url,headers=headers, data = json_payload, verify=False)
    return(aspace_response)

def createMultipartPostRequest(aspace_url,api_key,files,payload):
    headers = {
        'apikey': api_key
    }
    aspace_response = requests.post(aspace_url, headers=headers,files=files, data=payload, verify=False)
    return(aspace_response)

