import toml


class Config:
    def __init__(self):
        self.config = toml.load("config.toml")

    def get_telegram_bot(self):
        return self.config["bot"]["telegram_bot_token"]

    def get_allowed_users(self):
        return self.config["bot"]["allowed_ids"]

    def get_bot_name(self):
        return self.config["bot"]["name"]

    def get_sqlite_db(self):
        return self.config["bot"]["sqlite_db"]

    def get_model(self):
        return self.config["ollama"]["model"]

    def get_system_prompt(self):
        return self.config["ollama"]["system_prompt"]

    def get_llm_type(self):
        return "Ollama"
