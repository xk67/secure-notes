from .forms import SignUpForm
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.http import Http404

User = get_user_model()

def signup(request):
    if request.method == "POST":
       form = SignUpForm(request.POST)
       if form.is_valid():
            user = form.save()

            username = user.username
            email = user.email
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            html_content = render_to_string(
                "users/verification.html",
                context={"username": username, "domain": domain,"uid": uid, "token": token},
            )
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                "Email Verification",
                text_content,
                "from@example.com",
                ["to@example.com"],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()
    else:
        form = SignUpForm
    
    return render(request, 'users/signup.html', {'form': form})

def verify(request, uidb64, token):

    # Use a try block because handle user input, base64 decoding or missing users can cause errors
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user.username)
    except:
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "users/verification_confirm.html")

    # Return 404 for invalid tokens or non-existent users
    raise Http404()