# Generated by Django 3.2.16 on 2024-02-10 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payproject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='owner',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='owner',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]