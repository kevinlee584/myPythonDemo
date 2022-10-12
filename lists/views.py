from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.form import ExistingListItemForm, EMPTY_ITEM_ERROR
from lists.models import  Item, List
from lists.form import ItemForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    # list_ = List.objects.get(id=list_id)
    # error = None

    # if request.method == 'POST':
    #     try:    
    #         item = Item(text=request.POST['item_text'], list=list_)
    #         item.full_clean()
    #         item.save()
    #         return redirect(list_)
    #     except ValidationError:
    #         error = "You can't have an empty list item"
    # return render(request, 'list.html', {'list': list_, 'error': EMPTY_ITEM_ERROR})
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    # list_ = List.objects.create()
    # item = Item(text=request.POST['text'], list=list_)
    # try:
    #     item.full_clean()
    #     item.save()
    # except ValidationError:
    #     list_.delete()
    #     error = "You can't have an empty list item"
    #     return render(request, 'home.html', {"error": error})
    # return redirect(list_)
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})