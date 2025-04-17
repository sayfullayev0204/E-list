import django_filters
from django import forms
from .models import ElectionDistrict, CommissionMember, Representative, Observer

class ElectionDistrictFilter(django_filters.FilterSet):
    city_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Shahar (tuman) nomi",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    district_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Saylov uchastkasi raqami",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ElectionDistrict
        fields = ['city_name', 'district_number']

class CommissionMemberFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="F.I.Sh.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=ElectionDistrict.objects.all(),
        label="Uchastka",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nationality = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Millati",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = django_filters.ChoiceFilter(
        choices=[('male', 'Erkak'), ('female', 'Ayol')],
        label="Jinsi",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CommissionMember
        fields = ['full_name', 'district', 'nationality', 'gender']

class RepresentativeFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="F.I.Sh.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city_council = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Tuman (shahar) kengashi",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    party_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Partiya nomi",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Representative
        fields = ['full_name', 'party_name', 'city_council']

class ObserverFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="F.I.Sh.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=ElectionDistrict.objects.all(),
        label="Uchastka",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    party_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Partiya nomi",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Observer
        fields = ['full_name', 'party_name', 'district']