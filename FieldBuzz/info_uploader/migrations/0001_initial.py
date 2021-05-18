# Generated by Django 3.1.4 on 2020-12-11 03:29

import django.core.validators
from django.db import migrations, models
import info_uploader.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=256)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.PositiveIntegerField()),
                ('updated_at', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tsync_id', models.CharField(default=info_uploader.models.random_unique_string, max_length=55)),
                ('name', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=256)),
                ('phone', models.CharField(max_length=14)),
                ('full_address', models.CharField(max_length=512)),
                ('graduation_year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2015), django.core.validators.MaxValueValidator(2020)])),
                ('cgpa', models.FloatField(validators=[django.core.validators.MinValueValidator(2.0), django.core.validators.MaxValueValidator(4.0)])),
                ('experience_in_months', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('current_work_place_name', models.CharField(max_length=256)),
                ('applying_in', models.IntegerField(choices=[(1, 'Mobile'), (2, 'Backend')])),
                ('expected_salary', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(15000), django.core.validators.MaxValueValidator(60000)])),
                ('field_buzz_reference', models.CharField(max_length=256)),
                ('github_project_url', models.URLField(max_length=512)),
                ('cv_file', models.TextField(validators=[info_uploader.models.validate_cv_file_json])),
                ('on_spot_creation_time', models.PositiveIntegerField()),
                ('on_spot_update_time', models.PositiveIntegerField()),
            ],
        ),
    ]
