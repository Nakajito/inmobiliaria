from django import forms

from properties.models import Inquiry

from .models import NewsletterSubscriber


class InquiryForm(forms.ModelForm):
    INTEREST_CHOICES = [
        ("Curated Acquisition", "Curated Acquisition"),
        ("Asset Liquidation", "Asset Liquidation"),
        ("Strategic Investment", "Strategic Investment"),
        ("Architectural Partnership", "Architectural Partnership"),
    ]
    interest = forms.ChoiceField(choices=INTEREST_CHOICES, required=False)

    class Meta:
        model = Inquiry
        fields = ["name", "email", "phone", "interest", "message", "property"]
        widgets = {
            "property": forms.HiddenInput(),
            "phone": forms.TextInput(),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
