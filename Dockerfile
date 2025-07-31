# Python bazaviy rasmidan foydalanamiz
FROM python:3.10-slim

# Ish katalogini yaratamiz
WORKDIR /app

# requirements.txt faylini nusxalash
COPY reqiurements.txt .

# Kutubxonalarni o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botning asosiy faylini ko‘chirish
COPY bot.py .

# Botni ishga tushirish
CMD ["python", "bot.py"]
