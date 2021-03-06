# Generated by Django 2.2.13 on 2020-06-25 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_post_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile-pic-default.jpg', upload_to='profile_pics')),
                ('banner_image', models.ImageField(default='slider-1.jpg', upload_to='banner')),
                ('job_title', models.CharField(max_length=100)),
                ('bio', models.CharField(help_text='Short Bio (eg. I love cats and games)', max_length=100)),
                ('address', models.CharField(help_text='Enter Your Address', max_length=100)),
                ('city', models.CharField(help_text='Enter Your City', max_length=100)),
                ('country', models.CharField(help_text='Enter Your Country', max_length=100)),
                ('zip_code', models.CharField(help_text='Enter Your Zip Code', max_length=100)),
                ('twitter_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('instagram_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('facebook_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('github_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=250, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
