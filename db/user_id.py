import psycopg2
from config import Config

cfg = Config()

class UserIDsDB:
    def __init__(self):
        # PostgreSQL'ga ulanish
        self.connect = psycopg2.connect(
            host=cfg.host,
            user=cfg.user,
            database=cfg.db,
            password=cfg.password
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        # Jadvalni yaratish
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_ids (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT UNIQUE NOT NULL
            )
        """)
        self.connect.commit()

    def insert_user(self, chat_id):
        # Foydalanuvchi ID'sini qo'shish
        self.create_table()  # Jadval mavjudligini tekshirish
        try:
            self.cursor.execute("""
                INSERT INTO user_ids (chat_id)
                VALUES (%s)
                ON CONFLICT (chat_id) DO NOTHING
            """, (chat_id,))
            self.connect.commit()
        except Exception as e:
            print(f"Foydalanuvchi ID'sini qo'shishda xato: {e}")

    def check_user_exists(self, chat_id):
        # Foydalanuvchi ID'si mavjudligini tekshirish
        self.cursor.execute("SELECT COUNT(*) FROM user_ids WHERE chat_id = %s", (chat_id,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def get_all_users(self):
        # Barcha foydalanuvchilarni olish
        try:
            self.cursor.execute("SELECT chat_id FROM user_ids")  # Jadval nomi to'g'irlangan
            users = self.cursor.fetchall()
            return [user[0] for user in users]
        except Exception as e:
            print(f"Foydalanuvchilarni olishda xatolik: {e}")
            return []