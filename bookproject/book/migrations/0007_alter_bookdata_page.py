# Generated by Django 5.1.1 on 2024-10-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0006_alter_bookdata_page"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookdata",
            name="page",
            field=models.IntegerField(blank=True, null=True, verbose_name="ページ数"),
        ),
    ]
