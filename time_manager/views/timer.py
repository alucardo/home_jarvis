from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from time_manager.exceptions.timer_exceptions import TimerAlreadyRunningError
from time_manager.forms import TimerForm
from time_manager.services.timer_service import start_timer


@require_POST
def timer_start(request):
    form = TimerForm(request.POST, user=request.user)
    if form.is_valid():
        try:
            start_timer(request.user, form.cleaned_data["category"])
        except TimerAlreadyRunningError:
            pass
    return redirect("dashboard:dashboard")
