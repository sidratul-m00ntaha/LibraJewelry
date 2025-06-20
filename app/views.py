
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . models import Product, Customer, Cart
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,"app/home.html")
 
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html", locals())

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html", locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request,"app/category.html",locals())
    

class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
        def get(self,request,pk):
            totalitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
            product= Product.objects.get(pk=pk)
            return render(request,"app/productdetail.html",locals())

# class ProductDetail(View):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         return render(request, "app/productdetail.html", {'product': product})

# class  CustomerRegistrationView(View):
#     def get(self,request):
#         form=CustomerRegistrationForm()
#         return render(request,'app/customerregistration.html',locals())
#     def post(self,request):
#         form=CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Congratulations! User Register Successfully")

#         else:
#             messages.warning(request,"Invalid Input Data")
#         return render(request,'app/customerregistration.html',locals())
    

class  CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            return redirect("login")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())



class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request,'app/profile.html',locals())
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city, state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())
    
# ✅ Fix: Move this out of the class!
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())
    
# ✅ Also move this out of ProfileView
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
            return redirect("address")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/updateAddress.html', locals())

# @login_required
# def add_to_cart(request):
#     user=request.user
#     product_id=request.GET.get('prod_id')
#     product=Product.objects.get(id=product_id)
#     Cart(user=user,product=product).save()
#     return redirect("/cart")

# @login_required
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     if not product_id:
#         raise Http404("Product ID not provided")
    
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         raise Http404("Product not found")
    
#     Cart(user=user, product=product).save()
#     return redirect("/cart")

# @login_required
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     if not product_id:
#         raise Http404("Product ID not provided")

#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         raise Http404("Product not found")

#     Cart(user=user, product=product).save()
#     return redirect("/cart")


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    print("PRODUCT ID RECEIVED:", product_id)  # Debug line

    if not product_id:
        raise Http404("Product ID not provided")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    print("ADDED TO CART:", cart_item.product.title)  # Debug line
    return redirect("/cart")


# @login_required
# def show_cart(request):
#     user=request.user
#     cart=Cart.objects.filter(user=user)
#     return render(request,'app/addtocart.html',locals())

# @login_required
# def show_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user)

#     amount = 0
#     shipping_amount = 40  # fixed shipping
#     totalamount = 0
    

#     if cart.exists():
#         for item in cart:
#             amount += item.quantity * item.product.discounted_price
#         totalamount = amount + shipping_amount

#     return render(request, 'app/addtocart.html', {
#         'cart': cart,
#         'amount': amount,
#         'totalamount': totalamount,
#     })


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)

    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 40  # fixed shipping cost

    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/addtocart.html', locals())

#will update later based on the payment gateway integration
class checkout(View):
    def get(self, request):
        return render(request, 'app/checkout.html', locals())
            
 

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        total_amount = amount + 40  # fixed shipping cost
        data={
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        total_amount = amount + 40  # fixed shipping cost
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        total_amount = amount + 40  # fixed shipping cost
        data = {
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)
    

@login_required    
def search(request):
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(title__icontains=query)
    return render(request, 'app/search.html', locals())