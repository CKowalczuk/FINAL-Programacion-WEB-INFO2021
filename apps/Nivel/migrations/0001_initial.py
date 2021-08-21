# Generated by Django 3.2.5 on 2021-08-21 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preguntas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.CharField(max_length=50)),
                ('rta1', models.CharField(max_length=50)),
                ('rta1_v', models.BooleanField(default=False)),
                ('rta2', models.CharField(max_length=50)),
                ('rta2_v', models.BooleanField(default=False)),
                ('rta3', models.CharField(max_length=50)),
                ('rta3_v', models.BooleanField(default=False)),
                ('categoria', models.CharField(max_length=50)),
                ('nivel', models.IntegerField()),
            ],
            options={
                'db_table': 'Preguntas',
            },
        ),
    ]
