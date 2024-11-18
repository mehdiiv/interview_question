from django.db import models


class User(models.Model):
    email = models.CharField(max_length=128, blank=False, null=False)
    json_web_token = models.CharField(max_length=1024, blank=False, null=False)

    class Meta:
        db_table = "users"
