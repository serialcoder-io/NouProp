from datetime import datetime, timedelta, time

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm
from .models import Report, ReportStatus, Tag
from locations.models import Area

date_filters = (
    {"label": 'Today', 'num_days': 0},
    {"label": 'Last 24h hours', 'num_days': 1},
    {"label": 'This week', 'num_days': 7},
    {"label": 'Past 2 weeks', 'num_days': 14},
    {"label": 'Past 3 weeks', 'num_days': 21},
    {"label": 'This month', 'num_days': 30},
    {"label": 'Past 2 months', 'num_days': 60},
)

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


def staff_reports_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    reports = (
        Report.objects.all()
        .select_related("user", "area__district")
        .prefetch_related("tags")
        .order_by("-created_at")
    )
    areas = Area.objects.select_related("district").order_by("name")
    tags = Tag.objects.all().order_by("name")
    statuses = ("all",) + tuple(choice[0] for choice in ReportStatus.choices)

    q = request.GET.get("q")
    status = request.GET.get("status")
    area = request.GET.get("area")
    date_filter = request.GET.get("date_filter")
    selected_tag = request.GET.get("tag") or "all"

    if q:
        reports = reports.filter(Q(title__icontains=q))

    if status and status != "all":
        reports = reports.filter(status=status)

    if area and area != "all":
        reports = reports.filter(area__id=area)

    if date_filter and date_filter != "all":
        if date_filter == "0":
            today_start = datetime.combine(datetime.today(), time.min)
            reports = reports.filter(created_at__gte=today_start)

        elif date_filter.isdigit():
            days = int(date_filter)
            reports = reports.filter(
                created_at__gte=datetime.now() - timedelta(days=days)
            )

    if selected_tag != "all":
        reports = reports.filter(tags__id=selected_tag)

    page = request.GET.get("page", 1)
    paginator = Paginator(reports, 10)
    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj,
        "reports": page_obj.object_list,
        "areas": areas,
        "tags": tags,
        "statuses": statuses,
        "date_filters": date_filters,
        "current_status": status or "all",
        "current_area": area or "all",
        "current_tag": selected_tag,
        "date_filter": date_filter,
        "q": q,
    }

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    context["query_params"] = query_params.urlencode()

    if request.htmx:
        target = request.headers.get("HX-Target")

        if target == "staff-reports":
            return render(request, "cotton/partials/staff_reports_list_partial.html", context)

        if target == "body":
            return render(request, "reports/staff_reports_list.html", context)

    return render(request, "reports/staff_reports_list.html", context)
