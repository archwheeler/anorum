# Generated by Django 4.0.4 on 2022-05-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_forum_post_useridentity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=models.TextField(max_length=10000),
        ),
    ]