from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from .models import User, ContactMessage
from .forms import ContactForm


def contact_us(request):
    """
    Contact form
    """
    contact_form = ContactForm(request.POST or None)

    if request.method == "POST":
        if contact_form.is_valid():
            contact_form.instance.name = request.user
            contact_form.save()
            messages.success(request, 'Your message has been sent')
            return redirect("contact_success")
    template = "contact/contact_us.html"
    context = {
        "form": contact_form,
    }
    return render(request, template, context)


def contact_success(request):
    """
    Contact form success confirmation
    """
    return render(request, "contact/contact_success.html")
