from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.db_bot()
        self.getBotEnv()

    def getBotEnv(self):
        self.token = os.getenv("TOKEN", "deafulttoken")

    def db_bot(self):
        self.host = os.getenv("HOST", "localhost")
        self.user = os.getenv("USER", "postgres")
        self.db = os.getenv("DATABASE", "webcervice")
        self.password = os.getenv("PASSWORD", "123456")