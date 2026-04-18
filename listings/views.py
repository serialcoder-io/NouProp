from django.contrib.auth.decorators import login_required
import uuid
from datetime import datetime, timedelta, time
from django.contrib import messages

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from listings.forms import OfferForm
from listings.models import Listing, Category
from locations.models import District

date_filters = (
        {"label": 'Today', 'num_days': 0},
        {"label": 'Last 24h hours', 'num_days': 1},
        {"label": 'This week', 'num_days': 7},
        {"label": 'Past 2 weeks', 'num_days': 14},
        {"label": 'Past 3 weeks', 'num_days': 21},
        {"label": 'This month', 'num_days': 30},
        {"label": 'Past 2 months', 'num_days': 60},
    )

def listings_view(request):
    listings = Listing.objects.select_related('category', 'area').order_by('-created_at')

    categories = Category.objects.all().order_by('name')
    districts = District.objects.all().order_by('name')

    date_filter = request.GET.get('date_filter')
    category = request.GET.get('category')
    district = request.GET.get('district')
    free_only = request.GET.get('free_only')

    # CATEGORY
    if category and category != "all":
        listings = listings.filter(category__slug=category)

    # DISTRICT
    if district and district != "all":
        listings = listings.filter(area__district__slug=district)

    # FREE ONLY
    if free_only == "on":
        listings = listings.filter(is_free=True)

    # DATE FILTER
    if date_filter and date_filter != "all":

        # TODAY (0)
        if date_filter == "0":
            today_start = datetime.combine(datetime.today(), time.min)
            listings = listings.filter(created_at__gte=today_start)

        # X DAYS
        elif date_filter.isdigit():
            days = int(date_filter)
            listings = listings.filter(
                created_at__gte=datetime.now() - timedelta(days=days)
            )

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(listings, 2)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'listings': page_obj.object_list,
        'categories': categories,
        'districts': districts,
        'free_only': free_only == "on",
        'date_filter': date_filter,
        'category_slug': category,
        'district_slug': district,
        'date_filters': date_filters,
    }

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    context["query_params"] = query_params.urlencode()

    if request.htmx:
        target = request.headers.get('HX-Target')

        if target == "listing-container":
            return render(request, "cotton/partials/listings_container_partial.html", context)

        if target == "body":
            return render(request, "cotton/partials/listings_page_partial.html", context)

    return render(request, "listings/listings.html", context)


def listing_details(request, listing_id):
    listing = get_object_or_404(
        Listing.objects.select_related('area', 'user', 'category'),
        pk=listing_id
    )
    form = OfferForm()
    context = {
        'listing': listing,
        'form': form,
    }
    return render(request, "listings/listing_details.html", context)

@login_required
def make_offer(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.listing = listing
            offer.user = request.user
            offer.save()
            messages.success(request, "Offer sent successfully")
            return redirect("listing_details", listing_id=listing.id)

        return render(request, "listings/listing_details.html", {
            "listing": listing,
            "form": form,
            "modal_open": True
        })

    return redirect("listing_details", listing_id=listing.id)