# Generated by Django 5.0.2 on 2024-02-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lentapp", "0005_alter_itemowner_contact_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemlend",
            name="time_return",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
