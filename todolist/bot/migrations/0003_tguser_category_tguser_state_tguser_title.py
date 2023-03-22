# Generated by Django 4.1.7 on 2023-03-22 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0013_alter_goalcategory_board'),
        ('bot', '0002_rename_telegram_chat_id_tguser_chat_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='goals.goalcategory'),
        ),
        migrations.AddField(
            model_name='tguser',
            name='state',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tguser',
            name='title',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
