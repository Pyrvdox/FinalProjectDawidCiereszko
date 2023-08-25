"""
URL configuration for techdesk project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('main/', MainpageView.as_view(), name='main'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('typeform', ChooseFormView.as_view(), name='chooseform'),
    path('myprofile', ProfileView.as_view(), name='profile'),
    path('typenewform', AddNewChooseView.as_view(), name='choosenewform'),
    path('newapp', AddAppView.as_view(), name="addapp"),
    path('allapps/', AllAppsView.as_view(), name='allapps'),
    path('newhardwere', AddNewHardwereView.as_view(), name="addhardwere"),
    path('allhardwere/', AllHardwereView.as_view(), name='allhardwere'),
    path('newtechticket/', NewTechTicketView.as_view(), name='newtechticket'),
    path('alltechtickets/', AllTechTicketsView.as_view(), name='techtickets'),
    path('newappticket/', NewAppTicketView.as_view(), name='newappticket'),
    path('allapptickets/', AllAppTicketsView.as_view(), name='apptickets'),
    path('employeetickets/', AllEmployeeTicketsView.as_view(), name='persontickets'),
    path('appdetails/<int:id>', AppView.as_view(), name='app'),
    path('techdetails/<int:id>', TechView.as_view(), name='tech'),
    path('appticketdetails/<int:id>', AppTicketView.as_view(), name='appticketdetails'),
    path('techticketdetails/<int:id>', TechTicketView.as_view(), name='techticketdetails'),
    path('myappdetails/<int:id>', MyAppView.as_view(), name='myapp'),
    path('mytechdetails/<int:id>', MyTechView.as_view(), name='mytech'),
    path('eqandapps/', EqView.as_view(),name='eqandapps'),
    path('officerules/', OfficeView.as_view(),name='office'),
    path('saleshelp/', SalesHelpView.as_view(),name='saleshelp')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
