from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Advertisement, AdvertisementImage
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    AdvertisementForm,
    AdvertisementImageForm
)


def main(request):
    ads = Advertisement.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'main/base_logged.html', {'ads': ads})


def base_logged(request):
    ads = Advertisement.objects.filter(status='approved').order_by('-created_at')
    return render(request, "main/base_logged.html", {'ads': ads})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('base-logged')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'main/profile.html')


@login_required
def settings_view(request):
    return render(request, 'main/settings.html')


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    applications = Advertisement.objects.filter(status='pending').order_by('-created_at')

    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')
        action = request.POST.get('action')
        reason = request.POST.get('reason', '').strip()

        if not ad_id:
            messages.error(request, "Не указан ID объявления.")
            return redirect('admin_dashboard')

        try:
            ad = Advertisement.objects.get(id=ad_id, status='pending')
        except Advertisement.DoesNotExist:
            messages.error(request, "Объявление не найдено или уже обработано.")
            return redirect('admin_dashboard')

        if action == 'approve':
            ad.status = 'approved'
            ad.rejection_reason = ''
            ad.save()
            messages.success(request, f"Объявление '{ad.title}' одобрено.")
        elif action == 'reject':
            if not reason:
                messages.error(request, "Для отклонения нужно указать причину.")
                return redirect('admin_dashboard')

            ad.status = 'rejected'
            ad.rejection_reason = reason
            ad.save()
            messages.success(request, f"Объявление '{ad.title}' отклонено с причиной: {reason}")
        else:
            messages.error(request, "Неизвестное действие.")
            return redirect('admin_dashboard')

        return redirect('admin_dashboard')

    return render(request, 'main/admin_dashboard.html', {'applications': applications})


def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        image_form = AdvertisementImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()

            if image_form.cleaned_data.get('image'):
                image = image_form.save(commit=False)
                image.advertisement = ad
                image.save()

            return redirect('home')
    else:
        form = AdvertisementForm()
        image_form = AdvertisementImageForm()

    return render(request, 'main/add_advertisement.html', {'form': form, 'image_form': image_form})


def advertisement_list(request):
    ads = Advertisement.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'main/advertisement_list.html', {'ads': ads})


def advertisement_detail(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id, status='approved')
    return render(request, 'main/advertisement_detail.html', {'ad': ad})
