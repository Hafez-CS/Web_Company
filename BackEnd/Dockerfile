# Dockerfile
FROM python:3.11

# جلوگیری از ایجاد pyc و فعال کردن لاگ لحظه‌ای
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب پیش‌نیازها
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . /app/

# باز کردن پورت
EXPOSE 8000

# اجرای سرور توسعه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]