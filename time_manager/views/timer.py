from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from time_manager.exceptions.timer_exceptions import TimerAlreadyRunningError, TimerNotRunningError
from time_manager.forms import TimerForm
from time_manager.services.timer_service import start_timer, stop_timer


@require_POST
def timer_start(request):
    form = TimerForm(request.POST, user=request.user)
    if form.is_valid():
        try:
            start_timer(request.user, form.cleaned_data["category"])
            messages.success(request, "Timer wystartowany")
        except TimerAlreadyRunningError:
            messages.error(request, "Timer już działa")
    else:
        messages.error(request, "Błędna kategoria")
    return redirect("dashboard:dashboard")


@require_POST
def timer_stop(request):
    try:
        stop_timer(request.user)
        messages.success(request, "Timer zatrzymany")
    except TimerNotRunningError:
        messages.error(request, "Brak działającego timera")
    return redirect("dashboard:dashboard")
