# Generated by Django 4.0.6 on 2022-07-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CollageMaker', '0006_collage_name_alter_collage_collage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collage',
            name='name',
        ),
        migrations.AlterField(
            model_name='collage',
            name='collage',
            field=models.ImageField(upload_to='collagess/'),
        ),
        migrations.AlterField(
            model_name='image_iitem',
            name='image_file',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
