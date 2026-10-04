from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from appliances.models import Appliance
from homes.models import Home


@login_required
def appliance_list_view(request):
    home = request.user.homes.first()
    appliances = Appliance.objects.filter(home=home) if home else Appliance.objects.none()
    return render(request, 'appliances/appliance_list.html', {'appliances': appliances, 'home': home})


@login_required
def appliance_create_view(request):
    home = request.user.homes.first()
    if request.method == 'POST':
        home_id = request.POST.get('home')
        home = get_object_or_404(Home, pk=home_id, user=request.user)
        appliance = Appliance(
            home=home,
            name=request.POST.get('name', '').strip(),
            category=request.POST.get('category', 'Other'),
            power_watts=request.POST.get('power_watts', 0),
            average_hours_per_day=request.POST.get('average_hours_per_day', 0),
            days_per_period=request.POST.get('days_per_period', 30),
            quantity=request.POST.get('quantity', 1),
            standby_power_watts=request.POST.get('standby_power_watts', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        try:
            appliance.full_clean()
            appliance.save()
            messages.success(request, 'Appliance added.')
            return redirect('home_detail', pk=home.pk)
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, 'appliances/appliance_form.html', {'homes': request.user.homes.all(), 'home': home})


@login_required
def appliance_update_view(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk, home__user=request.user)
    if request.method == 'POST':
        appliance.name = request.POST.get('name', appliance.name).strip()
        appliance.category = request.POST.get('category', appliance.category)
        appliance.power_watts = request.POST.get('power_watts', appliance.power_watts)
        appliance.average_hours_per_day = request.POST.get('average_hours_per_day', appliance.average_hours_per_day)
        appliance.days_per_period = request.POST.get('days_per_period', appliance.days_per_period)
        appliance.quantity = request.POST.get('quantity', appliance.quantity)
        appliance.standby_power_watts = request.POST.get('standby_power_watts', appliance.standby_power_watts)
        appliance.is_active = request.POST.get('is_active') == 'on'
        try:
            appliance.full_clean()
            appliance.save()
            messages.success(request, 'Appliance updated.')
            return redirect('home_detail', pk=appliance.home.pk)
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, 'appliances/appliance_form.html', {'appliance': appliance, 'homes': request.user.homes.all()})


@login_required
def appliance_delete_view(request, pk):
    appliance = get_object_or_404(Appliance, pk=pk, home__user=request.user)
    if request.method == 'POST':
        home = appliance.home
        appliance.delete()
        messages.success(request, 'Appliance deleted.')
        return redirect('home_detail', pk=home.pk)
    return render(request, 'appliances/appliance_confirm_delete.html', {'appliance': appliance})
