# Generated by Django 4.1.5 on 2023-01-19 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessELO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChessPuzzles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NotataionVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vers', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChessNotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('white', models.CharField(max_length=100)),
                ('black', models.CharField(max_length=100)),
                ('site', models.URLField()),
                ('mainline', models.TextField()),
                ('opening', models.TextField()),
                ('event', models.CharField(max_length=50)),
                ('result', models.CharField(max_length=20)),
                ('avg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notation', to='api.chesselo')),
            ],
        ),
    ]