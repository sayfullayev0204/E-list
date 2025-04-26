from django import forms
from .models import ElectionDistrict, CommissionMember, Representative, Observer

class ElectionDistrictForm(forms.ModelForm):
    class Meta:
        model = ElectionDistrict
        fields = ['city_name', 'district_number', 'address', 'boundaries']
        widgets = {
            'boundaries': forms.Textarea(attrs={'rows': 4}),
        }

class CommissionMemberForm(forms.ModelForm):
    birth_date = forms.DateField(
        label=("Tug'ilgan sanasi"),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d',
        ),
        input_formats=['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y'],
    )
    
    age = forms.IntegerField(
        label=("Yoshi"),
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control',
        })
    )

    class Meta:
        model = CommissionMember
        fields = [
            'district', 'membership_role', 'full_name', 'photo',
            'birth_date', 'age', 'birth_place', 'nationality', 'education', 
            'district_address', 'specialization', 'workplace', 'phone_number', 'gender'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control phone-mask'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.birth_date:
            # Calculate age when form loads
            from datetime import date
            today = date.today()
            bd = self.instance.birth_date
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
            self.initial['age'] = age

class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = Representative
        fields = ['party_name', 'city_council', 'full_name', 'workplace']

class ObserverForm(forms.ModelForm):
    class Meta:
        model = Observer
        fields = ['party_name', 'district', 'full_name', 'workplace']

from django import forms
from .models import Member, District

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'district', 'participation_status',
            'activity_field', 'specialization', 'nationality', 'education',
            'birth_date', 'gender', 'is_disabled', 'is_it_specialist',
            'is_retired', 'position', 'knows_russian', 'knows_english','participation_status'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MemberCheckForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="Ism")
    last_name = forms.CharField(max_length=100, label="Familiya")
    district = forms.ModelChoiceField(queryset=District.objects.all(), label="Hudud", required=False)

