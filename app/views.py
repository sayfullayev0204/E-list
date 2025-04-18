from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from .models import ElectionDistrict, CommissionMember, Representative, Observer
from .forms import ElectionDistrictForm, CommissionMemberForm, RepresentativeForm, ObserverForm
from .filters import ElectionDistrictFilter, CommissionMemberFilter, RepresentativeFilter, ObserverFilter

@login_required
def home(request):
    # Get statistics for dashboard
    districts_count = ElectionDistrict.objects.count()
    members_count = CommissionMember.objects.count()
    
    # Gender statistics
    male_count = CommissionMember.objects.filter(gender='male').count()
    female_count = CommissionMember.objects.filter(gender='female').count()
    
    # Nationality statistics
    nationalities = CommissionMember.objects.values('nationality').annotate(
        count=Count('nationality')
    ).order_by('-count')[:5]
    
    # Specialization statistics
    specializations = CommissionMember.objects.values('specialization').annotate(
        count=Count('specialization')
    ).order_by('-count')[:5]
    
    # Education statistics
    educations = CommissionMember.objects.values('education').annotate(
        count=Count('education')
    ).order_by('-count')[:5]
    
    # Age groups
    age_groups = {
        'age_18_30': CommissionMember.objects.filter(age__gte=18, age__lte=30).count(),
        'age_31_45': CommissionMember.objects.filter(age__gte=31, age__lte=45).count(),
        'age_46_60': CommissionMember.objects.filter(age__gte=46, age__lte=60).count(),
        'age_60_plus': CommissionMember.objects.filter(age__gt=60).count(),
    }
    
    # Group ElectionDistrict by city_name and count the number of districts per city
    district_counts = ElectionDistrict.objects.values('city_name').annotate(
        district_count=Count('id')
    ).order_by('city_name')
    
    # Prepare data for each city_name
    district_data = []
    for district in district_counts:
        city_name = district['city_name']
        # Count related commission members and observers for all districts in this city
        commission_member_count = CommissionMember.objects.filter(district__city_name=city_name).count()
        observer_count = Observer.objects.filter(district__city_name=city_name).count()
        
        district_data.append({
            'name': city_name,
            'district_count': district['district_count'],  # Number of election districts in this city
            'commission_member_count': commission_member_count,
            'observer_count': observer_count,
            'total_count': commission_member_count + observer_count  # Total related records
        })
    
    context = {
        'districts_count': districts_count,
        'members_count': members_count,
        'male_count': male_count,
        'female_count': female_count,
        'nationalities': nationalities,
        'specializations': specializations,
        'educations': educations,
        'age_groups': age_groups,
        'district_data': district_data
    }
    
    return render(request, 'elections/home.html', context)
from .models import CommissionMember, DISTRICT_CHOICES
class CommissionMemberListView(LoginRequiredMixin,ListView):
    model = CommissionMember
    template_name = 'elections/commission_members/list.html'
    context_object_name = 'members'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CommissionMemberFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['districts'] = DISTRICT_CHOICES  # Add DISTRICT_CHOICES to context
        return context

import django_filters
from .models import CommissionMember, DISTRICT_CHOICES
from django import forms

class CommissionMemberFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr='icontains', label='F.I.Sh.',widget=forms.TextInput(attrs={'class': 'form-control'}))
    district = django_filters.ChoiceFilter(choices=DISTRICT_CHOICES, field_name='district_address', label='Tuman',widget=forms.Select(attrs={'class': 'form-control'}))
    nationality = django_filters.CharFilter(lookup_expr='icontains', label='Millati',widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = django_filters.ChoiceFilter(choices=[('male', 'Erkak'), ('female', 'Ayol')], label='Jinsi',widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CommissionMember
        fields = ['full_name', 'district', 'nationality', 'gender']
        
@login_required
def commission_member_create(request):
    if request.method == 'POST':
        form = CommissionMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "A'zo muvaffaqiyatli qo'shildi!")
            return redirect('commission_member_list')
    else:
        form = CommissionMemberForm()
    
    return render(request, 'elections/commission_members/form.html', {'form': form})

@login_required
def commission_member_update(request, pk):
    member = get_object_or_404(CommissionMember, pk=pk)
    
    if request.method == 'POST':
        form = CommissionMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "A'zo muvaffaqiyatli yangilandi!")
            return redirect('commission_member_list')
    else:
        messages.error(request, "A'zo ma'lumotlarini yangilashda xatolik yuz berdi!")
        form = CommissionMemberForm(instance=member)
    
    return render(request, 'elections/commission_members/form.html', {'form': form, 'member': member})

@login_required
def commission_member_delete(request, pk):
    member = get_object_or_404(CommissionMember, pk=pk)
    
    if request.method == 'POST':
        member.delete()
        messages.success(request, "A'zo muvaffaqiyatli o'chirildi!")
        return redirect('commission_member_list')
    
    return render(request, 'elections/commission_members/delete.html', {'member': member})

import xlsxwriter
from io import BytesIO
from PIL import Image
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from .models import CommissionMember
from django.contrib.auth.decorators import login_required

@login_required
def export_commission_members_excel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("USK A'zolari")

    # Sarlavhalar
    headers = [
        'Uchastka raqami', 'A\'zoligi', 'F.I.Sh.', 'Tug\'ilgan sanasi',
        'Tug\'ilgan joyi', 'Millati', 'Ma\'lumoti', 'Mutaxassisligi',
        'Ish joyi va lavozimi', 'Telefon raqami', 'Jinsi', 'Yoshi', 'Rasmi'
    ]

    bold = workbook.add_format({'bold': True})
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, bold)

    # Har bir ustun eni
    for col in range(len(headers) - 1):
        worksheet.set_column(col, col, 20)

    image_col = len(headers) - 1
    worksheet.set_column(image_col, image_col, 15)

    members = CommissionMember.objects.select_related('district').all()
    row_num = 1

    for member in members:
        data = [
            member.district.district_number,
            member.membership_role,
            member.full_name,
            member.birth_date.strftime('%d.%m.%Y') if member.birth_date else '',
            member.birth_place,
            member.nationality,
            member.education,
            member.specialization,
            member.workplace,
            member.phone_number,
            'Erkak' if member.gender == 'male' else 'Ayol',
            member.age or '',
        ]

        for col_num, value in enumerate(data):
            worksheet.write(row_num, col_num, value)

        worksheet.set_row(row_num, 80)  # Rasmga joy bo'lishi uchun satr balandligi

        # Rasmini tayyorlash
        if member.photo and default_storage.exists(member.photo.name):
            image_path = os.path.join(settings.MEDIA_ROOT, member.photo.name)

            # Rasmni Pillow orqali ochamiz va resize qilamiz
            try:
                with Image.open(image_path) as img:
                    # Rasmni qayta o‘lchamlash (masalan 100x100 px)
                    img = img.convert('RGB')
                    img = img.resize((100, 100))

                    # Temporarily saqlaymiz memoryga
                    temp_thumb = BytesIO()
                    img.save(temp_thumb, format='PNG')
                    temp_thumb.seek(0)

                    # Excelga joylaymiz
                    worksheet.insert_image(
                        row_num,
                        image_col,
                        member.full_name + ".png",  # unique image name
                        {
                            'image_data': temp_thumb,
                            'x_offset': 5,
                            'y_offset': 5,
                        }
                    )
            except Exception as e:
                print(f"Rasmni ochishda xatolik: {e}")

        row_num += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=commission_members.xlsx'
    return response



from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from PIL import Image as PILImage
import os

from django.conf import settings
from django.core.files.storage import default_storage
from .models import CommissionMember

@login_required
def export_commission_members_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="commission_members.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    members = CommissionMember.objects.select_related('district').all()

    for member in members:
        # Rasm tayyorlash
        img_data = None
        if member.photo and default_storage.exists(member.photo.name):
            image_path = os.path.join(settings.MEDIA_ROOT, member.photo.name)
            try:
                with PILImage.open(image_path) as img:
                    img = img.convert('RGB')
                    img = img.resize((80, 80))  # bir xil o‘lcham
                    img_buffer = BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    img_data = Image(img_buffer, width=80, height=80)
            except Exception as e:
                print(f"Rasmda xatolik: {e}")

        # Matnli ma'lumotlar
        gender = 'Erkak' if member.gender == 'male' else 'Ayol'
        text_data = [
            ['Uchastka raqami', member.district.district_number],
            ['A\'zoligi', member.membership_role],
            ['F.I.Sh.', member.full_name],
            ['Millati', member.nationality],
            ['Ma\'lumoti', member.education],
            ['Yoshi', str(member.age)],
            ['Jinsi', gender],
        ]

        table = Table(text_data, colWidths=[120, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        row = [img_data, table] if img_data else [table]
        elements.append(Table([row], colWidths=[100, 400]))
        elements.append(Spacer(1, 15))  # Har a'zo o'rtasida bo‘sh joy

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='application/pdf')


# Election Districts Views
class ElectionDistrictListView(LoginRequiredMixin,ListView):
    model = ElectionDistrict
    template_name = 'elections/districts/list.html'
    context_object_name = 'districts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ElectionDistrictFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

@login_required
def election_district_create(request):
    if request.method == 'POST':
        form = ElectionDistrictForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Saylov uchastkasi muvaffaqiyatli qo'shildi!")
            return redirect('election_district_list')
    else:
        form = ElectionDistrictForm()
    
    return render(request, 'elections/districts/form.html', {'form': form})


@login_required
def election_district_update(request, pk):
    district = get_object_or_404(ElectionDistrict, pk=pk)
    
    if request.method == 'POST':
        form = ElectionDistrictForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            messages.success(request, "Saylov uchastkasi muvaffaqiyatli yangilandi!")
            return redirect('election_district_list')
    else:
        form = ElectionDistrictForm(instance=district)
    
    return render(request, 'elections/districts/form.html', {'form': form, 'district': district})

@login_required
def election_district_delete(request, pk):
    district = get_object_or_404(ElectionDistrict, pk=pk)
    
    if request.method == 'POST':
        district.delete()
        messages.success(request, "Saylov uchastkasi muvaffaqiyatli o'chirildi!")
        return redirect('election_district_list')
    
    return render(request, 'elections/districts/delete.html', {'district': district})

@login_required
def export_districts_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="election_districts.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Saylov uchastkalari')
    
    # Sheet header
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Shahar (tuman) nomi', 'Saylov uchastkasi raqami', 'Saylov uchastkasi manzili', 'Saylov uchastkasi chegaralari']
    
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)
    
    # Sheet body
    font_style = xlwt.XFStyle()
    
    rows = ElectionDistrict.objects.all().values_list('city_name', 'district_number', 'address', 'boundaries')
    
    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value), font_style)
    
    wb.save(response)
    return response

# Representatives Views
class RepresentativeListView(LoginRequiredMixin,ListView):
    model = Representative
    template_name = 'elections/representatives/list.html'
    context_object_name = 'representatives'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepresentativeFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

@login_required
def representative_create(request):
    if request.method == 'POST':
        form = RepresentativeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vakolatli vakil muvaffaqiyatli qo'shildi!")
            return redirect('representative_list')
    else:
        form = RepresentativeForm()
    
    return render(request, 'elections/representatives/form.html', {'form': form})

@login_required
def representative_update(request, pk):
    representative = get_object_or_404(Representative, pk=pk)
    
    if request.method == 'POST':
        form = RepresentativeForm(request.POST, instance=representative)
        if form.is_valid():
            form.save()
            messages.success(request, "Vakolatli vakil muvaffaqiyatli yangilandi!")
            return redirect('representative_list')
    else:
        form = RepresentativeForm(instance=representative)
    
    return render(request, 'elections/representatives/form.html', {'form': form, 'representative': representative})

@login_required
def representative_delete(request, pk):
    representative = get_object_or_404(Representative, pk=pk)
    
    if request.method == 'POST':
        representative.delete()
        messages.success(request, "Vakolatli vakil muvaffaqiyatli o'chirildi!")
        return redirect('representative_list')
    
    return render(request, 'elections/representatives/delete.html', {'representative': representative})

# Observers Views
class ObserverListView(LoginRequiredMixin,ListView):
    model = Observer
    template_name = 'elections/observers/list.html'
    context_object_name = 'observers'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ObserverFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

@login_required
def observer_create(request):
    if request.method == 'POST':
        form = ObserverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kuzatuvchi muvaffaqiyatli qo'shildi!")
            return redirect('observer_list')
    else:
        form = ObserverForm()
    
    return render(request, 'elections/observers/form.html', {'form': form})

def export_representatives_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="representatives.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Vakolatli vakillar')
    
    # Sheet header
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Partiya', 'Tuman (shahar) kengashi', 'F.I.Sh.', 'Ish joyi va lavozimi']
    
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)
    
    # Sheet body
    font_style = xlwt.XFStyle()
    
    representatives = Representative.objects.all()
    
    for representative in representatives:
        row_num += 1
        row = [
            representative.get_party_name_display(),  # Use get_party_name_display() instead of dict lookup
            representative.city_council,
            representative.full_name,
            representative.workplace
        ]
        
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value), font_style)
    
    wb.save(response)
    return response

def export_representatives_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="representatives.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Define table data
    data = [
        ['Partiya', 'Tuman (shahar) kengashi', 'F.I.Sh.', 'Ish joyi va lavozimi']
    ]
    
    representatives = Representative.objects.all()
    for representative in representatives:
        data.append([
            representative.get_party_name_display(),  # Use get_party_name_display() instead of dict lookup
            representative.city_council,
            representative.full_name,
            representative.workplace
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response

def export_observers_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="observers.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Kuzatuvchilar')
    
    # Sheet header
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Partiya', 'Uchastka raqami', 'F.I.Sh.', 'Ish joyi va lavozimi']
    
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)
    
    # Sheet body
    font_style = xlwt.XFStyle()
    
    observers = Observer.objects.all().select_related('district')
    
    for observer in observers:
        row_num += 1
        row = [
            observer.get_party_name_display(),  # Use get_party_name_display() instead of dict lookup
            observer.district.district_number,
            observer.full_name,
            observer.workplace
        ]
        
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value), font_style)
    
    wb.save(response)
    return response

def export_observers_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="observers.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Define table data
    data = [
        ['Partiya', 'Uchastka raqami', 'F.I.Sh.', 'Ish joyi va lavozimi']
    ]
    
    observers = Observer.objects.all().select_related('district')
    for observer in observers:
        data.append([
            observer.get_party_name_display(),  # Use get_party_name_display() instead of dict lookup
            observer.district.district_number,
            observer.full_name,
            observer.workplace
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response

@login_required
def observer_update(request, pk):
    observer = get_object_or_404(Observer, pk=pk)
    
    if request.method == 'POST':
        form = ObserverForm(request.POST, instance=observer)
        if form.is_valid():
            form.save()
            messages.success(request, "Kuzatuvchi muvaffaqiyatli yangilandi!")
            return redirect('observer_list')
    else:
        form = ObserverForm(instance=observer)
    
    return render(request, 'elections/observers/form.html', {'form': form, 'observer': observer})

@login_required
def observer_delete(request, pk):
    observer = get_object_or_404(Observer, pk=pk)
    
    if request.method == 'POST':
        observer.delete()
        messages.success(request, "Kuzatuvchi muvaffaqiyatli o'chirildi!")
        return redirect('observer_list')
    
    return render(request, 'elections/observers/delete.html', {'observer': observer})
