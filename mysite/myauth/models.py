from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_avatar_path(instance, filename):
    # Путь сохранения аватара пользователя
    return f'avatars/user_{instance.user.pk}/{filename}'

class Profile(models.Model):
    # Профиль пользователя, расширяет стандартную модель User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # Автоматически создавать профиль для нового пользователя
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Сохранять профиль при сохранении пользователя
    if hasattr(instance, 'profile'):
        instance.profile.save()
