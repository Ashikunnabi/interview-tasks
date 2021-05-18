from django.db import models
from django.core.exceptions import ValidationError


class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    is_child = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self.is_child:
            if self.parent is None:
                # child must have parent to be added as user
                raise ValidationError('Parent is required for this user.')
            else:
                # below fields value will be empty as child must not have any address
                self.street = ''
                self.city = ''
                self.state = ''
                self.zip = ''
        return super(User, self).save(*args, **kwargs)
