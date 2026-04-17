from django.contrib import admin

from .models import (
    Agent,
    Amenity,
    Inquiry,
    Location,
    Property,
    PropertyFeature,
    PropertyImage,
    PropertyType,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyFeatureInline(admin.TabularInline):
    model = PropertyFeature
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "property_type", "price", "status", "featured", "is_published")
    list_filter = ("status", "property_type", "featured", "is_published")
    search_fields = ("title", "location__city", "location__country")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("amenities",)
    inlines = [PropertyImageInline, PropertyFeatureInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "region", "country")
    prepopulated_fields = {"slug": ("city", "country")}


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "featured", "order")
    list_editable = ("featured", "order")


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "property", "created_at", "handled")
    list_filter = ("handled", "created_at")
    search_fields = ("name", "email", "message")
