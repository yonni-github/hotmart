from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .models import Category, Item


# Create your views here.
def index(request):
    return render(request, 'shop/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/shop')

    else:
        form = UserCreationForm()
        context = {'form': form}
    return render(request, 'shop/registration_form.html', context)


# pass category objects to the "shop_by_aisle.html" template
class CategoryView(generic.ListView):
    template_name = "shop/shop_by_aisle.html"
    context_object_name = 'all_categories'

    def get_queryset(self):
        return Category.objects.all().filter(parent=None)


def show_category(request, hierarchy=None):
    slug_category = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    for slug in slug_category[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=slug_category[-1])
    except:
        instance = get_object_or_404(Item, slug=slug_category[-1])
        return render(request, "shop/item_detail.html", {'item_instance': instance})
    else:
        # pass category slugs to the categories.html template
        return render(request, "shop/categories.html", {'instance': instance})
