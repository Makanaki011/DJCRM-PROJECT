# Generated by Django 4.1 on 2022-09-08 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_alter_category_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]
