from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem
from store.models import Product
from order.models import Payment, OrderProduct, Order
from .forms import OrderForm, Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
import json


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )

  
    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=order.order_total,
        status=body["status"],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart item to the Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        print(orderproduct)

        # reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stoke -= item.quantity
        product.save()

        
    # clear cart
    CartItem.objects.filter(user=request.user).delete()
    # sent email order email to the customer
    email_subject = "Thank you for your order"
    message = render_to_string(
        "order_template/order_received_email.html",
        {
            "user": request.user,
            "order": order,
            'payment':payment,
        },
    )
    to_email = request.user.email
    sent_email = EmailMessage(email_subject, message, to=[to_email])
    sent_email.send()

    # send order number and the transaction id back to sendData method via JsonResponse
    data = {"order_number": order.order_number, "transID": payment.payment_id}
    return JsonResponse(data)

    return render(request, "order_template/payment.html")


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

    tax = 0
    grand_total = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
        tax = (5 * total) / 100
        grand_total = total + tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.firstname = form.cleaned_data["firstname"]
            data.lastname = form.cleaned_data["lastname"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.city = form.cleaned_data["city"]
            data.state = form.cleaned_data["state"]
            data.country = form.cleaned_data["country"]
            data.address = form.cleaned_data["address"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
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

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
            }
            return render(request, "order_template/payment.html", context)

    else:
        return render(request, "user_template/home.html")


def order_complete(request):
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        context = {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "transID": payment.payment_id,
            "payment": payment,
            "subtotal": subtotal,
        }
        return render(request, "order_template/order_complete.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect("home")




from django.http import JsonResponse


def check_product_availability(request):
    try:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)

        unavailable_products = []

        for cart_item in cart_items:
            product = Product.objects.get(id=cart_item.product.id)
            if product.stoke < cart_item.quantity:
                unavailable_products.append({
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "available_quantity": product.stoke,
                })

        if unavailable_products:
            # If there are unavailable products, return a JSON response with the list of unavailable products
            return JsonResponse({"unavailable_products": unavailable_products})
        else:
            # If all products are available, return a success JSON response
            return JsonResponse({"success": "All products are available"})

    except Exception as e:
        # Handle any exceptions and return an error JSON response
        return JsonResponse({"error": str(e)})
