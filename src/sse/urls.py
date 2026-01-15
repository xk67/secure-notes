"""
URL configuration for sse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

@require_GET
def index(request):
    if request.user.is_authenticated:
        return redirect('notes:create_note')
    return render(request, 'pages/index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("notes.urls")),
    path("", include("users.urls")),
    path("imprint", TemplateView.as_view(template_name="pages/imprint.html"), name="imprint"),
    path("privacy", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
    path("", index, name="index")
]
