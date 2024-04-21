from allauth.account.signals import email_confirmed
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.utils.crypto import get_random_string


class RegistrationConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

@receiver(email_confirmed)
def email_confirmed_callback(sender, request, email_address, **kwargs):
    user = email_address.user
    confirmation_code = get_random_string(length=100)
    RegistrationConfirmation.objects.create(user=user, confirmation_code=confirmation_code)
    registration_confirmation = RegistrationConfirmation.objects.get(user=user)
    registration_confirmation.is_confirmed = True
    registration_confirmation.save()

class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = RichTextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def send_notification_email(self):
        subject = 'Новый отклик на ваше объявление'
        message = f'Пользователь {self.user.username} оставил отклик на ваше объявление "{self.ad.title}".\n\nТекст отклика: {self.text}'
        sender_email = 'goskazon@yandex.ru'  # Замените на ваш email
        recipient_email = self.ad.user.email
        send_mail(subject, message, sender_email, [recipient_email])





