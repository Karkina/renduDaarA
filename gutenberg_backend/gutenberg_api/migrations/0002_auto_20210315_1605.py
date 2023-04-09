# Generated by Django 3.1.5 on 2021-03-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gutenberg_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indexlivre',
            options={'ordering': ['language']},
        ),
        migrations.RemoveField(
            model_name='indexlivre',
            name='idLivre',
        ),
        migrations.RemoveField(
            model_name='indexlivre',
            name='word',
        ),
        migrations.AddField(
            model_name='indexlivre',
            name='author',
            field=models.TextField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='indexlivre',
            name='coverBook',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='indexlivre',
            name='language',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='indexlivre',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='indexlivre',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='indexlivre',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]