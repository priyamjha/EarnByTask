from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)
    
    
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)  # Add this field

    objects = CustomUserManager()

    
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    

class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    download_link = models.URLField()
    points = models.IntegerField(default=0)
    logo = models.ImageField(upload_to='app_logos/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="apps", blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="apps", blank=True, null=True)


    def __str__(self):
        return self.name
    



class TaskSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="submissions")
    app = models.ForeignKey(AndroidApp, on_delete=models.CASCADE, related_name="submissions")
    image = models.ImageField(upload_to="task_submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)  # Admin approval
    points_awarded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"




