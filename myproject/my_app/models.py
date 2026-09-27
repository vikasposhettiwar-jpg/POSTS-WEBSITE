from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=200)
    subtitle=models.CharField(max_length=400)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')  #pip install pillow
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    
    #python manage.py makemigrations --> creattes a file
    #python manage.py migrate -->applies changes to the file

