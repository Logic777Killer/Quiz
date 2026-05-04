from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другое'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    country = models.CharField(max_length=50)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"Профиль {self.user.username}"
