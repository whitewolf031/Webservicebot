# Python bazaviy rasmidan foydalanamiz
FROM python:3.10-slim

# Loyihaning ishlash katalogini aniqlash
WORKDIR /app

# Kutubxonalar ro‘yxatini konteynerga ko‘chirish
COPY requirements.txt .

# Kutubxonalarni o‘rnatish
RUN pip3 freeze > requirements.txt

# Botning asosiy faylini ko‘chirish
COPY bot.py .

# Botni ishga tushirish
CMD ["python", "bot.py"]
