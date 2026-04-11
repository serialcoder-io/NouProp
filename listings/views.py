from django.shortcuts import render
from listings.models import Listing, Category
from locations.models import District


def listings_view(request):
    listings = Listing.objects.select_related('category', 'area')
    categories = Category.objects.all().order_by('name')
    districts = District.objects.all().order_by('name')
    context = {'listings': listings, 'categories': categories, 'districts': districts}
    if request.htmx:
        return render(request, "cotton/partials/listings_page_partial.html", context)
    return render(request, 'listings/listings_page.html', context)
