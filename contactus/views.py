from django.shortcuts import render
from django.http import JsonResponse

from .forms import ContactForm


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST.dict())
        if form.is_valid():
            form.save()
            return JsonResponse(data={})
        return JsonResponse(
            data=str(form.errors), 
            safe=False, 
            status=400
        )
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', context={'form': form})
