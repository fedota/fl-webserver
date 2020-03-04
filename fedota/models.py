from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class Problem(models.Model):

    def __str__(self):
        """Convert entry of class Problem to a string representation."""
        return "Prob-{}".format(self.id)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    data_def = models.TextField()
    files = models.FileField(
        upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['zip'])])
