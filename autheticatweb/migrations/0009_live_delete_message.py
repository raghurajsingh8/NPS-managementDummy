# Generated by Django 5.0.3 on 2024-04-05 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autheticatweb', '0008_message_delete_livechat'),
    ]

    operations = [
        migrations.CreateModel(
            name='live',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
