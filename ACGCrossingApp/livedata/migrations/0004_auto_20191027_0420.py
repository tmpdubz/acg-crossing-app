# Generated by Django 2.2.6 on 2019-10-27 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livedata', '0003_usershift_year_in_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershift',
            name='year_in_school',
        ),
        migrations.AlterField(
            model_name='usershift',
            name='checked_in',
            field=models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior')], default='JR', max_length=2),
        ),
    ]
