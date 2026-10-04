import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from electricity.models import MeterReading
from homes.models import Home


@login_required
def reading_list_view(request):
    home = request.user.homes.first()
    readings = MeterReading.objects.filter(home=home) if home else MeterReading.objects.none()
    return render(request, 'electricity/reading_list.html', {'readings': readings, 'home': home})


@login_required
def reading_create_view(request):
    home = request.user.homes.first()
    if request.method == 'POST':
        home_id = request.POST.get('home')
        home = get_object_or_404(Home, pk=home_id, user=request.user)
        if 'csv_file' in request.FILES:
            file = request.FILES['csv_file']
            text = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(text))
            if reader.fieldnames is None or 'date' not in reader.fieldnames or 'kwh' not in reader.fieldnames:
                messages.error(request, 'CSV must include date and kwh columns.')
                return render(request, 'electricity/reading_form.html', {'homes': request.user.homes.all(), 'home': home})
            imported = []
            for row in reader:
                try:
                    reading = MeterReading(
                        home=home,
                        reading_date=row['date'],
                        reading_value_kwh=row['kwh'],
                        source='csv_import',
                        notes='Imported from CSV',
                    )
                    reading.full_clean()
                    imported.append(reading)
                except Exception as exc:
                    messages.error(request, f'Invalid CSV row: {row}. Error: {exc}')
                    return render(request, 'electricity/reading_form.html', {'homes': request.user.homes.all(), 'home': home})
            for reading in imported:
                reading.save()
            messages.success(request, f'Imported {len(imported)} readings successfully.')
            return redirect('reading_list')

        reading = MeterReading(
            home=home,
            reading_value_kwh=request.POST.get('reading_value_kwh', 0),
            reading_date=request.POST.get('reading_date'),
            source=request.POST.get('source', 'manual'),
            notes=request.POST.get('notes', ''),
        )
        try:
            reading.full_clean()
            reading.save()
            messages.success(request, 'Meter reading added.')
            return redirect('reading_list')
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, 'electricity/reading_form.html', {'homes': request.user.homes.all(), 'home': home})


@login_required
def reading_update_view(request, pk):
    reading = get_object_or_404(MeterReading, pk=pk, home__user=request.user)
    if request.method == 'POST':
        reading.reading_value_kwh = request.POST.get('reading_value_kwh', reading.reading_value_kwh)
        reading.reading_date = request.POST.get('reading_date', reading.reading_date)
        reading.source = request.POST.get('source', reading.source)
        reading.notes = request.POST.get('notes', reading.notes)
        try:
            reading.full_clean()
            reading.save()
            messages.success(request, 'Meter reading updated.')
            return redirect('reading_list')
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, 'electricity/reading_form.html', {'reading': reading, 'homes': request.user.homes.all()})


@login_required
def reading_delete_view(request, pk):
    reading = get_object_or_404(MeterReading, pk=pk, home__user=request.user)
    if request.method == 'POST':
        reading.delete()
        messages.success(request, 'Meter reading deleted.')
        return redirect('reading_list')
    return render(request, 'electricity/reading_confirm_delete.html', {'reading': reading})
