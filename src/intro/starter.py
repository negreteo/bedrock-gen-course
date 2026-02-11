import boto3
import pprint
import subprocess
from botocore.exceptions import TokenRetrievalError

pp = pprint.PrettyPrinter(indent=4)

def get_bedrock_client():
    session = boto3.Session(profile_name='work-dev')
    try:
        client = session.client(region_name='us-east-1', service_name='bedrock')
        client.list_foundation_models()
        return client
    except TokenRetrievalError:
        print("SSO token expired. Re-authenticating...")
        subprocess.run(['aws', 'sso', 'login', '--profile', 'work-dev'])
        return session.client(region_name='us-east-1', service_name='bedrock')

def list_foundation_models():
    bedrock = get_bedrock_client()
    models = bedrock.list_foundation_models()
    print(models)
    for model in models['modelSummaries']:
        pp.pprint(model)
        pp.pprint("-----------------------")

def get_foundation_model(modelIdentifier):
    bedrock = get_bedrock_client()
    model = bedrock.get_foundation_model(modelIdentifier=modelIdentifier)
    pp.pprint(model)

#list_foundation_models()
get_foundation_model('anthropic.claude-haiku-4-5-20251001-v1:0')
