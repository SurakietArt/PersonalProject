# Generated by Django 3.2.7 on 2022-01-21 03:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='Update_By_ID',
            field=models.CharField(default=django.utils.timezone.now, max_length=127),
            preserve_default=False,
        ),
    ]
