# Generated by Django 2.0.1 on 2019-06-04 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_auto_20190604_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='tags',
        ),
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.CharField(default='tag1', max_length=30),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
