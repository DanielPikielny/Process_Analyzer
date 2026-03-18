from openai import OpenAI
from schema import validate_output
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    with open("prompts/process_prompt.txt") as f:
        PROMPT_TEMPLATE = f.read()
except FileNotFoundError:
    logger.error("process_prompt.txt not found in prompts/ directory.")
    raise


def analyze_process(text: str) -> dict:
    full_prompt = PROMPT_TEMPLATE + text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2
        )
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return {"error": f"API request failed: {str(e)}"}

    output = response.choices[0].message.content

    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse model output as JSON: {e}\nOutput was: {output}")
        return {"error": "Model did not return valid JSON"}

    if not validate_output(data):
        logger.error(f"Model output missing required fields. Got keys: {list(data.keys())}")
        return {"error": "Model response was missing required fields"}

    return data