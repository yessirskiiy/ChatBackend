from django.db import models
from django.contrib.auth.models import User


class Dialog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialog_author')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialog_partner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.user}, id:{self.id}'


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    attachments = models.FileField(upload_to='attachments/', default=None, blank=True)
    send_at = models.DateTimeField(auto_now_add=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: {self.text}'[:50]
