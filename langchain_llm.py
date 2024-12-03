from pydantic import BaseModel, Field
from typing import List, Union
from enum import Enum
import os, logging, base64
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langsmith import traceable
from constants import *
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


clients = {
    "anthropic":ChatAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"), 
                               model_name=os.getenv("ANTHROPIC_MODEL"), 
                               temperature=0, max_tokens=DEFAULT_MAX_TOKENS),
    "openai": ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), 
                         model_name=os.getenv("OPENAI_MODEL"), 
                         temperature=0, max_tokens=DEFAULT_MAX_TOKENS),
    "fastopenai": ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), 
                             model_name=os.getenv("OPENAI_FAST_MODEL"), 
                             temperature=0, max_tokens=DEFAULT_MAX_TOKENS)
}

# Global variable to store the chosen API
chosen_api = "openai"

class BaseMessage:
    def __init__(self, text=None, image_data=None):
        self.content = []

        if text:
            self.add_text(text)

        if image_data:
            self.add_image(image_data)

    def add_text(self, text):
        """Adds a text message to the content."""
        self.content.append({
            "type": "text",
            "text": text
        })

    def add_image(self, image_data):
        """Adds an image in base64 encoding to the content."""
        base64_image = base64.b64encode(image_data).decode('utf-8')
        self.content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    def get_message(self):
        """Returns the formatted message content."""
        return self.content


class ResponseType(str, Enum):
    score = "score"
    reasons = "reasons"
    url = "url"
    email = "email"

class Score(BaseModel):
    value: int = Field(..., ge=0, le=100)

class Reasons(BaseModel):
    items: List[str] = Field(..., max_items=5)

class URL(BaseModel):
    value: str

class Email(BaseModel):
    subject: str
    body: str

class AIResponse(BaseModel):
    response_type: ResponseType
    content: Union[Score, Reasons, URL, Email]

@traceable
def talk_to_ai(prompt,
               max_tokens=DEFAULT_MAX_TOKENS,
               image_data=None,
               client=None):
    global chosen_api
    chosen_api = "openai"
    try:
        if chosen_api == "anthropic":
            response = talk_to_anthropic(prompt, max_tokens, image_data, client)
        elif chosen_api == "openai":
            response = talk_to_openai(prompt, max_tokens, image_data, client)
        elif chosen_api == "fastopenai":
            response = talk_fast()
        return response.strip() if response else ""
    except Exception as e:
        logging.error(f"Error in talk_to_ai: {str(e)}")
        return ""

@traceable
def talk_to_anthropic(prompt,
                      max_tokens=DEFAULT_MAX_TOKENS,
                      image_data=None,
                      client=None):
    if client is None:
        client = clients['anthropic']

    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

    if image_data:
        for img in image_data:
            base64_image = base64.b64encode(img).decode('utf-8')
            messages[0]["content"].append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image
                }
            })

    try:
        # response = client.messages.create(
        #     model=ANTHROPIC_MODEL,  # Use model from environment variable
        #     max_tokens=max_tokens,
        #     messages=messages
        # )
        response = client.invoke(input=messages)
        return response.content[0].strip()
    except Exception as e:
        logging.error(f"Error in Anthropic AI communication: {str(e)}")
        return ""

@traceable
def talk_to_openai(prompt,
                   max_tokens=DEFAULT_MAX_TOKENS,
                   image_data=None,
                   client=None):
    if client is None:
        client = clients["openai"]

    message = BaseMessage(text=prompt, image_data=image_data[0] if image_data else None)

    if image_data and len(image_data) > 1:
        for img in image_data[1:]:
            message.add_image(img)
    messages=[{"role": "user", "content": message.get_message()}]
    try:
        # response = client.chat.completions.create(
        #     model=OPENAI_MODEL,
        #     messages=messages,
        #     max_tokens=max_tokens
        # )
        response = client.invoke(input=messages)
        return response.content.strip()
    except Exception as e:
        logging.error(f"Error in OpenAI communication: {str(e)}")
        return ""

@traceable
def talk_fast(messages,
              model=OPENAI_FAST_MODEL,
              max_tokens=DEFAULT_MAX_TOKENS,
              client=None,
              image_data=None):
    import tiktoken  # Ensure this package is installed: pip install tiktoken

    if client is None:
        client = clients['fastopenai']

    message = BaseMessage(text=messages, image_data=image_data[0] if image_data else None)

    if image_data and len(image_data) > 1:
        for img in image_data[1:]:
            message.add_image(img)

    # Estimate token count
    encoding = tiktoken.encoding_for_model(model)
    content_text = ''
    for item in message.get_message():
        if item['type'] == 'text':
            content_text += item['text']
    input_tokens = len(encoding.encode(content_text))

    # Ensure total tokens do not exceed context window
    context_window = GPT_4O_CONTEXT_WINDOW
    if input_tokens + max_tokens > context_window:
        max_tokens = context_window - input_tokens - 1  # Reserve 1 token for safety

        if max_tokens <= 0:
            logging.error("Input text is too long for the model to process.")
            return None  # Or handle as needed
    messages=[{"role": "user", "content": message.get_message()}]
    try:
        # response = client.chat.completions.create(
        #     model=model,
        #     messages=messages,
        #     max_tokens=max_tokens
        # )
        response = client.invoke(input=messages)
        return response.content.strip()
    except Exception as e:
        logging.error(f"Error in talk_fast: {str(e)}")
        return None
