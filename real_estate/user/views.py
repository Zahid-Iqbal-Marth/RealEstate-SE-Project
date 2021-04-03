from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UpdateUserProfile, UpdateProfileDetails
from django.contrib.auth.models import User
from .models import Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cust , created= User.objects.get_or_create(username=form.cleaned_data['username'],first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],email=form.cleaned_data['email'])
            Customer.objects.create(user=cust,Type=form.cleaned_data['Type'])
            cust.set_password(form.cleaned_data['password'])
            cust.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form_U = UpdateUserProfile(request.POST, instance=request.user)
        form_P = UpdateProfileDetails(request.POST,request.FILES, instance=request.user.customer)

        if form_U.is_valid() and form_P.is_valid():
            form_U.save()
            form_P.save()
            return redirect('user-profile')

    else:
        form_U = UpdateUserProfile(instance=request.user)
        form_P = UpdateProfileDetails(instance=request.user.customer)

    context = {
        'form_U': form_U,
        'form_P': form_P
    }

    return render(request, 'user/profile.html', context)



@login_required
def delete(request):
    if request.method == 'POST':
        User.objects.get(username=request.user).delete()
        return redirect('login')
    return render(request, 'user/delete.html',)    