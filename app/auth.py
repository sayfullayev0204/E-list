from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.db import models

# Custom User Profile model to store role
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('usk', 'USK Azolari'),
        ('uchastka', 'Saylov uchastkasi'),
        ('vakolatli', 'Vakolatli vakil'),
        ('kuzatuvchi','Kuzatuvchi')

    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        role = request.POST['role']  # Role from form
        
        # Validate role
        valid_roles = [choice[0] for choice in UserProfile.ROLE_CHOICES]
        if role not in valid_roles:
            messages.error(request, "Noto'g'ri rol tanlandi.")
            return redirect('register')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud. Iltimos, boshqa nom tanlang.")
            return redirect('register')
        
        # Create user without logging them in
        user = User.objects.create_user(username=username, password=password, first_name=name)
        # Create user profile with role
        UserProfile.objects.create(user=user, role=role)
        
        # Success message and redirect without logging in the new user
        messages.success(request, "Yangi foydalanuvchi muvaffaqiyatli ro'yxatdan o'tkazildi!")
        return redirect('home')  # Redirect to home page, current user remains logged in
    
    # Pass role choices to template
    role_choices = UserProfile.ROLE_CHOICES
    return render(request, 'register.html', {"register": "register", "role_choices": role_choices})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # User authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home on successful login
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri.")
            return redirect('login')  
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')