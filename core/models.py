from django.db import models


class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    photo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return f"{self.author}"

    @property
    def rating_range(self):
        return range(self.rating)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SiteSettings(models.Model):
    """Singleton-ish config row for global site copy."""

    brand_name = models.CharField(max_length=80, default="Aperture Estate")
    tagline = models.CharField(
        max_length=240,
        default="Curating the world's most significant architectural achievements for the discerning few.",
    )
    hq_address = models.CharField(
        max_length=240, default="14 Bruton Place, Mayfair, London, W1J 6LY"
    )
    email = models.EmailField(default="concierge@apertureestate.com")
    phone = models.CharField(max_length=40, default="+44 (0) 20 7946 0123")
    established_year = models.PositiveIntegerField(default=1984)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.brand_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
