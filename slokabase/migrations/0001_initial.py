# Generated by Django 3.1.7 on 2021-04-03 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shloka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('canto', models.IntegerField(null=True)),
                ('chapter', models.IntegerField()),
                ('number', models.CharField(max_length=10)),
                ('w2w', models.CharField(max_length=200)),
                ('translation', models.CharField(max_length=200)),
                ('purport', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ParentTheme', to='slokabase.theme')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('shloka', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='slokabase.shloka')),
                ('tag', models.ManyToManyField(to='slokabase.Theme')),
            ],
        ),
    ]
