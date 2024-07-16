import os
import django
from django.core.mail import send_mail

# Настройка Django окружения (замените 'your_project_name.settings' на реальное имя вашего проекта)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QT_website.settings')
django.setup()

def send_test_email():
    try:
        send_mail(
            'Test Email',
            'This is a test email sent from Django.',
            'info@qt.com.kz',  # Отправитель
            ['madiyaryep@gmail.com'],  # Замените на реальный email получателя
            fail_silently=False,
        )
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {e}")

if __name__ == '__main__':
    send_test_email()
