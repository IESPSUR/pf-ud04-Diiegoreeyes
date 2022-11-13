# Generated by Django 4.1.3 on 2022-11-13 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.CharField(max_length=200)),
                ('importe', models.CharField(max_length=200)),
                ('fecha', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='marca',
            fields=[
                ('nombre', models.CharField(max_length=200, primary_key='true', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('modelo', models.CharField(max_length=200)),
                ('unidades', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('detalles', models.CharField(max_length=200)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.marca')),
            ],
        ),
    ]
