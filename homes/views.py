from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from appliances.models import Appliance
from homes.models import Home


@login_required
def home_list_view(request):
    homes = Home.objects.filter(user=request.user)
    return render(request, 'homes/home_list.html', {'homes': homes})


@login_required
def home_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if not name:
            messages.error(request, 'Home name is required.')
            return render(request, 'homes/home_form.html', {'name': name, 'description': description})
        Home.objects.create(user=request.user, name=name, description=description)
        messages.success(request, 'Home created successfully.')
        return redirect('home_list')
    return render(request, 'homes/home_form.html')


@login_required
def home_detail_view(request, pk):
    home = get_object_or_404(Home, pk=pk, user=request.user)
    appliances = Appliance.objects.filter(home=home, is_active=True)
    return render(request, 'homes/home_detail.html', {'home': home, 'appliances': appliances})


@login_required
def home_update_view(request, pk):
    home = get_object_or_404(Home, pk=pk, user=request.user)
    if request.method == 'POST':
        home.name = request.POST.get('name', home.name).strip()
        home.description = request.POST.get('description', home.description).strip()
        if not home.name:
            messages.error(request, 'Home name is required.')
            return render(request, 'homes/home_form.html', {'home': home})
        home.save()
        messages.success(request, 'Home updated.')
        return redirect('home_detail', pk=home.pk)
    return render(request, 'homes/home_form.html', {'home': home})


@login_required
def home_delete_view(request, pk):
    home = get_object_or_404(Home, pk=pk, user=request.user)
    if request.method == 'POST':
        home.delete()
        messages.success(request, 'Home deleted.')
        return redirect('home_list')
    return render(request, 'homes/home_confirm_delete.html', {'home': home})
