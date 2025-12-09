from .forms import SignUpForm
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def signup(request):
    if request.method == "POST":
       form = SignUpForm(request.POST)
       if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            html_content = render_to_string(
                "users/verification.html",
                context={"username": username},
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