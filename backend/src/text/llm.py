import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class llm_wrapper:
    def __init__(self, config, api_key=None):
        self.model = config.text_model
        self.temperature = config.temperature
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, prompt: str, stream=False):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=self.temperature,
            stream=stream
        )
        if stream:
            return response
        return response.choices[0].message.content

    def make_prompt(self, document, topic, prompt_template):
        return prompt_template.format(document, topic)
