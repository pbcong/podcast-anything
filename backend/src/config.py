# Configuration file for LLM

class Config:
    def __init__(self):
        self.text_model = "gpt-4o"
        self.audio_model = "tts-1"
        self.temperature = 0.7

    def get_model_name(self):
        return self.model_name

    def get_api_key(self):
        return self.api_key

    def get_max_tokens(self):
        return self.max_tokens

    def get_temperature(self):
        return self.temperature

    def get_top_p(self):
        return self.top_p

    def get_frequency_penalty(self):
        return self.frequency_penalty

    def get_presence_penalty(self):
        return self.presence_penalty
    
