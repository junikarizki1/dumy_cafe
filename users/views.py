from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Akun berhasil dibuat untuk {username}! Silakan login.")
            return redirect('users:login') # Arahkan ke halaman login setelah registrasi
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})