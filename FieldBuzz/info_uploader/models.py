import json
import time
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


def unix_timestamp():
    """Get current datetime in unix timestamp millisecond."""
    return int(round(time.time() * 1000))


def random_unique_string():
    """Generate unique random string."""
    return str(uuid.uuid4())


class AuthToken(models.Model):
    token = models.CharField(max_length=256)
    is_valid = models.BooleanField(default=True)
    created_at = models.PositiveIntegerField()
    updated_at = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set created_at during the instance creation.
            self.created_at = unix_timestamp()
            self.updated_at = unix_timestamp()
        else:
            self.updated_at = unix_timestamp()
        super(AuthToken, self).save(*args, **kwargs)


def validate_cv_file_json(value):
    # validate cv_file json
    value_json = json.loads(value)
    # check tsync_id key in json
    if 'tsync_id' not in value_json:
        raise ValidationError("JSON key 'tsync_id' is required.")


class PersonalInformation(models.Model):
    POSITION = (
        ('Mobile', 'Mobile'),
        ('Backend', 'Backend')
    )
    tsync_id = models.CharField(max_length=55, default=random_unique_string)
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    phone = models.CharField(max_length=14)
    full_address = models.CharField(max_length=512)
    name_of_university = models.CharField(max_length=256)
    graduation_year = models.PositiveIntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2020)])
    cgpa = models.FloatField(null=True, blank=True, validators=[MinValueValidator(2.0), MaxValueValidator(4.0)])
    experience_in_months = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    current_work_place_name = models.CharField(max_length=256, null=True, blank=True)
    applying_in = models.CharField(max_length=7, choices=POSITION)
    expected_salary = models.PositiveIntegerField(validators=[MinValueValidator(15000), MaxValueValidator(60000)])
    field_buzz_reference = models.CharField(max_length=256, blank=True, null=True)
    github_project_url = models.URLField(max_length=512)
    cv_file = models.TextField(validators=[validate_cv_file_json])
    cv_file_path = models.CharField(max_length=256)
    on_spot_creation_time = models.PositiveIntegerField(null=True, blank=True)
    on_spot_update_time = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set on_spot_creation_time during the instance creation.
            self.on_spot_creation_time = unix_timestamp()
            self.on_spot_update_time = unix_timestamp()
        else:
            self.on_spot_update_time = unix_timestamp()
        super(PersonalInformation, self).save(*args, **kwargs)
