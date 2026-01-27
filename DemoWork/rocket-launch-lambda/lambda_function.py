import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(f"Event received: {json.dumps(event)}")
    
    action_group = event['actionGroup']
    api_path = event['apiPath']
    http_method = event.get('httpMethod', 'POST')
    parameters = event.get('parameters', [])
    
    bucket_name = 'bedrock-agent-rocket-launch-logs'
    rocket_name = 'Falcon-9'
    
    for param in parameters:
        if param['name'] == 'bucket_name':
            bucket_name = param['value']
        elif param['name'] == 'rocket_name':
            rocket_name = param['value']
    
    timestamp = datetime.utcnow().isoformat()
    filename = f"launch-{timestamp}.txt"
    
    content = f"""
ROCKET LAUNCH REPORT
====================
Rocket: {rocket_name}
Launch Time: {timestamp}
Status: SUCCESS
Mission: Deployment Complete
Altitude: 400km
Velocity: 28,000 km/h
====================
"""
    
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=content,
        ContentType='text/plain'
    )
    
    response_body = {
        'TEXT': {
            'body': f'Successfully launched rocket {rocket_name}! Launch report saved to {filename}'
        }
    }
    
    action_response = {
        'actionGroup': action_group,
        'apiPath': api_path,
        'httpMethod': http_method,
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    print(f"Response: {json.dumps(action_response)}")
    
    return {
        'messageVersion': '1.0',
        'response': action_response
    }
