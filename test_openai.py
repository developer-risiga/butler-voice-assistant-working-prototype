# test_openai.py
import openai
import os
from dotenv import load_dotenv

print("=== TESTING OPENAI ===")
print(f"Current directory: {os.getcwd()}")

# Load environment variables
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
print(f'API Key exists: {bool(api_key)}')

if api_key:
    print(f'API Key starts with sk-: {api_key.startswith("sk-")}')
    print(f'API Key first 10 chars: {api_key[:10]}...')
else:
    print('❌ NO API KEY FOUND')
    print('Checking all environment variables:')
    for key, value in os.environ.items():
        if 'openai' in key.lower() or 'api' in key.lower():
            print(f'  {key}: {value}')

if api_key and api_key.startswith('sk-'):
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Hello, test message'}],
            max_tokens=50
        )
        print('✅ SUCCESS: API Key works!')
        print(f'Response: {response.choices[0].message.content}')
    except Exception as e:
        print(f'❌ FAILED: {e}')
else:
    print('❌ API Key missing or invalid format')
