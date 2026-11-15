from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from time_manager.models import TimeEntry


def time_entry_index(request):
    time_entries = request.user.time_entries.all().select_related("category").order_by("-started_at")
    return render(request, "time_manager/time_entry/index.html", {"time_entries": time_entries})


@require_POST
def time_entry_delete(request, pk):
    time_entry = get_object_or_404(TimeEntry, pk=pk, user=request.user)
    if time_entry.ended_at is not None:
        time_entry.delete()
    else:
        messages.error(request, "Najpierw zakończ logowanie przed usuwaniem")
    return redirect("time_manager:time_entry_index")
