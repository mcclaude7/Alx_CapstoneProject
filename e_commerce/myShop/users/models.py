from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Email is required')
        user = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
class User(AbstractUser ):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=False, max_length=20)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    pic = models.URLField()
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, null=True)