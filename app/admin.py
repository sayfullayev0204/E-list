from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import ElectionDistrict, CommissionMember, Representative, Observer
from django.utils.translation import gettext_lazy as _
from .auth import UserProfile

admin.site.register(UserProfile)

@admin.register(ElectionDistrict)
class ElectionDistrictAdmin(ModelAdmin):
    list_display = ['district_number', 'city_name', 'address', 'created_at']
    list_filter = ['city_name', 'created_at']
    search_fields = ['district_number', 'city_name', 'address']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('city_name', 'district_number', 'address', 'boundaries')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['district_number']
    unfold = {
        'list_layout': 'table',  # Use table layout for list view
        'list_per_page': 20,
    }

    @display(description=_("Saylov uchastkasi"))
    def get_district_info(self, obj):
        return f"{obj.district_number} - {obj.city_name}"

@admin.register(CommissionMember)
class CommissionMemberAdmin(ModelAdmin):
    list_display = ['full_name', 'district', 'membership_role', 'gender', 'age', 'created_at']
    list_filter = ['district__city_name', 'gender', 'district_address', 'created_at']
    search_fields = ['full_name', 'membership_role', 'district__district_number', 'district__city_name']
    readonly_fields = ['created_at', 'updated_at', 'age']
    fieldsets = (
        (None, {
            'fields': ('district', 'membership_role', 'full_name', 'photo', 'gender')
        }),
        (_('Personal Information'), {
            'fields': ('birth_date', 'birth_place', 'district_address', 'nationality')
        }),
        (_('Professional Information'), {
            'fields': ('education', 'specialization', 'workplace', 'phone_number')
        }),
        (_('Computed Fields'), {
            'fields': ('age',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_select_related = ['district']
    ordering = ['district', 'full_name']
    unfold = {
        'list_layout': 'table',
        'list_per_page': 20,
        'image_field': 'photo',  # Display photo in list view if available
    }

    @display(description=_("A'zo ma'lumotlari"))
    def get_member_info(self, obj):
        return f"{obj.full_name} ({obj.district.city_name})"

@admin.register(Representative)
class RepresentativeAdmin(ModelAdmin):
    list_display = ['full_name', 'party_name', 'city_council', 'created_at']
    list_filter = ['party_name', 'city_council', 'created_at']
    search_fields = ['full_name', 'party_name', 'city_council']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('party_name', 'city_council', 'full_name', 'workplace')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['party_name', 'full_name']
    unfold = {
        'list_layout': 'table',
        'list_per_page': 20,
    }

    @display(description=_("Vakil ma'lumotlari"))
    def get_representative_info(self, obj):
        return f"{obj.full_name} - {obj.get_party_name_display()}"

@admin.register(Observer)
class ObserverAdmin(ModelAdmin):
    list_display = ['full_name', 'party_name', 'district', 'created_at']
    list_filter = ['party_name', 'district__city_name', 'created_at']
    search_fields = ['full_name', 'party_name', 'district__district_number', 'district__city_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('party_name', 'district', 'full_name', 'workplace')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_select_related = ['district']
    ordering = ['district', 'full_name']
    unfold = {
        'list_layout': 'table',
        'list_per_page': 20,
    }

    @display(description=_("Kuzatuvchi ma'lumotlari"))
    def get_observer_info(self, obj):
        return f"{obj.full_name} - {obj.get_party_name_display()}"
from django.contrib import admin
from .models import District, Member, DistrictStats

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'district', 'specialization', 'nationality', 'education', 'gender')
    list_filter = ('district', 'specialization', 'nationality', 'education', 'gender', 'is_disabled', 'is_it_specialist', 'is_retired')
    search_fields = ('first_name', 'last_name')
    date_hierarchy = 'created_at'

@admin.register(DistrictStats)
class DistrictStatsAdmin(admin.ModelAdmin):
    list_display = ('district', 'registered_voters', 'total_voters', 'percentage', 'updated_at')
    list_filter = ('district',)
    readonly_fields = ('updated_at',)    

