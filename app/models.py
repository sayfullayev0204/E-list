from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="Hudud nomi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Hudud"
        verbose_name_plural = "Hududlar"
# Political party choices
PARTY_CHOICES = [
    ('adolat', 'Ozbekiston Adolat sotsial-demokratik partiyasi'),
    ('ekologik', 'Ozbekiston Ekologik partiyasi'),
    ('liberal', 'Ozbekiston Liberal demokratik partiyasi'),
    ('xalq', 'Ozbekiston Xalq demokratik partiyasi'),
    ('milliy', 'Ozbekiston Milliy tiklanish demokratik partiyasi'),
]

DISTRICT_CHOICES = [
    ('qarshi_shaxri', 'Qarshi shahri'),
    ('shahrisabz_shaxri', 'Shahrisabz shahri'),
    ('shahrisabz_tumani', 'Shahrisabz tumani'),
    ('guzor_tumani', 'Guzor tumani'),
    ('dehqonobod_tumani', 'Dehqonobod tumani'),
    ('qamashi_tumani', 'Qamashi tumani'),
    ('qarshi_tumani', 'Qarshi tumani'),
    ('kasbi_tumani', 'Kasbi tumani'),
    ('kitob_tumani', 'Kitob tumani'),
    ('koson_tumani', 'Koson tumani'),
    ('mirishkor_tumani', 'Mirishkor tumani'),
    ('muborak_tumani', 'Muborak tumani'),
    ('nishon_tumani', 'Nishon tumani'),
    ('kokdala tumani', 'Ko\'kdala tumani'),
    ('chiroqchi tumani', 'Chiroqchi tumani'),
    ('yakkabog_tumani', 'Yakkabog\' tumani'),

]

# Gender choices
GENDER_CHOICES = [
    ('male', _('Erkak')),
    ('female', _('Ayol')),
]

class ElectionDistrict(models.Model):
    """Model for election districts (Saylov uchastkalari)"""
    city_name = models.ForeignKey(District, on_delete=models.CASCADE, related_name='precincts')
    district_number = models.CharField(_("Saylov uchastkasi raqami"), max_length=20)
    address = models.CharField(_("Saylov uchastkasi manzili"), max_length=255)
    boundaries = models.TextField(_("Saylov uchastkasi chegaralari"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Saylov uchastkasi")
        verbose_name_plural = _("Saylov uchastkalari")
        ordering = ['district_number']

    def __str__(self):
        return f"{self.district_number} - {self.city_name}"

class CommissionMember(models.Model):
    """Model for commission members (USK A'zolari)"""
    district = models.ForeignKey(
        ElectionDistrict, 
        on_delete=models.CASCADE, 
        related_name='members',
        verbose_name=_("Uchastka raqami")
    )
    membership_role = models.CharField(_("A'zoligi"), max_length=100)
    full_name = models.CharField(_("F.I.Sh."), max_length=255)
    photo = models.ImageField(_("Rasmi"), upload_to='member_photos/', blank=True, null=True)
    birth_date = models.DateField(_("Tug'ilgan sanasi"))
    birth_place = models.CharField(_("Tug'ilgan joyi"), max_length=255)
    district_address = models.CharField(_("Tuman (shahar) manzili"), max_length=255, choices=DISTRICT_CHOICES)
    nationality = models.CharField(_("Millati"), max_length=100)
    education = models.CharField(_("Ma'lumoti"), max_length=255)
    specialization = models.CharField(_("Mutaxassisligi"), max_length=255)
    workplace = models.CharField(_("Ish joyi va lavozimi"), max_length=255)
    phone_number = models.CharField(_("Telefon raqami"), max_length=20)
    gender = models.CharField(_("Jinsi"), max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(_("Yoshi"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("USK A'zosi")
        verbose_name_plural = _("USK A'zolari")
        ordering = ['district', 'full_name']

    def __str__(self):
        return f"{self.full_name} - {self.district}"
    
    def save(self, *args, **kwargs):
        # Calculate age if birth_date is provided
        if self.birth_date:
            from datetime import date
            today = date.today()
            self.age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        super().save(*args, **kwargs)

class Representative(models.Model):
    """Model for authorized representatives (Vakolatli vakillar)"""
    party_name = models.CharField(_("Siyosiy partiya nomi"), max_length=100, choices=PARTY_CHOICES)
    city_council = models.CharField(_("Tuman (shahar) kengashi"), max_length=100)
    full_name = models.CharField(_("F.I.Sh."), max_length=255)
    workplace = models.CharField(_("Ish joyi va lavozimi"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Vakolatli vakil")
        verbose_name_plural = _("Vakolatli vakillar")
        ordering = ['party_name', 'full_name']

    def __str__(self):
        return f"{self.full_name} - {self.get_party_name_display()}"

class Observer(models.Model):
    """Model for observers (Kuzatuvchilar)"""
    party_name = models.CharField(_("Siyosiy partiya nomi"), max_length=100, choices=PARTY_CHOICES)
    district = models.ForeignKey(
        ElectionDistrict, 
        on_delete=models.CASCADE, 
        related_name='observers',
        verbose_name=_("Saylov uchastkasi raqami")
    )
    full_name = models.CharField(_("F.I.Sh."), max_length=255)
    workplace = models.CharField(_("Ish joyi va lavozimi"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Kuzatuvchi")
        verbose_name_plural = _("Kuzatuvchilar")
        ordering = ['district', 'full_name']

    def __str__(self):
        return f"{self.full_name} - {self.get_party_name_display()}"
    


class Member(models.Model):
    # Basic information
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='members', verbose_name="Hudud")
    
    # Status
    PARTICIPATION_CHOICES = [
        ('participated', 'Avval qatnashgan'),
        ('not_participated', 'Avval qatnashmagan'),
    ]
    participation_status = models.CharField(max_length=20, choices=PARTICIPATION_CHOICES, verbose_name="Qatnashish holati")
    
    # Activity field
    ACTIVITY_FIELD_CHOICES = [
        ('public_education', 'Xalq ta\'limi tizimi hodimi'),
        ('higher_education', 'Oliy ta\'lim tizimi hodimi'),
        ('government', 'Boshqa davlat boshqaruvlari va muassasalar xodimlari'),
        ('self_governance', 'O\'zini o\'zi boshqarish organi vakillari'),
        ('ngo', 'Nodavlat notijorat tashkilotlar xodimlari'),
        ('private_sector', 'Boshqa nodavlat mavjudligi sohasi vakillari'),
        ('unemployed', 'Vaqtcha ishsizlar'),
    ]
    activity_field = models.CharField(max_length=30, choices=ACTIVITY_FIELD_CHOICES, verbose_name="Faoliyat sohasi")
    
    # Specialization
    SPECIALIZATION_CHOICES = [
        ('teacher', 'O\'qituvchi'),
        ('doctor', 'Shifokor'),
        ('engineer', 'Muhandis'),
        ('economist', 'Iqtisodchi'),
        ('journalist', 'Jurnalist'),
        ('lawyer', 'Huquqshunos'),
        ('agriculture', 'Qishloq xo\'jaligi'),
        ('other', 'Boshqa'),
    ]
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, verbose_name="Mutaxassisligi")
    
    # Nationality
    NATIONALITY_CHOICES = [
        ('uzbek', 'O\'zbek'),
        ('karakalpak', 'Qoraqalpoq'),
        ('kazakh', 'Qozoq'),
        ('russian', 'Rus'),
        ('tajik', 'Tojik'),
        ('korean', 'Koreys'),
        ('other', 'Boshqa'),
    ]
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES, verbose_name="Millati")
    
    # Education
    EDUCATION_CHOICES = [
        ('higher', 'Oliy'),
        ('secondary_special', 'O\'rta maxsus'),
        ('secondary', 'O\'rta'),
    ]
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name="Ma'lumoti")
    
    # Age
    birth_date = models.DateField(verbose_name="Tug'ilgan sana")
    
    # Gender
    GENDER_CHOICES = [
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Jinsi")
    
    # Additional fields
    is_disabled = models.BooleanField(default=False, verbose_name="Nogironligi tegishli shaxs")
    is_it_specialist = models.BooleanField(default=False, verbose_name="Axborot-kommunikatsiya texnologiyalari yaratish")
    is_retired = models.BooleanField(default=False, verbose_name="Nafaqadagi")
    
    # Position (for women statistics)
    POSITION_CHOICES = [
        ('none', 'Yo\'q'),
        ('chairman', 'Rais'),
        ('deputy', 'Rais o\'rinbosari'),
        ('secretary', 'Kotib'),
    ]
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='none', verbose_name="Lavozimi")
    
    # Language proficiency
    knows_russian = models.BooleanField(default=False, verbose_name="Mukammal rus tilini biladi")
    knows_english = models.BooleanField(default=False, verbose_name="Mukammal ingliz tilini biladi")
    
    # Registration date
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatga olingan sana")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age
    
    class Meta:
        verbose_name = "A'zo"
        verbose_name_plural = "A'zolar"

class DistrictStats(models.Model):
    """
    This model stores pre-calculated statistics for each district
    """
    district = models.OneToOneField(District, on_delete=models.CASCADE, related_name='stats')
    district_count = models.IntegerField(default=0, verbose_name="Uchastkalar soni")
    registered_voters = models.IntegerField(default=0, verbose_name="Ro'yxatga olingan saylovchilar soni")
    total_voters = models.IntegerField(default=0, verbose_name="Jami ovoz berganlar")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Foiz")
    cancelled_ballots = models.IntegerField(default=0, verbose_name="Bekor qilingan byulletenlar")
    
    # Activity hours statistics
    activity_8 = models.IntegerField(default=0)
    activity_10 = models.IntegerField(default=0)
    activity_12 = models.IntegerField(default=0)
    activity_14 = models.IntegerField(default=0)
    activity_16 = models.IntegerField(default=0)
    activity_18 = models.IntegerField(default=0)
    activity_19 = models.IntegerField(default=0)
    activity_20 = models.IntegerField(default=0)
    activity_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Specialization counts
    teacher_count = models.IntegerField(default=0)
    doctor_count = models.IntegerField(default=0)
    engineer_count = models.IntegerField(default=0)
    economist_count = models.IntegerField(default=0)
    lawyer_count = models.IntegerField(default=0)
    agriculture_count = models.IntegerField(default=0)
    other_specialization_count = models.IntegerField(default=0)
    total_specialization_count = models.IntegerField(default=0)
    
    # Nationality counts
    uzbek_count = models.IntegerField(default=0)
    other_nationality_count = models.IntegerField(default=0)
    
    # Education counts
    higher_education_count = models.IntegerField(default=0)
    secondary_education_count = models.IntegerField(default=0)
    
    # Age group counts
    age_21_30_count = models.IntegerField(default=0)
    age_31_40_count = models.IntegerField(default=0)
    age_41_50_count = models.IntegerField(default=0)
    age_51_60_count = models.IntegerField(default=0)
    age_above_60_count = models.IntegerField(default=0)
    
    # Gender counts
    male_count = models.IntegerField(default=0)
    female_count = models.IntegerField(default=0)
    
    # Women in positions
    female_chairman_count = models.IntegerField(default=0)
    female_deputy_count = models.IntegerField(default=0)
    female_secretary_count = models.IntegerField(default=0)
    
    # Other counts
    disabled_count = models.IntegerField(default=0)
    it_specialist_count = models.IntegerField(default=0)
    retired_count = models.IntegerField(default=0)
    
    # Language proficiency
    russian_speakers_count = models.IntegerField(default=0)
    english_speakers_count = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats for {self.district.name}"
    
    class Meta:
        verbose_name = "Hudud statistikasi"
        verbose_name_plural = "Hududlar statistikasi"
