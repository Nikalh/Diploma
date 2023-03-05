# Generated by Django 4.1.7 on 2023-02-26 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0009_remove_goalcomment_is_deleted_goalcomment_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goalcomment',
            old_name='content',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='goalcomment',
            name='title',
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='goals.goal'),
        ),
    ]
