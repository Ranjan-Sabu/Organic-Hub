from django.shortcuts import render, redirect
from .models import Registration
from .forms import Registrationform
from store.models import Product
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from Accounts.models import UserProfile
from order.models import Order, OrderProduct
from django.shortcuts import get_object_or_404
from .forms import UserProfile, UserForm, UserProfileForm
from functools import wraps

from django.contrib.auth import update_session_auth_hash

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.models import Cart, CartItem
from carts.views import _cart_id


# Create your views here.
# def home(request):
#     return render(request,'user_template/home.html')
def logout_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@csrf_protect
@logout_required
def user_register(request):
    if request.method == "POST":
        form = Registrationform(request.POST)
        print(request.POST, "dsfadfewewrwqrrrrrrrrrrrrrrrr")

        if form.is_valid():
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data["lastname"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            user = Registration.objects.create_user(
                firstname=firstname,
                lastname=lastname,
                email=email,
                username=username,
                password=password,
            )

            user.save()

            profile = UserProfile()
            profile.user = user
            profile.save()

            current_site = get_current_site(request)
            email_subject = "please activate your account"
            message = render_to_string(
                "user_template/verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            sent_email = EmailMessage(email_subject, message, to=[to_email])
            sent_email.send()

            #  messages.success(request,'Registration successful')
            return redirect("/login/?command=verification&email=" + email)
    else:
        form = Registrationform()

    context = {"form": form}
    return render(request, "user_template/registration.html", context)


@csrf_protect
@logout_required
def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:  # Check if the user is active
            try:
                print("try block")
                cart = Cart.objects.get(cart_id=_cart_id(request))
                print(f"Cart: {cart}")  # Add this line for debugging
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(
                    f"is_cart_item_exists: {is_cart_item_exists}"
                )  # Add this line for debugging

                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    print(f"cart_items: {cart_items}")  # Add this line for debugging

                    for item in cart_items:
                        item.user = user
                        item.save()
            except Exception as e:
                print(f"except block: {e}")  # Print the exception message for debugging

            login(request, user)
            # messages.success(request, 'You are successfully logged in')
            return redirect("home")
        else:
            messages.error(request, "Invalid login")
            return redirect("register")

    return render(request, "user_template/login.html")


@login_required(login_url="login")
def user_logout(request):
    auth.logout(request)
    messages.success(request, "you are logg out")
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    print(request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    print("userpro",user_profile)
    order_lists = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {"user_profile": user_profile, "order_lists": order_lists}
    return render(request, "user_template/dashboard.html", context)


@login_required(login_url="login")
def vieworder(request, id):
    orderview = OrderProduct.objects.filter(order=id)

    context = {"orderview": orderview}
    return render(request, "user_template/view_order.html", context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Registration._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Registration.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Registration.objects.filter(email=email).exists():
            user = Registration.objects.get(email__exact=email)
            # set password and email
            current_site = get_current_site(request)
            email_subject = "Reset your password"
            message = render_to_string(
                "user_template/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            sent_email = EmailMessage(email_subject, message, to=[to_email])
            sent_email.send()

            messages.success(
                request, "Password reset mail has been sent to your email address"
            )
            return redirect("login")
        else:
            messages.error(request, "account doesnot exist")
            return redirect("forgotPassword")
    return render(request, "user_template/forgotPassword.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Registration._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Registration.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "please reset your password")
        return redirect("resetpassword")
    else:
        messages.error(request, "this link has been expired")
        return redirect("login")


def resetpassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["Confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            user = Registration.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "password reset successfully")
            return redirect("login")

        else:
            messages.error(request, "password doesnot match")
            return redirect("resetpassword")
    else:
        return render(request, "user_template/resetpassword.html")


@login_required(login_url="loginPage")
def changepassword(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["Confirm_password"]

        user = Registration.objects.get(username=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password Update Successfully")
                return redirect("dashboard")
            else:
                messages.error(request, "Please Enter Valid Current Password")
                return redirect("changepassword")
        else:
            messages.error(request, "Password Didn't Matched")
    return render(request, "user_template/changepassword.html")


@login_required(login_url="login")
def editprofile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    print(user_profile, "userprofile")
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            if user_profile is None:
                user_profile = profile_form.save(commit=False)
                user_profile.user = request.user
            profile_form.save()
            messages.success(request, "Your Profile Has Been Updated")
            return redirect("dashboard")
        else:
            messages.error(request, "Enter Valid Input")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }

    return render(request, "user_template/editprofile.html", context)
