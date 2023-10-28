from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from shopquanao import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . token import generate_token

# Create your views here.
def index(request):
    items = Item.objects.all()
    return render(request,'home/index.html',{
        'items': items,
    })

def signin(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Account Does Not Exist')
            return redirect('/signin')
    else:
        return render(request, 'home/signin.html')
    

def signout(request):
    logout(request)
    return redirect('/')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(request, "Your Account has been activated!")
        return redirect('/signin')
    else:
        messages.error(request, "Activation link is invalid!")
    
    return redirect('/index')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('/register')
                
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('/register')
                
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                    
                user.is_active = False
                user.save()
                    
                #Gửi tin nhắn cho email
                subject = "Welcome to my project"
                message = "Hello " + username + "! \n" + "Welcome to my project\n Thank you for joining my project to have some fun"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    
                    
                current_site = get_current_site(request)
                email_subject = "Confirm your account @ Project - Django Signin"
                message2 = render_to_string('confirmation.html', {
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.fail_silently = True
                email.send()
                    
                messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to active your account")
                return redirect('/signin')
                
        else:
            messages.info(request, 'Password Not The Same')
            return redirect('/register')
            
    else:
        return render(request, 'home/register.html')


def checkout(request):
    return render(request,'home/checkout.html') 

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'home/detail.html',{
        'item': item,
    })

def cart(request):
    return render(request,'home/cart.html')

def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(item = item,user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item in order
        if order.items.filter(item__pk = pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"This item quantity was updated successfully")
        else:
            messages.info(request,"This item was added to your cart")
            order_item.quantity = 1
            order_item.save()
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item was added to your cart")
    return redirect('home:detail', pk=pk)

def remove_from_cart(request,pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item in order
        if order.items.filter(item__pk = pk).exists():
            order_item = OrderItem.objects.get_or_create(item = item,user = request.user, ordered = False)[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
        else:
            messages.info(request,"This item was not in your cart")
            return redirect('home:detail', pk=pk)
    else:
        messages.info(request,"You do not have an active order")
        return redirect('home:detail', pk=pk)
    return redirect('home:detail', pk=pk)

