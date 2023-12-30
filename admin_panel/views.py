from django.shortcuts import render, redirect
from django.contrib import messages
from category.models import Category
from store.models import Product
from Accounts.models import Registration, UserProfile
from order.models import Order, OrderProduct, Payment
from admin_panel.forms import CategoryUpdateForm, ProductUpdateForm

# Create your views here.


def admin_panel(request):
    return render(request, "admin_template/admin_panel.html")


def category(request):
    categories = Category.objects.all().order_by("id")

    context = {"categories": categories}

    return render(request, "admin_template/category.html", context)


def add_Category(request):
    if request.method == "POST":
        form = CategoryUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_category")
    else:
        form = CategoryUpdateForm()

    context = {
        "form": form,
    }
    return render(request, "admin_template/category_update_form.html", context)


def edit_Category(request, slug):
    category = Category.objects.get(slug=slug)

    if request.method == "POST":
        print(request.POST)
        form = CategoryUpdateForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect("admin_category")
    else:
        form = CategoryUpdateForm(instance=category)

    context = {
        "form": form,
    }
    return render(request, "admin_template/category_update_form.html", context)


def delete_Category(request, slug):
    category = Category.objects.get(slug=slug)
    category.delete()
    # messages.success(request, 'Category deleted successfully.')
    return redirect("admin_category")


def products(request):
    products = Product.objects.all().order_by("id")

    context = {"products": products}
    return render(request, "admin_template/products.html", context)


def add_Product(request):
    if request.method == "POST":
        form = ProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_product")
    else:
        form = ProductUpdateForm()

    context = {
        "form": form,
    }
    return render(request, "admin_template/product_update_form.html", context)


def edit_Product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        print(request.POST)
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("admin_product")
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        "form": form,
    }
    return render(request, "admin_template/product_update_form.html", context)


def delete_Product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("admin_product")


def users(request):
    users = Registration.objects.all().order_by("id")

    context = {"users": users}
    return render(request, "admin_template/users.html", context)


def blockuser(request, id):
    # user = get_object_or_404(User, id=id)
    user = Registration.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect("admin_users")


def usersprofile(request, id):
    u=Registration.objects.get(pk=id)
    user = UserProfile.objects.get(user=u)
    context = {"user": user}
    return render(request, "admin_template/users_profile.html", context)


def booking(request):
    # order_number = request.GET.get('order_number')
    # transID = request.GET.get('payment_id')

    order = Order.objects.all()
    ordered_products = OrderProduct.objects.all()

    # payment = Payment.objects.get(payment_id=transID)
    # subtotal =0
    # for i in ordered_products:
    #    subtotal += i.product_price * i.quantity
    context = {
        "order": order,
        "ordered_products": ordered_products,
        #    'order_number' : order.order_number,
        #    'transID' : payment.payment_id,
        #    'payment' : payment,
        #    'subtotal' : subtotal
    }
    return render(request, "admin_template/booking.html", context)
