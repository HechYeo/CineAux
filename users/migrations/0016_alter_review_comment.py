# Generated by Django 5.1.6 on 2025-03-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]
