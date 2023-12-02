from django.shortcuts import render,redirect
from .models import Registration
from .forms import Registrationform
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.
def home(request):
    return render(request,'user_template/home.html')


def user_register(request): 
  

  if request.method == 'POST':
    form = Registrationform(request.POST)
    print(request.POST,'dsfadfewewrwqrrrrrrrrrrrrrrrr')
  
    if form.is_valid():
       firstname =form.cleaned_data['firstname']
       lastname =form.cleaned_data['lastname']
       email =form.cleaned_data['email']
       password =form.cleaned_data['password']
       username=email.split('@')[0]

       user = Registration.objects.create_user(firstname=firstname,lastname=lastname,email=email,username=username,password=password)
       
       user.save()
      #  current_site = get_current_site(request)
      #  mail_subject = 'please activate your account'
      #  message = render_to_string('user_template/account_verification.html',{
      #     'user': user,
      #     'domain': current_site,
      #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
      #     'token': default_token_generator.make_token
      #  })
       messages.success(request,'Registration successful')
       return redirect('register')
  else:
       
       form=Registrationform()

  context={
        'form':form
    }
  return render(request,'user_template/registration.html',context)



def login_user(request):
    if request.method=='POST':
       email = request.POST['email']
       password = request.POST['password']
  
       user = authenticate(request,email=email,password=password)

       if user is not None:
          login(request,user)
          # messages.success(request,'you are successfully logged in')
          return redirect('home')
       else:
          messages.error(request,'invalid login')
          return redirect('register')
       
    return render(request,'user_template/login.html')


@login_required(login_url='login')
def user_logout(request):
   auth.logout(request)
   messages.success(request,'you are logg out')
   return redirect('login')



@login_required(login_url='login')
def dashboard(request):
   return render(request,'user_template/dashboard.html')


def forgotPassword(request):
   if request.method =='POST':
      email = request.POST['email']
      if Registration.objects.get('email').exists():
         user = Registration.objects.filter(email__exact=email)


      else:
         messages.error(request,'message doesnot exist')
   return render(request,'user_template/forgotPassword.html')