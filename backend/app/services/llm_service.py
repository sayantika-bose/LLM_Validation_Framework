from langchain_ollama import OllamaLLM
from jinja2 import Template
import os
import logging
from typing import Dict, List, Any

class LLMService:
    def __init__(self):
        logging.info("Initializing LLMService and loading models...")
        self.models = {
            "deepseek-r1": OllamaLLM(model="deepseek-r1:1.5b", base_url="http://host.docker.internal:11434"),
            "qwen2.5": OllamaLLM(model="qwen2.5", base_url="http://host.docker.internal:11434"),
            "llama3.2": OllamaLLM(model="llama3.2", base_url="http://host.docker.internal:11434"),
            "gemma2": OllamaLLM(model="gemma2:2b", base_url="http://host.docker.internal:11434")
        }
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

    async def get_response(self, prompt: str, model_name: str = "deepseek-r1") -> str:
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not available")
                
            logging.info(f"Rendering prompt for user input: {prompt}")
            rendered_prompt = self.prompt_template.render(user_prompt=prompt)
            logging.info(f"Rendered prompt: {rendered_prompt}")

            logging.info(f"Invoking {model_name} model...")
            response = self.models[model_name].invoke(rendered_prompt)
            logging.info(f"Model response: {response}")

            if isinstance(response, dict) and "content" in response:
                logging.info("Extracted 'content' from model response.")
                return response["content"]
            return str(response)

        except Exception as e:
            logging.error(f"Error in LLMService.get_response: {e}")
            raise

    async def get_multiple_responses(self, prompt: str, model_names: List[str]) -> Dict[str, str]:
        responses = {}
        for model_name in model_names:
            try:
                responses[model_name] = await self.get_response(prompt, model_name)
            except Exception as e:
                responses[model_name] = f"Error: {str(e)}"
        return responses

    async def check_model_availability(self, model_name: str) -> bool:
        """Check if a model is available on the Ollama server"""
        try:
            if model_name not in self.models:
                return False
            # Try a simple test prompt to check if model is available
            test_response = self.models[model_name].invoke("Hello")
            return True
        except Exception as e:
            logging.warning(f"Model {model_name} not available: {e}")
            return False

    async def get_available_models(self) -> List[str]:
        """Get list of actually available models by testing each one"""
        available = []
        for model_name in self.models.keys():
            if await self.check_model_availability(model_name):
                available.append(model_name)
        return available if available else ["deepseek-r1"]  # Fallback to at least one model
