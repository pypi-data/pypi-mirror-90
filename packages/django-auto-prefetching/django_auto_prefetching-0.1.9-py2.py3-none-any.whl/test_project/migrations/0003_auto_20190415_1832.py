# Generated by Django 2.2 on 2019-04-15 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("test_project", "0002_childb_childb_text")]

    operations = [
        migrations.AddField(
            model_name="childabro",
            name="brother_text",
            field=models.TextField(default="sfdf"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="childabro",
            name="sibling",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="brother",
                to="test_project.ChildA",
            ),
        ),
    ]
