"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello_view, name='hello'), # test endpoint
    path('api/identify-chord/', views.identify_chord, name='identify_chord'), # generating chord from notes
    path('api/gen-progression/', views.generate_chord_progression, name='generate-chord-progression'), # generating chords in a key
    path('api/auth/', views.auth, name="auth"), # login auth
    path('api/signup/', views.save_user, name="save_user"), # saving user to db
]
