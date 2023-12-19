from django.shortcuts import render,redirect
from carts.models import CartItem
from .forms import OrderForm,Order
import datetime
# Create your views here.
def payments(request):
   return render(request,'order_template/payment.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")
    
    tax = 0
    grand_total = 0

    for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (5 * total)/100
            grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data  = Order()
            data.user=current_user
            data.firstname = form.cleaned_data['firstname']
            data.lastname = form.cleaned_data['lastname']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate Order Number
            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime(
                "%Y%m%d"
            )  # This will be todays Date Eg:- 20231218
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total
            }
            return render(request,'order_template/payment.html',context)

    else:
        return render(request,'user_template/home.html')
def order_complete(request):
   pass