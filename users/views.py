import uuid

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from listings.models import Category, Listing


# Create your views here.

def index(request):
    if request.htmx:
        return render(request, "cotton/partials/index_partial.html")
    return render(request, 'index.html')


@login_required
def my_listings(request):
    categories = Category.objects.all().order_by('name')
    listings = (Listing.objects
                .filter(user = request.user, is_deleted=False)
                .select_related('category').order_by('-created_at')
                )
    statuses = ('all', 'open', 'closed')

    q = request.GET.get("q")
    status = request.GET.get("status")
    category = request.GET.get("category")

    if q:
        listings = listings.filter(
            Q(title__icontains=q) |
            Q(title__icontains=q.lower())
        )

    if status and status != 'all':
        listings = listings.filter(is_open=True) if status == 'open' else listings.filter(is_open=False)

    if category and category != 'all':
        listings = listings.filter(category__slug=category)

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(listings, 1)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'listings': page_obj.object_list,
        'statuses': statuses,
        'categories': categories,
        'current_status': status,
        'q': q,
        'category': category,
    }

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    context["query_params"] = query_params.urlencode()

    if request.htmx:
        target = request.headers.get('HX-Target')
        if target == "listings":
            return render(request, "cotton/partials/listings_partial.html", context)

        if target == "body":
            return render(request, "users/listings.html", context)

    return render(request, 'users/listings.html', context)

def my_offers(request):
    pass