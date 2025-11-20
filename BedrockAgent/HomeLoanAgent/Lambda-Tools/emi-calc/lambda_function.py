import json

def lambda_handler(event, context):
    try:
        # Extract parameters from Bedrock Agent format
        parameters = event['parameters']
        principal = float(next(p['value'] for p in parameters if p['name'] == 'principal'))
        annual_rate = float(next(p['value'] for p in parameters if p['name'] == 'interest_rate'))
        tenure_years = float(next(p['value'] for p in parameters if p['name'] == 'tenure'))
        
        # Convert to monthly values
        monthly_rate = annual_rate / (12 * 100)
        tenure_months = tenure_years * 12
        
        # EMI calculation formula
        if monthly_rate == 0:
            emi = principal / tenure_months
        else:
            emi = principal * monthly_rate * (1 + monthly_rate)**tenure_months / ((1 + monthly_rate)**tenure_months - 1)
        
        return {
            'response': {
                'actionGroup': event['actionGroup'],
                'function': event['function'],
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': json.dumps({
                                'emi': round(emi, 2),
                                'total_amount': round(emi * tenure_months, 2),
                                'total_interest': round((emi * tenure_months) - principal, 2)
                            })
                        }
                    }
                }
            }
        }
    
    except Exception as e:
        return {
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