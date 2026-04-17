from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from properties.models import Agent, Property

from .forms import InquiryForm, NewsletterForm
from .models import Testimonial


def home(request):
    featured_properties = (
        Property.objects.filter(is_published=True, featured=True)
        .select_related("location", "property_type")[:3]
    )
    hero_properties = (
        Property.objects.filter(is_published=True)
        .select_related("location", "property_type")
        .order_by("-featured", "-created_at")[:3]
    )
    testimonials = Testimonial.objects.filter(featured=True)[:2]
    context = {
        "featured_properties": featured_properties,
        "hero_properties": hero_properties,
        "testimonials": testimonials,
    }
    return render(request, "core/home.html", context)


def about(request):
    agents = Agent.objects.all()[:4]
    return render(request, "core/about.html", {"agents": agents})


def contact(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inquiry received. Our concierge will respond shortly.")
            return redirect("core:contact")
    else:
        form = InquiryForm()
    return render(request, "core/contact.html", {"form": form})


@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Subscribed to The Aperture Journal.")
    else:
        messages.error(request, "Please provide a valid email.")
    return redirect(request.META.get("HTTP_REFERER", "core:home"))
