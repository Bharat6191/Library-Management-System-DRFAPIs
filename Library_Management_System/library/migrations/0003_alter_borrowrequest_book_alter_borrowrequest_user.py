# Generated by Django 5.1.4 on 2024-12-13 13:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_rename_borrow_end_date_borrowrequest_date_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrequest',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_requests', to='library.book'),
        ),
        migrations.AlterField(
            model_name='borrowrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]