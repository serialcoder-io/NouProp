# from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta, time

# from .permissions import is_collector
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from listings.models import Category, Listing, Offer
from reports.models import Report


# Create your views here.

def index(request):
    if request.htmx:
        return render(request, "cotton/partials/index_partial.html")
    return render(request, 'index.html')


@login_required
def my_listings(request):
    categories = Category.objects.all().order_by('name')
    listings = (Listing.objects
                .filter(user=request.user, is_deleted=False)
                .select_related('category').order_by('-created_at')
                )
    listing_statuses = ('all', 'open', 'closed')

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
    paginator = Paginator(listings, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'listings': page_obj.object_list,
        'statuses': listing_statuses,
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


# offer statuses
statuses = ('all', 'pending', 'accepted', 'rejected')
# offer dates filters
date_filters = (
    {"label": 'Today', 'num_days': 0},
    {"label": 'Last 24h hours', 'num_days': 1},
    {"label": 'This week', 'num_days': 7},
    {"label": 'Past 2 weeks', 'num_days': 14},
    {"label": 'Past 3 weeks', 'num_days': 21},
    {"label": 'This month', 'num_days': 30},
    {"label": 'Past 2 months', 'num_days': 60},
)


@login_required
def my_offers(request):
    if not (request.user.role and request.user.role.name == "collector"):
        raise Http404()
    offers = (
        Offer.objects
        .filter(user=request.user, is_deleted=False)
        .select_related('listing')
        .order_by('-created_at')
    )

    categories = Category.objects.all().order_by('name')

    # GET params
    q = request.GET.get("q")
    status = request.GET.get("status")
    date_filter = request.GET.get("date_filter")
    category = request.GET.get("category")

    # SEARCH
    if q:
        offers = offers.filter(
            Q(listing__title__icontains=q)
        )

    # STATUS FILTER
    if status and status != 'all':
        offers = offers.filter(status=status)

    if category and category != 'all':
        offers = offers.filter(listing__category__slug=category)

    # DATE FILTER
    if date_filter and date_filter != "all":

        if date_filter == "0":
            today_start = datetime.combine(datetime.today(), time.min)
            offers = offers.filter(created_at__gte=today_start)

        elif date_filter.isdigit():
            days = int(date_filter)
            offers = offers.filter(
                created_at__gte=datetime.now() - timedelta(days=days)
            )

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(offers, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'offers': page_obj.object_list,
        'statuses': statuses,
        'date_filters': date_filters,
        'current_status': status,
        'current_date_filter': date_filter,
        'categories': categories,
        'q': q,
    }

    # pagination
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    context["query_params"] = query_params.urlencode()

    # HTMX support
    if request.htmx:
        target = request.headers.get('HX-Target')

        if target == "offers":
            return render(request, "cotton/partials/offers_partial.html", context)

        if target == "body":
            return render(request, "users/offers.html", context)

    return render(request, "users/offers.html", context)


@login_required
def received_offers(request):
    """
    Render offers received on the current user's listings.
    """
    offers = (
        Offer.objects
        .filter(listing__user=request.user, is_deleted=False)
        .select_related('listing', 'user')  # the user who made the offer
        .order_by('-created_at')
    )
    categories = Category.objects.all().order_by('name')

    # GET params
    q = request.GET.get("q")
    status = request.GET.get("status")
    date_filter = request.GET.get("date_filter")
    category = request.GET.get("category")

    # SEARCH
    if q:
        offers = offers.filter(
            Q(listing__title__icontains=q)
        )

    # STATUS FILTER
    if status and status != 'all':
        offers = offers.filter(status=status)

    if category and category != 'all':
        offers = offers.filter(listing__category__slug=category)

    # DATE FILTER
    # date_filter defines the time window in days:
    # - "0"  → today only
    # - "1"  → last 24 hours
    # - "7"  → last 7 days (1 week)
    # - "30" → last 30 days (1 month)
    # - up to 60 days max
    if date_filter and date_filter != "all":

        if date_filter == "0":
            today_start = datetime.combine(datetime.today(), time.min)
            offers = offers.filter(created_at__gte=today_start)

        elif date_filter.isdigit():
            days = int(date_filter)
            offers = offers.filter(
                created_at__gte=datetime.now() - timedelta(days=days)
            )

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(offers, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'offers': page_obj.object_list,
        'statuses': statuses,
        'date_filters': date_filters,
        'current_status': status,
        'current_date_filter': date_filter,
        'categories': categories,
        'q': q,
    }

    # clean query params (pagination HTMX)
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    context["query_params"] = query_params.urlencode()

    # HTMX
    if request.htmx:
        target = request.headers.get('HX-Target')

        if target == "received-offers":
            return render(request, "cotton/partials/received_offers_partial.html", context)

        if target == "body":
            return render(request, "users/received_offers.html", context)

    return render(request, "users/received_offers.html", context)


@login_required
def my_reports(request):
    """
    Render reports created by the current user.
    """

    reports = (
        Report.objects
        .filter(user=request.user)
        .select_related('user', 'area')
        .prefetch_related('tags')
        .order_by('-created_at')
    )

    categories = Category.objects.all().order_by('name')
    reports_statuses = ('all', 'pending', 'validated', 'in_progress', 'completed', 'rejected')

    # GET params
    status = request.GET.get("status")
    date_filter = request.GET.get("date_filter")
    category = request.GET.get("category")

    # STATUS FILTER
    if status and status != 'all':
        reports = reports.filter(status=status)

    # CATEGORY FILTER
    if category and category != 'all':
        reports = reports.filter(category__slug=category)

    # DATE FILTER
    if date_filter and date_filter != "all":

        if date_filter == "0":
            today_start = datetime.combine(datetime.today(), time.min)
            reports = reports.filter(created_at__gte=today_start)

        elif date_filter.isdigit():
            days = min(int(date_filter), 60)
            reports = reports.filter(
                created_at__gte=datetime.now() - timedelta(days=days)
            )

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(reports, 10)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'reports': page_obj.object_list,
        'statuses': reports_statuses,
        'date_filters': date_filters,
        'current_status': status,
        'current_date_filter': date_filter,
        'categories': categories,
    }

    # clean query params (pagination HTMX)
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    context["query_params"] = query_params.urlencode()

    # HTMX
    if request.htmx:
        target = request.headers.get('HX-Target')

        if target == "my-reports":
            return render(request, "cotton/partials/my_reports_partial.html", context)

        if target == "body":
            return render(request, "users/reports.html", context)

    return render(request, "users/reports.html", context)