# Installation and Setup

## Environment Configuration

1. Create an `.env` file in the root directory with the following variables:

   ```
   OPENAI_API_KEY=your_key_here
   ```
   
   > **Note:** Your OpenAI API key will need read/write permissions as this project uses the OpenAI Agents SDK.

2. For observability (optional), you can also include:

   ```
   LANGFUSE_SECRET_KEY=your_secret_key
   LANGFUSE_PUBLIC_KEY=your_public_key
   LANGFUSE_HOST=your_langfuse_host
   ```

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Standard Run

```bash
python3 entrypoint.py
```

### With Langfuse Observability

To run with Langfuse observability (requires the relevant environment variables):

```bash
python3 entrypoint.py -o
```
