# Install and run
Create an .env file in root directory and include OPENAI_API_KEY. This will need read write permissions as I am using OpenAI agents SDK.
You can also include the following for observablity:
LANGFUSE_SECRET_KEY
LANGFUSE_PUBLIC_KEY
LANGFUSE_HOST

pip install -r requirements.txt

python3 entrypoint.py

or run with langfuse observablity, you will need to include 3 relevant ENV vars.
python3 entrypoint.py -o
