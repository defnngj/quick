# Generated by Django 3.2.10 on 2022-01-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0006_auto_20211016_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testresult',
            options={'ordering': ['-create_time']},
        ),
        migrations.AddField(
            model_name='module',
            name='parent_id',
            field=models.IntegerField(default=0, verbose_name='父级ID'),
        ),
    ]
