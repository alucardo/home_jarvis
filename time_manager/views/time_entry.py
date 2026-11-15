from django.shortcuts import render


def time_entry_index(request):
    time_entries = request.user.time_entries.all().select_related("category").order_by("-started_at")
    return render(request, "time_manager/time_entry/index.html", {"time_entries": time_entries})
