# Generated by Django 4.1.5 on 2023-01-12 14:47

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_profile_cropping_alter_profile_image"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="cropping",),
        migrations.AddField(
            model_name="profile",
            name="cropping_avatar",
            field=image_cropping.fields.ImageRatioField(
                "image",
                "300x300",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=False,
                help_text=None,
                hide_image_field=False,
                size_warning=True,
                verbose_name="cropping avatar",
            ),
        ),
    ]
