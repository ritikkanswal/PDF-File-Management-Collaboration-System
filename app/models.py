from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    # No need to define id, username, password, and email fields as they are already provided by AbstractUser
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

class PDFFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdf_files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    unique_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return self.title

class SharedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.ForeignKey(PDFFile, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)+" : "+str(self.pdf_file.file.name)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.ForeignKey(PDFFile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)+" : "+str(self.pdf_file.file.name)



