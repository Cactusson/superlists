from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request):
    return render(request, "lists/home.html")


def new_list(request):
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    return redirect("/lists/the-only-list-in-the-world/")


def view_list(request):
    items = Item.objects.all()
    context = {"items": items}
    return render(request, "lists/list.html", context)
