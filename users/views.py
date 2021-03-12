from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'you`re account created {username}! please login')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    return render(request, 'users/profile.html')

@login_required
def update_profile(request):
    if request.method=='POST':
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'your profile was updated')
            return redirect('profile')
    else:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'users/update_profile.html',context)