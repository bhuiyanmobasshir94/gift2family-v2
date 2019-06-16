# Generated by Django 2.0.13 on 2019-06-16 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0005_regenerate_user_address_hashes'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='full name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text='For emergency purpose', max_length=128, verbose_name='Phone number')),
                ('nationality', models.CharField(max_length=30, verbose_name='nationality (by born)')),
                ('passport_copy', models.FileField(help_text='Scanned document', upload_to='agents/passport/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.Country', verbose_name='Present country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
            },
        ),
    ]
