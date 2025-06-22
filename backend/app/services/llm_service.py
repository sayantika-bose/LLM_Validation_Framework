from langchain_ollama import OllamaLLM
from jinja2 import Template
import os
import logging

class LLMService:
    def __init__(self):
        logging.info("Initializing LLMService and loading model...")
        self.model = OllamaLLM(model="deepseek-r1:1.5b", base_url="http://host.docker.internal:11434")
        self.prompt_template = self._load_prompt_template()
        logging.info("LLMService initialized successfully.")

    def _load_prompt_template(self):
        template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "chat_prompt.j2")
        logging.info(f"Loading prompt template from {template_path}")
        try:
            with open(template_path, 'r') as f:
                template = Template(f.read())
            logging.info("Prompt template loaded successfully.")
            return template
        except Exception as e:
            logging.error(f"Failed to load prompt template: {e}")
            raise

    async def get_response(self, prompt: str) -> str:
        try:
            logging.info(f"Rendering prompt for user input: {prompt}")
            rendered_prompt = self.prompt_template.render(user_prompt=prompt)
            logging.info(f"Rendered prompt: {rendered_prompt}")

            logging.info("Invoking LLM model...")
            response = self.model.invoke(rendered_prompt)
            logging.info(f"Model response: {response}")

            if isinstance(response, dict) and "content" in response:
                logging.info("Extracted 'content' from model response.")
                return response["content"]
            return str(response)

        except Exception as e:
            logging.error(f"Error in LLMService.get_response: {e}")
            raise
