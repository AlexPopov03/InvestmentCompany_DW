# Generated by Django 5.0.1 on 2024-01-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_client_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='first_login',
            field=models.BooleanField(default=True, help_text='Чи закінчив користувач реєстрацію(ввів детальну інформацію про себе)'),
        ),
    ]
