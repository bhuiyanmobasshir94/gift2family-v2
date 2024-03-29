# Generated by Django 2.0.13 on 2019-09-23 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190616_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentInterestRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_rate', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': 'Agent interest rate',
                'verbose_name_plural': 'Agents interest rate',
            },
        ),
    ]
