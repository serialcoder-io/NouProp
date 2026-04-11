from django.shortcuts import render

from listings.models import Listing


def listings(request):
    if request.htmx:
        return render(request, "cotton/partials/listings_page_partial.html")
    return render(request, 'listings/listings_page.html')
