# Generated by Django 4.1.5 on 2023-01-18 11:56

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_alter_post_cropping_thumb"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="level",
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="lft",
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children",
                to="blog.category",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="rght",
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="tree_id",
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="post",
            name="category",
            field=mptt.fields.TreeForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="posts",
                to="blog.category",
                verbose_name="Категория",
            ),
        ),
    ]
