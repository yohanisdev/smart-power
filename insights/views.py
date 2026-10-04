from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from insights.models import Insight
from insights.services import build_insights_for_home


@login_required
def insight_list_view(request):
    home = request.user.homes.first()
    if home:
        build_insights_for_home(home)
    insights = Insight.objects.filter(home__user=request.user)
    return render(request, 'insights/insight_list.html', {'insights': insights})
