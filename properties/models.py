from builtins import property as cached_property_alias

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

_py_property = cached_property_alias


class Location(models.Model):
    city = models.CharField(max_length=120)
    region = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120)
    slug = models.SlugField(max_length=180, unique=True, blank=True)

    class Meta:
        ordering = ["country", "city"]

    def __str__(self):
        parts = [self.city, self.region, self.country]
        return ", ".join(p for p in parts if p)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.city}-{self.country}")[:180]
        super().save(*args, **kwargs)


class PropertyType(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Amenity(models.Model):
    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(
        max_length=60,
        default="star",
        help_text="Material Symbols Outlined icon name",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    photo = models.ImageField(upload_to="agents/", blank=True, null=True)
    photo_url = models.URLField(blank=True, help_text="External fallback image")
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} — {self.role}"

    @property
    def image_src(self):
        if self.photo:
            return self.photo.url
        return self.photo_url


class Property(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("exclusive", "Exclusive"),
        ("new", "New Listing"),
        ("pending", "Pending"),
        ("sold", "Sold"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tagline = models.CharField(max_length=180, blank=True)
    description = models.TextField()
    vision = models.TextField(
        blank=True,
        help_text="Architectural vision / editorial prose for detail page",
    )

    location = models.ForeignKey(
        Location, related_name="properties", on_delete=models.PROTECT
    )
    address = models.CharField(max_length=255, blank=True)

    property_type = models.ForeignKey(
        PropertyType, related_name="properties", on_delete=models.PROTECT
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    price = models.DecimalField(max_digits=14, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    square_feet = models.PositiveIntegerField(default=0)
    garage_spaces = models.PositiveIntegerField(default=0)

    cover_image = models.ImageField(upload_to="properties/", blank=True, null=True)
    cover_image_url = models.URLField(
        blank=True, help_text="External fallback image"
    )

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")
    agent = models.ForeignKey(
        Agent,
        related_name="properties",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-created_at"]
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("properties:detail", kwargs={"slug": self.slug})

    @property
    def cover_src(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url

    @property
    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="properties/gallery/", blank=True, null=True)
    image_url = models.URLField(blank=True)
    caption = models.CharField(max_length=160, blank=True)
    alt = models.CharField(max_length=240, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image for {self.property.title}"

    @_py_property
    def src(self):
        if self.image:
            return self.image.url
        return self.image_url


class PropertyFeature(models.Model):
    property = models.ForeignKey(
        Property, related_name="features", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=60, default="star")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.property.title} — {self.title}"


class Inquiry(models.Model):
    property = models.ForeignKey(
        Property,
        related_name="inquiries",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    interest = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"
