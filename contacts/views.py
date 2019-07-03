from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import Contact
from .forms import SearchForm, ContactForm


# Create your views here.

def home(request):
    form = SearchForm()
    search = request.GET.get('search', None)
    request.session['search'] = search
    contacts = []
    if search:
        contacts = Contact.objects.filter().search(search)

    return render(request, 'home.html', {'form': form, 'contacts':contacts})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = dict()
    if request.method == 'POST':
        contact.delete()
        data['form_is_valid'] = True
        contacts = Contact.objects.filter().search(request.session['search'])
        data['html_contact_list'] = render_to_string('includes/partial_contact_list.html', {'contacts': contacts})
    else:
        context = {'contact': contact}
        data['html_form'] = render_to_string('includes/partial_contact_delete.html', context, request=request)
    return JsonResponse(data)


def save_contact_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():            
            form.save()
            data['form_is_valid'] = True
            contacts = Contact.objects.filter().id_search(form.instance.id)
            data['html_contact_list'] = render_to_string('includes/partial_contact_list.html', {'contacts': contacts})
        else:
            data['form_is_valid'] = False
    contact = form.instance
    context = {'form': form, 'contact': contact}

    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, files=request.FILES)
    else:
        form = ContactForm()
    return save_contact_form(request, form, 'includes/partial_contact_create.html')

def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, files=request.FILES, instance=contact )
    else:
        form = ContactForm(instance=contact)
    return save_contact_form(request, form, 'includes/partial_contact_update.html')

