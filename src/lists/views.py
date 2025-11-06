from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    context = {"form": ItemForm()}
    return render(request, "lists/home.html", context)


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=nulist)
        return redirect(nulist)
    else:
        context = {"form": form}
        return render(request, "lists/home.html", context)


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=our_list)
            return redirect(our_list)
    else:
        form = ItemForm()

    context = {"list": our_list, "form": form}
    return render(request, "lists/list.html", context)
