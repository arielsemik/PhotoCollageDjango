# Generated by Django 4.0.6 on 2022-07-23 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CollageMaker", "0003_alter_image_iitem_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Collage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("collage", models.ImageField(upload_to="images/collages")),
            ],
        ),
    ]
