import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def get_completion(prompt, model="amazon.titan-text-express-v1"):
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 1
        }
    })

    response = bedrock.invoke_model(
        body=body,
        modelId=model,
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['results'][0]['outputText']

# Step 1: Generate a random recipe
recipe_prompt = "Generate a random recipe with a list of ingredients and basic instructions."
recipe = get_completion(recipe_prompt)
print("Generated Recipe:")
print(recipe)

# Step 2: Analyze the recipe for its cuisine type
cuisine_prompt = f"Analyze the following recipe and determine its cuisine type:\n\n{recipe}"
cuisine_type = get_completion(cuisine_prompt)
print("\nCuisine Type:")
print(cuisine_type)

# Step 3: Suggest a wine pairing
wine_prompt = f"Suggest a wine pairing for the following recipe and cuisine type:\n\nRecipe:\n{recipe}\n\nCuisine Type:\n{cuisine_type}. Give Final Output in JSON Format"
wine_pairing = get_completion(wine_prompt)
print("\nWine Pairing Suggestion:")
print(wine_pairing)
