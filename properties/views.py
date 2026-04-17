from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import InquiryForm

from .models import Amenity, Location, Property, PropertyType


def listing(request):
    qs = (
        Property.objects.filter(is_published=True)
        .select_related("location", "property_type")
    )

    location_slug = request.GET.get("location")
    type_slug = request.GET.get("type")
    price_range = request.GET.get("price")
    amenity_slug = request.GET.get("amenity")
    search = request.GET.get("q")

    if location_slug:
        qs = qs.filter(location__slug=location_slug)
    if type_slug:
        qs = qs.filter(property_type__slug=type_slug)
    if amenity_slug:
        qs = qs.filter(amenities__id=amenity_slug)
    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(location__city__icontains=search)
            | Q(location__country__icontains=search)
        )
    price_bounds = {
        "2-5": (2_000_000, 5_000_000),
        "5-15": (5_000_000, 15_000_000),
        "15-50": (15_000_000, 50_000_000),
        "50+": (50_000_000, 10_000_000_000),
    }
    if price_range in price_bounds:
        low, high = price_bounds[price_range]
        qs = qs.filter(price__gte=low, price__lte=high)

    qs = qs.distinct()

    paginator = Paginator(qs, 9)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page,
        "properties": page.object_list,
        "locations": Location.objects.all(),
        "property_types": PropertyType.objects.all(),
        "amenities": Amenity.objects.all(),
        "selected": {
            "location": location_slug,
            "type": type_slug,
            "price": price_range,
            "amenity": amenity_slug,
            "q": search or "",
        },
    }
    return render(request, "properties/listing.html", context)


def detail(request, slug):
    prop = get_object_or_404(
        Property.objects.select_related("location", "property_type", "agent").prefetch_related(
            "images", "features", "amenities"
        ),
        slug=slug,
        is_published=True,
    )

    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = prop
            inquiry.save()
            messages.success(request, "Inquiry sent. Your advisor will be in touch.")
            return redirect(prop.get_absolute_url())
    else:
        form = InquiryForm(initial={"property": prop.id})

    similar = (
        Property.objects.filter(is_published=True, property_type=prop.property_type)
        .exclude(pk=prop.pk)
        .select_related("location")[:3]
    )

    return render(
        request,
        "properties/detail.html",
        {"property": prop, "similar": similar, "form": form},
    )
