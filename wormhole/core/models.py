from django.conf import settings
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50, default="")
    token = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


class ShortLink(models.Model):
    class Meta:
        indexes = [models.Index(fields=["alias"], name="alias_idx")]

    url = models.CharField(max_length=200)
    alias = models.CharField(max_length=10, unique=True)
    randoms = models.CharField(max_length=10, default="")
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def build_url(self):
        return settings.BASE_URL + "/" + self.alias
