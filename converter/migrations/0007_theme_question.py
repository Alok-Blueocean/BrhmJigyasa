# Generated by Django 3.1.7 on 2021-03-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0006_auto_20210315_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='question',
            field=models.ManyToManyField(related_name='Question', to='converter.Question'),
        ),
    ]
