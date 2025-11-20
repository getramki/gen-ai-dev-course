import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('bank-interest-rates')

def lambda_handler(event, context):
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # Extract optional parameters
        parameters = event.get('parameters', [])
        bank_name = next((p['value'] for p in parameters if p['name'] == 'bank_name'), None)
        loan_type = next((p['value'] for p in parameters if p['name'] == 'loan_type'), None)
        
        print(f"Extracted parameters - bank_name: {bank_name}, loan_type: {loan_type}")
        
        # Query based on parameters
        if bank_name and loan_type:
            print(f"Getting specific item for bank: {bank_name}, loan_type: {loan_type}")
            response = table.get_item(Key={'bank_name': bank_name, 'loan_type': loan_type})
            rates = [response['Item']] if 'Item' in response else []
        elif bank_name:
            print(f"Querying rates for bank: {bank_name}")
            response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('bank_name').eq(bank_name))
            rates = response['Items']
        else:
            print("Scanning all rates")
            response = table.scan()
            rates = response['Items']
        
        print(f"Found {len(rates)} rates")
        
        # Format rates for response
        formatted_rates = []
        for rate in rates:
            formatted_rates.append({
                'bank_name': rate['bank_name'],
                'interest_rate': float(rate['interest_rate']),
                'loan_type': rate['loan_type']
            })
        
        result = {
            'response': {
                'actionGroup': event['actionGroup'],
                'function': event['function'],
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': json.dumps({
                                'interest_rates': formatted_rates,
                                'count': len(formatted_rates)
                            })
                        }
                    }
                }
            }
        }
        print(f"Returning result: {json.dumps(result)}")
        return result
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_result = {
            'response': {
                'actionGroup': event.get('actionGroup', ''),
                'function': event.get('function', ''),
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': json.dumps({'error': str(e)})
                        }
                    }
                }
            }
        }
        print(f"Returning error result: {json.dumps(error_result)}")
        return error_result