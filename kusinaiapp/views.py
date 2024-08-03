from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import SignUpForm, LoginForm, OTPForm
from .models import AppUser
import random
import string
from django.contrib import messages
from .forms import PhoneNumberForm, VerificationCodeForm, NewPasswordForm




def signup(request):
    
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            
            if AppUser.objects.filter(phone_number=phone).exists():
                form.add_error('phone', 'A user with this phone number already exists.')
            else:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    app_user = AppUser(
                        user=user,
                        name=name,
                        username=username,
                        phone_number=phone,
                        password=password,
                        family_size=1,
                        age_range=[],
                        meal_preference=[],
                        allergies=[],
                        cooking_skills=''
                    )
                    app_user.save()
                    
                    verification_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                    request.session['verification_token'] = verification_token
                    request.session['phone_number'] = phone

                    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(
                        to=phone,
                        channel='sms'
                    )
                    
                    return redirect('verify')

                except IntegrityError:
                    form.add_error(None, 'An error occurred while processing your request.')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def verify(request):
    print("Inside verify view")
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            phone_number = request.session.get('phone_number')

            # Debugging statements
            print(f'Phone number from session: {phone_number}')
            print(f'Entered OTP: {otp}')

            if phone_number:
                try:
                    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    
                    verification_check = client.verify \
                        .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                        .verification_checks \
                        .create(to=phone_number, code=otp)
                    
                    if verification_check.status == 'approved':
                        return redirect('login')  # Redirect to the login page
                    else:
                        form.add_error(None, 'Invalid OTP. Please try again.')
                except TwilioException as e:
                    print(f'Twilio error: {str(e)}')
                    form.add_error(None, 'An error occurred during verification. Please try again later.')
                except Exception as e:
                    print(f'Error during OTP verification: {str(e)}')
                    form.add_error(None, 'An error occurred during verification. Please try again later.')
            else:
                form.add_error(None, 'Phone number not found. Please start the verification process again.')
    else:
        form = OTPForm()
    
    return render(request, 'verify.html', {'form': form})



def tutorial(request):
    return render(request, 'tutorial.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to a success page or home page
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def survey(request):
    return render(request, 'survey.html')

def home(request):
    return render(request, 'home.html')

def homedish(request, dish_id):
    # Replace this with actual dish retrieval logic
    return render(request, 'homedish.html')

def saved(request):
    return render(request, 'saved.html')

def saveddish(request, dish_id):
    # Replace this with actual dish retrieval logic
    return render(request, 'saveddish.html')

def cooked(request):
    return render(request, 'cooked.html')

def about(request):
    return render(request, 'about.html')  # Make sure you have 'about.html' template

def faqs(request):
    return render(request, 'faqs.html')

def terms(request):
    return render(request, 'terms.html')

def forgetpass(request):
    if request.method == 'POST':
        if 'phone' in request.POST:
            phone_form = PhoneNumberForm(request.POST)
            if phone_form.is_valid():
                phone = phone_form.cleaned_data['phone']
                # Logic to send verification code to phone number
                messages.success(request, 'Verification code sent to your phone.')
                request.session['phone'] = phone
                return render(request, 'forgetpass.html', {'code_form': VerificationCodeForm(), 'phone_form': phone_form, 'new_password_form': NewPasswordForm(), 'show_code_form': True})
        elif 'code' in request.POST:
            code_form = VerificationCodeForm(request.POST)
            if code_form.is_valid():
                code = code_form.cleaned_data['code']
                phone = request.session.get('phone')
                # Logic to verify the code
                if True:  # Replace with actual verification logic
                    return render(request, 'forgetpass.html', {'code_form': code_form, 'phone_form': PhoneNumberForm(), 'new_password_form': NewPasswordForm(), 'show_new_password_form': True})
                else:
                    messages.error(request, 'Invalid code.')
        elif 'new_password' in request.POST:
            new_password_form = NewPasswordForm(request.POST)
            if new_password_form.is_valid():
                new_password = new_password_form.cleaned_data['new_password']
                # Logic to update the password if new_password and re_password match
                # Save new password
                messages.success(request, 'Password changed successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
    else:
        phone_form = PhoneNumberForm()
        code_form = VerificationCodeForm()
        new_password_form = NewPasswordForm()

    return render(request, 'forgetpass.html', {'phone_form': phone_form, 'code_form': code_form, 'new_password_form': new_password_form})

#@login_required
def settingss(request):
    return render(request, 'settings.html')

#@login_required
def editprofile(request):
    
    return render(request, 'editprofile.html')

#@login_required
def mealpref(request):
    
    return render(request, 'mealpref.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
