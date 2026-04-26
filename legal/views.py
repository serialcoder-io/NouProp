from django.shortcuts import render


def terms_of_use(request):
    return render(request, "legal/terms_of_use.html")


def privacy_policy(request):
    return render(request, "legal/privacy_policy.html")


def legal_notice(request):
    return render(request, "legal/legal_notice.html")
