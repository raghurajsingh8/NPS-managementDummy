# Generated by Django 5.0.3 on 2024-12-03 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autheticatweb', '0014_remove_contact_desc_contact_course_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_from', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('measurement_unit', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
                ('serial_no', models.CharField(max_length=255)),
                ('box_type', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('verified_by', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_to', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('measurement_unit', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
                ('serial_no', models.CharField(max_length=255)),
                ('box_type', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('verified_by', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
