# Generated by Django 3.1.7 on 2021-03-15 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0011_auto_20210315_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shloka',
            name='purport',
            field=models.ManyToManyField(related_name='PurportPara', to='converter.PurportPara'),
        ),
    ]
