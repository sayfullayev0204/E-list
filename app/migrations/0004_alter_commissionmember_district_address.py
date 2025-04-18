# Generated by Django 5.1.6 on 2025-04-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commissionmember',
            name='district_address',
            field=models.CharField(choices=[('qarshi_shaxri', 'Qarshi shahri'), ('shahrisabz_shaxri', 'Shahrisabz shahri'), ('shahrisabz_tumani', 'Shahrisabz tumani'), ('guzor_tumani', 'Guzor tumani'), ('dehqonobod_tumani', 'Dehqonobod tumani'), ('qamashi_tumani', 'Qamashi tumani'), ('qarshi_tumani', 'Qarshi tumani'), ('kasbi_tumani', 'Kasbi tumani'), ('kitob_tumani', 'Kitob tumani'), ('koson_tumani', 'Koson tumani'), ('mirishkor_tumani', 'Mirishkor tumani'), ('muborak_tumani', 'Muborak tumani'), ('nishon_tumani', 'Nishon tumani'), ('kokdala tumani', "Ko'kdala tumani"), ('chiroqchi tumani', 'Chiroqchi tumani'), ('yakkabog_tumani', "Yakkabog' tumani")], max_length=255, verbose_name='Tuman (shahar) manzili'),
        ),
    ]
