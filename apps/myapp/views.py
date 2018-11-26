from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import User, Wish_List
import bcrypt

def index(request):
    if 'user_id' in request.session:
        return redirect('/wish_items')

    return render(request, 'myapp/index.html')


def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
        print(errors)
        return redirect("/")
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST["name"], username=request.POST["username"], date_hired=request.POST["date_hired"], password=pwhash)
        print(user)
        request.session['user_id'] = user.id
        return redirect("/wish_items")


def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)
    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect("/")
    else:
        user = User.objects.get(username=request.POST['username'])
        request.session['user_id'] = user.id
        print("session id is", request.session['user_id'])
        print(user)
        return redirect("/wish_items")


def wish_items(request):
    if 'user_id' not in request.session:
        return redirect("/")
    else:
        other_wishlists = []
        all_wishlists = Wish_List.objects.all()
        user = User.objects.get(id=request.session['user_id'])
        wishlists = user.added_wishlists.all()
        for wishlist in all_wishlists:
            if wishlist not in wishlists:
                other_wishlists.append(wishlist)
        context = {
            "other_wishlists": other_wishlists,
            "user": user,
            "wishlists": wishlists, 
        }
    return render(request, "myapp/wish_items.html", context)

def add(request):
    return render(request, "myapp/add.html")


def create(request):
    errors = Wish_List.objects.wish_list_validator(request.POST)
    if errors:
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error)
        print(errors)
        return redirect ("/add")
    else:
        wishlist = Wish_List.objects.create(item=request.POST["item"], uploader_id=request.session["user_id"])
        wishlist.added_users.add(User.objects.get(id=request.session['user_id']))
        print(wishlist)
        return redirect('/wish_items')


def delete(request, wishlistid):
    Wish_List.objects.get(id=wishlistid).delete()
    return redirect('/wish_items')


def remove(request, wishlistid):
    wishlist = Wish_List.objects.get(id=wishlistid)
    wishlist.added_users.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/wish_items')


def add_wishlist(request, wishlistid):
    wishlist = Wish_List.objects.get(id=wishlistid)
    wishlist.added_users.add(User.objects.get(id=request.session['user_id']))
    return redirect('/wish_items')


def item(request, wishlistid):
    wishlist = Wish_List.objects.get(id=wishlistid)
    context = { 
        "wishlist": wishlist,
        "users": wishlist.added_users.all(),
    }
    print(wishlist)
    return render(request, 'myapp/item.html', context)


def clear(request):
    request.session.clear()
    return redirect("/")