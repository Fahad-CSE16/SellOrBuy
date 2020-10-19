# basic import
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import View
import time
# Userlogin signup, import
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeForm, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetView, PasswordResetForm, PasswordResetDoneView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
# LocAL IMPORT
from .forms import *
from .models import UserProfile

# TOKEN  generator import
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel = get_user_model()

# from notifications.signals import notify
# user = request.user
# receiver = User.objects.filter(username=post.author).first()
# notify.send(user, recipient=user, verb='Your any message that will show after the name of a sender')

class homeView(View):
    template_name= "person/home.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def handleSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('person/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(
                request, 'Please confirm From your email address to complete the registration and Then you can login')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'person/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(
            request, f"Thank you for your email confirmation.  Now you can login your account. {user}")
        return redirect('login')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('signup')


def handleLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"You are now logged in as {username}")
                return redirect('product:show')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="person/login.html",
                  context={"form": form})


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('product:show')


def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Has changed successfully!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'person/changepass.html', {'form': form})


class ResetPassword(PasswordResetView):
    template_name = 'person/reset_pass.html'


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'person/reset_pass_done.html'


class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'person/reset_pass_confirm.html'


class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'person/reset_pass_complete.html'


def notification(request):
    user = User.objects.get(username=request.user.username)
    qs = user.notifications.read()
    us = user.notifications.unread()
    return render(request, 'person/notification.html', {'qs': qs, 'us':us})
    
def markasread(request):
    user = User.objects.get(username=request.user.username)
    qs = user.notifications.unread()
    qs.mark_all_as_read()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def updateprofile(request):
    try:
        instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance = None
    username = request.user.username
    userp = User.objects.get(username=username)
    if request.method == 'POST':
        if instance:
            p_form = UserProfileForm(
                request.POST, request.FILES, instance=instance)
        else:
            p_form = UserProfileForm(request.POST, request.FILES)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            profile_obj = p_form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            email = u_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists() and userp.email != email:
                messages.warning(
                    request, 'Your Provided email is already in Use in another profile.')
                return redirect('updateprofile')
            elif userp.email == email:
                u_form.save()
            else:
                user = u_form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('person/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email1 = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email1.send()
                messages.warning(
                    request, ' Email Changed. Temporarily Your accound has been deactivated.')
                messages.info(
                    request, 'Activate your account From your email address and only then you can login.')
                logout(request)
                return redirect('home')
            messages.success(request, 'Successfully updated.')
            return redirect('userprofile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=instance)
    userp = UserProfile.objects.filter(user=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': request.user,
        'userp': userp
    }
    # redirect to a new URL:
    return render(request, 'person/updateprofile.html', context)
from product.models import OrderItem,Order
def userprofile(request):
    userp = UserProfile.objects.filter(user=request.user)
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'person/userprofile.html', {'userp': userp,'orders':orders})
