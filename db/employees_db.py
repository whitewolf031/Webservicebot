import psycopg2
from config import Config

cfg = Config()

class Employees_db:
    def __init__(self):
        self.connect = psycopg2.connect(
            host=cfg.host,
            user=cfg.user,
            database=cfg.db,
            password=cfg.password
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                fio VARCHAR(255),
                email TEXT,
                quest VARCHAR(255),
                phone VARCHAR(40)
            )
        """)
        self.connect.commit()

    def insert_data(self, chat_id, fio, email, quest, phone):
        self.create_table()  # Kiritishdan oldin jadval mavjudligini tekshiradi
        self.cursor.execute("""
            INSERT INTO employees (chat_id, fio, email, quest, phone)
            VALUES (%s, %s, %s, %s, %s)
        """, (chat_id, fio, email, quest, phone))
        self.connect.commit()

    def update_data(self, chat_id, fio=None, email=None, quest=None, phone=None):
        # Yangilash uchun SQL so'rovini yaratamiz
        set_clause = []
        params = []

        if fio:
            set_clause.append("fio = %s")
            params.append(fio)
        if email:
            set_clause.append("email = %s")
            params.append(email)
        if quest:
            set_clause.append("quest = %s")
            params.append(quest)
        if phone:
            set_clause.append("phone = %s")
            params.append(phone)

        # Agar yangilash uchun ma'lumotlar bo'lsa
        if set_clause:
            sql_query = f"UPDATE employees SET {', '.join(set_clause)} WHERE chat_id = %s"
            params.append(chat_id)
            self.cursor.execute(sql_query, params)
            self.connect.commit()

    def check_chat_id_exists(self, chat_id):
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE chat_id = %s", (chat_id,))
        count = self.cursor.fetchone()[0]
        return count > 0  # True yoki False qaytaradi

    def select_data(self):
        self.cursor.execute("""
            SELECT fio, email, quest, phone
            FROM employees
        """)
        return self.cursor.fetchall()