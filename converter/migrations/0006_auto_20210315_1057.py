# Generated by Django 3.1.7 on 2021-03-15 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0005_auto_20210315_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='theme',
            field=models.ManyToManyField(related_name='Theme', to='converter.Theme'),
        ),
    ]