from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List


def home_page(request):
    context = {"form": ItemForm()}
    return render(request, "lists/home.html", context)


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        context = {"form": form}
        return render(request, "lists/home.html", context)


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)

    context = {"list": our_list, "form": form}
    return render(request, "lists/list.html", context)


def my_lists(request, email):
    return render(request, "lists/my_lists.html")
