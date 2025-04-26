from django.urls import path
from . import views
from .auth import register, login_view,logout_view,admin_list,edit_admin,delete_admin


urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    path('add-member/', views.add_member, name='add_member'),
    path('check-member/', views.check_member, name='check_member'),
    path('export-excel/', views.export_excel, name='export_excel'),
    #auth
    path('register/', register, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('admins/', admin_list, name='admin_list'),
    path('admins/edit/<int:user_id>/', edit_admin, name='edit_admin'),
    path('admins/delete/<int:user_id>/', delete_admin, name='delete_admin'),
    # Commission Members
    path('commission-members/', views.CommissionMemberListView.as_view(), name='commission_member_list'),
    path('commission-members/create/', views.commission_member_create, name='commission_member_create'),
    path('commission-members/<int:pk>/update/', views.commission_member_update, name='commission_member_update'),
    path('commission-members/<int:pk>/delete/', views.commission_member_delete, name='commission_member_delete'),
    path('commission-members/export/excel/', views.export_commission_members_excel, name='export_commission_members_excel'),
    path('commission-members/export/pdf/', views.export_commission_members_pdf, name='export_commission_members_pdf'),
    
    # Election Districts
    path('districts/', views.ElectionDistrictListView.as_view(), name='election_district_list'),
    path('districts/create/', views.election_district_create, name='election_district_create'),
    path('districts/<int:pk>/update/', views.election_district_update, name='election_district_update'),
    path('districts/<int:pk>/delete/', views.election_district_delete, name='election_district_delete'),
    path('districts/export/excel/', views.export_districts_excel, name='export_districts_excel'),
    
    # Representatives
    path('representatives/', views.RepresentativeListView.as_view(), name='representative_list'),
    path('representatives/create/', views.representative_create, name='representative_create'),
    path('representatives/<int:pk>/update/', views.representative_update, name='representative_update'),
    path('representatives/<int:pk>/delete/', views.representative_delete, name='representative_delete'),
    path('representatives/export/excel/', views.export_representatives_excel, name='export_representatives_excel'),
    path('representatives/export/pdf/', views.export_representatives_pdf, name='export_representatives_pdf'),
    
    # Observers
    path('observers/', views.ObserverListView.as_view(), name='observer_list'),
    path('observers/create/', views.observer_create, name='observer_create'),
    path('observers/<int:pk>/update/', views.observer_update, name='observer_update'),
    path('observers/<int:pk>/delete/', views.observer_delete, name='observer_delete'),
    path('observers/export/excel/', views.export_observers_excel, name='export_observers_excel'),
    path('observers/export/pdf/', views.export_observers_pdf, name='export_observers_pdf'),
]
