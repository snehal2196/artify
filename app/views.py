from django import views
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import ContactUsForm, CustomerProfileForm, CustomerRegistrationForm
from .models import ContactUs, Customer, OrderPlaced, Product, Cart
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        totalitems = 0
        products = Product.objects.all()
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'products': products,'totalitems':totalitems})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitems = 0
        product = Product.objects.get(pk=pk)
        already_in_cart = False
        if request.user.is_authenticated:
            already_in_cart = Cart.objects.filter(Q(product=pk) & Q(user=request.user)).exists()
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product': product, 'already_in_cart':already_in_cart,'totalitems':totalitems})

@login_required
def add_to_cart(request):
    totalitems =0
    if request.method == 'GET':
        user = request.user
        product_id = request.GET['id']
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        totalitems = len(Cart.objects.filter(user=request.user))
        already_in_cart = False
        if request.user.is_authenticated:
            already_in_cart = Cart.objects.filter(Q(product=product_id) & Q(user=request.user)).exists()

        data = {
            'totalitems':totalitems,
            'in_cart':already_in_cart
        }
        return JsonResponse(data)

@login_required
def show_cart(request):
    totalitems = 0
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_price = 70
    total_amount = 0.0
    cart_product = [item for item in Cart.objects.all()
                    if item.user == request.user]
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    if cart_product:
        for product in cart_product:
            amount += (product.quantity * product.product.discounted_price)
        total_amount += amount+shipping_price
        return render(request, 'app/addtocart.html', {'cart_items': cart_items, 'amount': amount, 'total_amount': total_amount,
        'totalitems':totalitems})
    else:
        return render(request, 'app/emptycart.html',{'totalitems':totalitems})


def plus_cart(request):
    if request.method == "GET":
        totalitems = 0
        id = request.GET["id"]
        cart = Cart.objects.get(Q(product=id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        amount = 0.0
        shipping_price = 70
        total_amount = 0.0
        cart_product = [item for item in Cart.objects.all()
                    if item.user == request.user]
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for product in cart_product:
                amount += (product.quantity * product.product.discounted_price)
            total_amount += amount+shipping_price

        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'total_amount': total_amount,
            'totalitems':totalitems
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        totalitems = 0
        id = request.GET["id"]
        cart = Cart.objects.get(Q(product=id) & Q(user=request.user))
        cart.quantity -= 1
        cart.save()
        amount = 0.0
        shipping_price = 70
        total_amount = 0.0
        cart_product = [item for item in Cart.objects.all()
                    if item.user == request.user]
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for product in cart_product:
                amount += (product.quantity * product.product.discounted_price)
            total_amount += amount+shipping_price

        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'total_amount': total_amount,
            'totalitems':totalitems
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == "GET":
        totalitems = 0
        id = request.GET["id"]
        cart = Cart.objects.get(Q(product=id) & Q(user=request.user))
        cart.delete()
        amount = 0.0
        shipping_price = 70
        total_amount = 0.0
        cart_product = [item for item in Cart.objects.all()
                    if item.user == request.user]
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for product in cart_product:
                amount += (product.quantity * product.product.discounted_price)
            total_amount += amount+shipping_price

        data = {
            'amount': amount,
            'total_amount': total_amount,
            'totalitems':totalitems
        }
        return JsonResponse(data)

def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    totalitems = 0
    addresses = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'addresses': addresses, 'active': 'btn-warning','totalitems':totalitems})

@login_required
def orders(request):
    totalitems = 0
    orders = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{'orders':orders,'totalitems':totalitems})

@login_required
def change_password(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/changepassword.html',{'totalitems':totalitems})


def topwear(request, data=None):
    if (data == None):
        topwears = Product.objects.filter(category='TW')
    elif (data == 'Nike' or data == 'Adidas'):
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif (data == 'below'):
        topwears = Product.objects.filter(discounted_price__lt=5000)
    elif (data == 'above'):
        topwears = Product.objects.filter(discounted_price__gt=5000)
    return render(request, 'app/topwear.html', {'topwears': topwears})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! Registered successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def paymentdone(request):
    totalitems =0
    custid = request.GET.get('custid')
    user = request.user
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('/orders',{'totalitems':totalitems})

@login_required
def checkout(request):
    totalitems = 0
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_price = 70
    total_amount = 0.0
    cart_product = [item for item in Cart.objects.all()
                    if item.user == request.user]
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))               
    if cart_product:
        for product in cart_product:
            amount += (product.quantity * product.product.discounted_price)
        total_amount += amount+shipping_price

    return render(request, 'app/checkout.html',{'address':address,'cart_items':cart_items,'total_amount':total_amount,
    'totalitems':totalitems})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitems=0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-warning','totalitems':totalitems})

    def post(self, request):
        totalitems = 0
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            postdata = Customer(
                user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            postdata.save()
            messages.success(
                request, 'Congratulations!! Profile Updated Successfully')
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-warning','totalitems':totalitems})

def shop(request):
    totalitems = 0
    products = Product.objects.all()
    drawing = Product.objects.filter(category='D')
    painting = Product.objects.filter(category='P')
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,'app/shop.html',{'products':products, 'drawing':drawing,'painting':painting,'totalitems':totalitems})

def category(request, category=None):
    totalitems = 0
    if category == None:
        products = Product.objects.all()
    elif category == 'drawing':
        products = Product.objects.filter(category='D')
        # low = products.order_by('-discounted_price')
    elif category == 'painting':
        products = Product.objects.filter(category='P')
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/category.html',{'products':products, 'category':category,'low':'low','totalitems':totalitems})


def about(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,'app/about.html',{'totalitems':totalitems})

class ContactView(views.View):
    def get(self,request):
        totalitems=0
        contactForm = ContactUsForm
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        context = {'forms':contactForm,'totalitems':totalitems}
        return render(request,'app/contact.html',context)

    def post(self,request):
        totalitems=0
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            postdata = ContactUs(
                name=name, email=email, message=message)
            postdata.save()
            messages.success(
                request, 'Congratulations!! Our team will reach you shortly')
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/contact.html', {'forms': form, 'active': 'btn-warning','totalitems':totalitems})