from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        
        # Foydalanuvchi yaratish
        user = User.objects.create_user(username=username, password=password, first_name=name)
        user.save()
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Foydalanuvchi autentifikatsiyasi
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Muvaffaqiyatli login bo'lsa home sahifasiga yo'naltirish
        else:
            return HttpResponse("Noto'g'ri username yoki password")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')