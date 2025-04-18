from django.db import models
from django.utils.translation import gettext_lazy as _

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
    city_name = models.CharField(_("Shahar (tuman) nomi"), max_length=100)
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