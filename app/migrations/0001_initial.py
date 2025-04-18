# Generated by Django 5.1.6 on 2025-04-16 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=100, verbose_name='Shahar (tuman) nomi')),
                ('district_number', models.CharField(max_length=20, verbose_name='Saylov uchastkasi raqami')),
                ('address', models.CharField(max_length=255, verbose_name='Saylov uchastkasi manzili')),
                ('boundaries', models.TextField(verbose_name='Saylov uchastkasi chegaralari')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Saylov uchastkasi',
                'verbose_name_plural': 'Saylov uchastkalari',
                'ordering': ['district_number'],
            },
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party_name', models.CharField(choices=[('adolat', 'Ozbekiston Adolat sotsial-demokratik partiyasi'), ('ekologik', 'Ozbekiston Ekologik partiyasi'), ('liberal', 'Ozbekiston Liberal demokratik partiyasi'), ('xalq', 'Ozbekiston Xalq demokratik partiyasi'), ('milliy', 'Ozbekiston Milliy tiklanish demokratik partiyasi')], max_length=100, verbose_name='Siyosiy partiya nomi')),
                ('city_council', models.CharField(max_length=100, verbose_name='Tuman (shahar) kengashi')),
                ('full_name', models.CharField(max_length=255, verbose_name='F.I.Sh.')),
                ('workplace', models.CharField(max_length=255, verbose_name='Ish joyi va lavozimi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Vakolatli vakil',
                'verbose_name_plural': 'Vakolatli vakillar',
                'ordering': ['party_name', 'full_name'],
            },
        ),
        migrations.CreateModel(
            name='CommissionMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_role', models.CharField(max_length=100, verbose_name="A'zoligi")),
                ('full_name', models.CharField(max_length=255, verbose_name='F.I.Sh.')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='member_photos/', verbose_name='Rasmi')),
                ('birth_date', models.DateField(verbose_name="Tug'ilgan sanasi")),
                ('birth_place', models.CharField(max_length=255, verbose_name="Tug'ilgan joyi")),
                ('district_address', models.CharField(choices=[('qarshi_shaxri', 'Qarshi shaxri'), ('shahrisabz_tumani', 'Shahrisabz tumani'), ('guzor_tumani', 'Guzor tumani'), ('dehqonobod_tumani', 'Dehqonobod tumani'), ('qamashi_tumani', 'Qamashi tumani'), ('qarshi_tumani', 'Qarshi tumani'), ('kasbi_tumani', 'Kasbi tumani'), ('kitob_tumani', 'Kitob tumani'), ('koson_tumani', 'Koson tumani'), ('mirishkor_tumani', 'Mirishkor tumani'), ('muborak_tumani', 'Muborak tumani'), ('nishon_tumani', 'Nishon tumani'), ('kokdala tumani', "Ko'kdala tumani"), ('chiroqchi tumani', 'Chiroqchi tumani'), ('shahrisabz_shaxri', 'Shahrisabz shaxri'), ('yakkabog_tumani', "Yakkabog' tumani")], max_length=255, verbose_name='Tuman (shahar) manzili')),
                ('nationality', models.CharField(max_length=100, verbose_name='Millati')),
                ('education', models.CharField(max_length=255, verbose_name="Ma'lumoti")),
                ('specialization', models.CharField(max_length=255, verbose_name='Mutaxassisligi')),
                ('workplace', models.CharField(max_length=255, verbose_name='Ish joyi va lavozimi')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Telefon raqami')),
                ('gender', models.CharField(choices=[('male', 'Erkak'), ('female', 'Ayol')], max_length=10, verbose_name='Jinsi')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Yoshi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='app.electiondistrict', verbose_name='Uchastka raqami')),
            ],
            options={
                'verbose_name': "USK A'zosi",
                'verbose_name_plural': "USK A'zolari",
                'ordering': ['district', 'full_name'],
            },
        ),
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party_name', models.CharField(choices=[('adolat', 'Ozbekiston Adolat sotsial-demokratik partiyasi'), ('ekologik', 'Ozbekiston Ekologik partiyasi'), ('liberal', 'Ozbekiston Liberal demokratik partiyasi'), ('xalq', 'Ozbekiston Xalq demokratik partiyasi'), ('milliy', 'Ozbekiston Milliy tiklanish demokratik partiyasi')], max_length=100, verbose_name='Siyosiy partiya nomi')),
                ('full_name', models.CharField(max_length=255, verbose_name='F.I.Sh.')),
                ('workplace', models.CharField(max_length=255, verbose_name='Ish joyi va lavozimi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observers', to='app.electiondistrict', verbose_name='Saylov uchastkasi raqami')),
            ],
            options={
                'verbose_name': 'Kuzatuvchi',
                'verbose_name_plural': 'Kuzatuvchilar',
                'ordering': ['district', 'full_name'],
            },
        ),
    ]
