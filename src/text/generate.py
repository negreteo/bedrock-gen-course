import boto3
import json
import pprint

client = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")
nova_model_id = 'amazon.nova-micro-v1:0'

nova_config = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": [{"text": "Tell me a story about a dragon"}]
        }
    ],
    "inferenceConfig": {
        "maxTokens": 4096,
        "temperature": 0,
        "topP": 1
    }
})

response = client.invoke_model(
    body=nova_config,
    modelId=nova_model_id,
    accept='application/json',
    contentType='application/json'
)

response_body = json.loads(response.get('body').read())
pp = pprint.PrettyPrinter(depth=4)
pp.pprint(response_body['output']['message']['content'][0]['text'])