from dotenv import load_dotenv
import os
import urllib.parse as up

class Config:
    def __init__(self):
        load_dotenv()
        self.db_bot()
        self.set_bot_config()

    def set_bot_config(self):
        self.token = os.getenv("TOKEN", "defaulttoken")
        self.canal_id = os.getenv("CANAL_ID")
        self.owner_id = os.getenv("OWNER_ID")

    def db_bot(self):
        self.host = os.getenv("PGHOST", "localhost")
        self.user = os.getenv("PGUSER", "postgres")
        self.db = os.getenv("PGDATABASE", "default_db")
        self.password = os.getenv("PGPASSWORD", "123456")