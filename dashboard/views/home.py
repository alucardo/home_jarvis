from django.shortcuts import render

from time_manager.forms import TimerForm
from time_manager.services.timer_service import get_running_entry


def dashboard(request):
    timer_form = TimerForm(user=request.user)
    running_entry = get_running_entry(request.user)
    return render(request, "dashboard/dashboard.html", {"timer_form": timer_form, "running_entry": running_entry})
