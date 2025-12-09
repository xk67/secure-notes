#from django.urls import reverse_lazy
#from django.views.generic import CreateView
from .forms import SignUpForm
from django.shortcuts import render
from django.core.mail import send_mail

#class SignUpView(CreateView):
#    form_class = SignUpForm
#    success_url = reverse_lazy("login")

def signup(request):
    if request.method == "POST":
       form = SignUpForm(request.POST)
       if form.is_valid():
            form.save()

            email = form.cleaned_data['email']

            send_mail(
                "dev test",
                "Here is the message.",
                "dev@secure-notes.dev",
                [email],
                fail_silently=False,
            )
    else:
        form = SignUpForm
    
    return render(request, 'users/signup.html', {'form': form})