# Generated by Django 3.1.1 on 2020-09-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20200909_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='method',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Method',
        ),
    ]
