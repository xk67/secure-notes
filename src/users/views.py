from .forms import SignUpForm, DeleteForm
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, get_user_model, logout
from django.http import Http404
from django.contrib.auth.decorators import login_required
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
import base64
from django.contrib import messages
from django.views.decorators.http import require_GET, require_http_methods

User = get_user_model()

# sha256 always returns 32 bytes, no matter how long the secret key is
bytes = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
key = base64.urlsafe_b64encode(bytes)
fernet = Fernet(key)

@require_http_methods(["GET", "POST"])
def signup(request):

    if request.user.is_authenticated:
        return redirect('notes:create_note')

    if request.method == "POST":
       form = SignUpForm(request.POST)
       if form.is_valid():
            user = form.save()

            username = user.username
            email = user.email
            domain = get_current_site(request).domain

            token = fernet.encrypt(force_bytes(user.pk)).decode('utf-8')

            html_content = render_to_string(
                "users/verification.html",
                context={"username": username, "domain": domain, "token": token},
            )
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                "Email Verification",
                text_content,
                "noreply@secure-notes.de",
                [email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Account created successfully! Please check your emails to verify your account.')
            return redirect('users:signup')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})

@require_GET
def verify(request, token):

    # Use a try block because handle user input, base64 decoding or missing users can cause errors
    try:
        id = int(force_str(fernet.decrypt(token.encode('utf-8'))))
        user = User.objects.get(pk=id)

        user.is_active = True
        user.save()

        return render(request, "users/verification_confirm.html")
    except Exception:

        # Return 404 for invalid tokens or non-existent users
        raise Http404()

@login_required
@require_GET
def profile(request):
    return render(request, 'users/profile.html')

@login_required
@require_http_methods(["GET", "POST"])
def delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():

            username = request.user.username
            password = form.cleaned_data["password"]

            # No need to check confirm, handled by form.is_valid(

            user = authenticate(username=username, password=password)

            if not user:
                form.add_error('password', 'Invalid password')
            else:
                user.delete()
                logout(request)
                return redirect("index")
    else:
        form = DeleteForm()

    return render(request, "users/delete.html", { "form": form })
