import boto3
import json

client = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")
nova_model_id = 'amazon.nova-micro-v1:0'
history = []

def get_history():
    return "\n".join(history)

def get_configuration():
    return json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [{"text": get_history()}]  # Fixed: must be a list of content objects
            }
        ],
        "inferenceConfig": {
            "maxTokens": 4096,
            "stopSequences": []
        }
    })

while True:
    user_input = input("User: ")

    if user_input.lower() == "exit":  # Fixed: moved before appending to history
        break

    history.append("User: " + user_input)  # Fixed: moved after exit check

    response = client.invoke_model(
        body=get_configuration(),
        modelId=nova_model_id,
        accept="application/json",
        contentType="application/json"  # Fixed: was "ontentType"
    )

    response_body = json.loads(response.get('body').read())
    output_text = response_body['output']['message']['content'][0]['text'].strip()  # Fixed: correct Nova response path

    print(output_text)
    history.append("Assistant: " + output_text)  # Fixed: added "Assistant:" prefix for clarity