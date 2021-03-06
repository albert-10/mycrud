# Generated by Django 3.0.3 on 2020-05-07 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('nummeroIdentidad', models.CharField(max_length=11)),
                ('nota', models.IntegerField(choices=[(2, 2), (3, 3), (4, 4), (5, 5)], max_length=1)),
                ('numeroTelefono', models.IntegerField(max_length=10)),
            ],
        ),
    ]
