# Generated by Django 4.1.7 on 2023-03-12 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_tq_user_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tguser',
            old_name='telegram_chat_id',
            new_name='chat_id',
        ),
        migrations.RenameField(
            model_name='tguser',
            old_name='verification',
            new_name='verification_code',
        ),
    ]
