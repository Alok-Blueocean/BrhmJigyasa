# Generated by Django 3.1.7 on 2021-03-16 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0012_auto_20210315_1158'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('para', 'number'), name='unique question of the para'),
        ),
    ]
