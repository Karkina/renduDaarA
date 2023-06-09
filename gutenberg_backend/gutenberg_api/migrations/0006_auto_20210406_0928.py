# Generated by Django 3.1.7 on 2021-04-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gutenberg_api', '0005_bookindexmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphJaccard',
            fields=[
                ('bookSrc', models.IntegerField(primary_key=True, serialize=False)),
                ('bookDes', models.IntegerField(default='-1')),
            ],
            options={
                'ordering': ('bookSrc',),
            },
        ),
        migrations.AlterModelOptions(
            name='bookindexmodel',
            options={'ordering': ['word', 'idBook']},
        ),
    ]
