from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm
from .models import Report, ReportStatus

# Create your views here.
def reports(request):
    return HttpResponse("reports")

def create_report(request):
    form = ReportForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():

        report = form.save(commit=False)

        # USER (optional: a anonymous user can can report an illegal dumping)
        report.user = request.user if request.user.is_authenticated else None

        report.save()
        form.save_m2m()
        messages.success(request, "your report has been sent successfully. thank your for helping")
        return redirect("my_offers")

    return render(request, "reports/create_report.html", {
        "form": form
    })


def report_details(request, report_id):
    report = get_object_or_404(
        Report.objects.select_related("user", "area__district").prefetch_related("tags"),
        pk=report_id,
    )

    is_owner = request.user.is_authenticated and request.user == report.user
    is_staff = request.user.is_authenticated and request.user.is_staff

    if not (is_owner or is_staff):
        return HttpResponseForbidden()

    valid_statuses = {choice[0] for choice in ReportStatus.choices}

    if request.method == "POST":
        if not is_staff:
            return HttpResponseForbidden()

        status = request.POST.get("status")
        if status not in valid_statuses:
            return HttpResponseForbidden()

        report.status = status
        report.save(update_fields=["status", "updated_at"])
        return redirect("report_details", report_id=report.id)

    context = {
        "report": report,
        "status_choices": ReportStatus.choices,
        "is_staff_user": is_staff,
        "has_coordinates": report.lat is not None and report.lng is not None,
    }
    return render(request, "reports/report_details.html", context)
