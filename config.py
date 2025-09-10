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
        self.host = os.getenv("HOST", "localhost")
        self.user = os.getenv("USER", "postgres")
        self.db = os.getenv("DATABASE", "default_db")
        self.password = os.getenv("PASSWORD", "123456")



# class Config:
#     def __init__(self):
#         load_dotenv()
#         self.set_database_config()
#         self.set_bot_config()
#         self.set_url_config()
#
#     def set_database_config(self):
#         # Agar DATABASE_URL mavjud bo‘lsa, undan foydalanamiz
#         database_url = os.getenv("DATABASE_URL")
#         if database_url:
#             up.uses_netloc.append("postgres")
#             url = up.urlparse(database_url)
#             self.host = url.hostname
#             self.user = url.username
#             self.password = url.password
#             self.db = url.path[1:]
#             self.port = url.port
#         else:
#             # Aks holda alohida maydonlardan olamiz
#             self.host = os.getenv("HOST", "localhost")
#             self.user = os.getenv("USER", "postgres")
#             self.password = os.getenv("PASSWORD", "123456")
#             self.db = os.getenv("DATABASE", "mydb")
#             self.port = int(os.getenv("PORT", 5432))