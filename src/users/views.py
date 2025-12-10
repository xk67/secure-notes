from .forms import SignUpForm
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

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