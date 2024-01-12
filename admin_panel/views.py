from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from category.models import Category
from store.models import Product
from Accounts.models import Registration, UserProfile
from order.models import Order, OrderProduct, Payment
from admin_panel.forms import CategoryUpdateForm, ProductUpdateForm,OrderStatusUpdateForm
from django.contrib.auth.decorators import user_passes_test


def super_admin(user):
    return user.is_authenticated and user.is_staff

# Create your views here.

@user_passes_test(super_admin)
def admin_panel(request):
    return render(request, "admin_template/admin_panel.html")

@user_passes_test(super_admin)
def category(request):
    categories = Category.objects.all().order_by("id")

    context = {"categories": categories}

    return render(request, "admin_template/category.html", context)

@user_passes_test(super_admin)
def add_Category(request):
    if request.method == "POST":
        form = CategoryUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect("admin_category")
    else:
        form = CategoryUpdateForm()

    context = {
        "form": form,
    }
    return render(request, "admin_template/category_update_form.html", context)

@user_passes_test(super_admin)
def edit_Category(request, slug):
    category = Category.objects.get(slug=slug)

    if request.method == "POST":
        print(request.POST)
        form = CategoryUpdateForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category edited successfully.')
            return redirect("admin_category")
    else:
        form = CategoryUpdateForm(instance=category)

    context = {
        "form": form,
    }
    return render(request, "admin_template/category_update_form.html", context)

@user_passes_test(super_admin)
def delete_Category(request, slug):
    category = Category.objects.get(slug=slug)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect("admin_category")

@user_passes_test(super_admin)
def products(request):
    products = Product.objects.all().order_by("id")

    context = {"products": products}
    return render(request, "admin_template/products.html", context)

@user_passes_test(super_admin)
def add_Product(request):
    if request.method == "POST":
        form = ProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect("admin_product")
    else:
        form = ProductUpdateForm()

    context = {
        "form": form,
    }
    return render(request, "admin_template/product_update_form.html", context)

@user_passes_test(super_admin)
def edit_Product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        print(request.POST)
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product edited successfully.')
            return redirect("admin_product")
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        "form": form, 
    }
    return render(request, "admin_template/product_update_form.html", context)

@user_passes_test(super_admin)
def delete_Product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect("admin_product")

@user_passes_test(super_admin)
def users(request):
    users = Registration.objects.all().order_by("id")

    context = {"users": users}
    return render(request, "admin_template/users.html", context)

@user_passes_test(super_admin)
def blockuser(request, id):
    user_to_block = Registration.objects.get(id=id)

    if user_to_block.is_superadmin:
        messages.error(request, "Cannot block super admin.")
    elif user_to_block.is_staff and user_to_block == request.user:
        messages.error(request, "Cannot block yourself.")
    else:
        if user_to_block.is_blocked:
            user_to_block.is_blocked = False
            messages.success(request, f"{user_to_block.get_full_name()} has been unblocked.")
            user_to_block.save()
        else:
            user_to_block.is_blocked = True
            messages.success(request, f"{user_to_block.get_full_name()} has been blocked.")
            user_to_block.save()

    return redirect("admin_users")

def toggle_admin(request, id):
    user_to_toggle = Registration.objects.get(id=id)

    # Super admin cannot toggle own admin status
    if user_to_toggle == request.user:
        messages.error(request, "Cannot change your own admin status.")
    else:
        user_to_toggle.is_staff = not user_to_toggle.is_staff
        user_to_toggle.save()

        action = "added" if user_to_toggle.is_staff else "removed"
        messages.success(request, f"{user_to_toggle.get_full_name()} has been {action} as an admin.")

    return redirect("usersprofile", id=user_to_toggle.id)

@user_passes_test(super_admin)
def usersprofile(request, id):
    u=Registration.objects.get(pk=id)
    user = UserProfile.objects.get(user=u)
    context = {"user": user}
    return render(request, "admin_template/users_profile.html", context)

@user_passes_test(super_admin)
def orders(request):
    
    orders = Order.objects.all().order_by('-created_at')
 
    context = {
        "orders": orders,
    
    }
    return render(request, "admin_template/orders.html", context)

@user_passes_test(super_admin)
def orderdetails(request, id):
    order = Order.objects.get(id=id)
    details = OrderProduct.objects.filter(order=order)
    print(f"Details: {details}")

    context = {"details": details,"order":order}
   

    return render(request, "admin_template/orderdetails.html", context)

@user_passes_test(super_admin) 
def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orderdetails', id=id)  
    else:
        form = OrderStatusUpdateForm(instance=order)

    return render(request, 'admin_template/update_order_status.html', {'form': form, 'order': order})