from django.contrib import messages
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReportForm

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