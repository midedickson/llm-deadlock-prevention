from openai import OpenAI
from decouple import config


class ModelFactory:
    instance = None

    def get_instance() -> OpenAI:
        if ModelFactory.instance is None:
            ModelFactory.instance = OpenAI(api_key=config("OPENAI_API_KEY"))
        return ModelFactory.instance
