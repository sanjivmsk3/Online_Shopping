from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from shop.models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from shop.forms import AddForm
import random
import string
from  django.contrib import messages

# Create your views here.

def home(r):
    data = {"item":Item.objects.all(),
    "cat":Category.objects.all(),
    }
    return render(r,"public/home.html",data)

def product(r,slug):
    data = {
        "item":Item.objects.get(slug=slug),
        "cat":Category.objects.all(),
    }
    return render(r,"public/product.html",data)

def catview(r,cat_slug):
    data={
        "item":Item.objects.filter(category__slug=cat_slug),
        "cat":Category.objects.all()
    }
    return render(r,"public/home.html",data)

def search(r):
    if r.method == "GET":
        search = r.GET.get('search')
        data = {
            "item":Item.objects.filter(title__icontains=search),
        }
    return render(r,"public/home.html",data)

@login_required
def addtocart(r,slug):
    item = get_object_or_404(Item,slug=slug)
    orderItem, created = OrderItem.objects.get_or_create(
        item=item,
        user=r.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=r.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            orderItem.qty +=1
            orderItem.save()
            messages.success(r,'This item is updated in our cart')
            return redirect(ordersummery)
        else:
            order.items.add(orderItem)
            messages.success(r,'This item is added in your cart.')
            return redirect(ordersummery)
    else:
        order_date = timezone.now()
        order= Order.objects.create(user=r.user,ordered=False,start_date=order_date)
        order.items.add(orderItem)
        order.save()
        messages.success(r,'This item was added to your cart.')
        return redirect(ordersummery)

def ramovetocart(r,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=r.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=r.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = r.user,
                ordered = False
            )[0]
            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
                messages.error(r,'This item updated successfully.')   
                return redirect(ordersummery)
            else:
                order.items.remove(order_item)
                messages.error(r,'This item updated successfully.')
                return redirect("homepage")
            
            
        else:
            messages.error(r,'This item is not available in your cart.')
            return redirect(ordersummery)
    else:
        messages.warning(r,'You do not have any active order.')
        return redirect(ordersummery)


@login_required
def ordersummery(r):
    try:
        data= {
        "object":Order.objects.get(user=r.user,ordered=False)
            }
    except ObjectDoesNotExist:
        return redirect('homepage')
    return render(r,'public/cart.html',data)

@login_required
def checkout(r):
    form = AddForm(r.POST or None)
    if r.method == 'POST':
        if form.is_valid():
            f = form .save(commit=False)
            f.user = r.user 
            f.save()
            return redirect("checkout")
    data ={
        "addform": form,
        'showadd':Address.objects.filter(user=r.user)
    }
    return render(r,"public/checkout.html",data)

def get_ref_code(digit):
    return ''.join(random.choices(string.digits,k=digit))

def couponcheck(code):
    try:
        coupon= Coupon.objects.get(code=code)
        return True
    except ObjectDoesNotExist:
        return False

def getcoupon(r,code):
    try:
        coupon=Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.error(r,'This coupon does not exists.')
        return redirect('cart')

def coupon_add(r):
    if r.method == 'POST':
        code = r.POST.get("code")
        if couponcheck(code):
            order = Order.objects.get(user=r.user,ordered=False)
            if order.get_total_amount()> 500:
                order.coupon = getcoupon(r,code)
                order.save()
            messages.success(r,'coupon added successfully.')
            return redirect('cart')
        else:
            messages.warning(r,'Coupon invalid ! Please enter a valid coupon.')
            return redirect('cart')
    else:
        messages.error(r,'Please enter a valid coupon.')
        return redirect('cart')

def removecoupon(r):
    order = Order.objects.get(user=r.user,ordered=False)
    order.coupon = None
    order.save()
    messages.error(r,'Coupon removed successfully.')
    return redirect('cart')


def makepayment(r):

    if r.method == 'POST':
        address_id = r.POST.get('adds')

        address = Address.objects.get(user=r.user,id=address_id)


        order = Order.objects.get(user=r.user,ordered=False)
            
        OrderItems = order.items.all()

        OrderItems.update(ordered=True)

        for item in OrderItems: 
            item.save()
        order.ordered= True
        order.ref_code= get_ref_code(8)
        order.address = address
        order.save()


        return redirect('homepage')

def myorder(r):
    order = Order.objects.filter(user=r.user,ordered=True)
    data= {
        'order':order
    }
    return render(r,'public\myorder.html',data)
