from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from mainapp.forms import AddUserForm, LoginForm, AddNewAppForm, AddNewHardwereForm, NewTechTicket, NewAppTicket
from mainapp.models import CustomUser, App, Tech, Techticket, Appticket


# Create your views here.
class Register(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, template_name='register.html', context={'form': form})

    def post(self, request):
        user_form = AddUserForm(request.POST)

        if user_form.is_valid():
            user = CustomUser()
            user.username = user_form.cleaned_data['email']
            user.email = user_form.cleaned_data['email']

            split_email = user_form.cleaned_data['email'].split('.')
            user.first_name = split_email[0]
            user.last_name = split_email[1]

            user.department = user_form.cleaned_data['department']
            user.code = user_form.cleaned_data['code']

            if user_form.cleaned_data['password'] == user_form.cleaned_data['repassword']:
                user.set_password(user_form.cleaned_data['password'])
            else:
                return redirect('register')

            if user_form.cleaned_data['department'] == 'Management':
                user.is_staff = True
            elif user_form.cleaned_data['department'] == 'IT':
                user.is_staff = True
                user.is_superuser = True

            user.save()
            return redirect('login')

        return redirect('register')


class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, template_name='login.html', context={'form':form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('main')
        return render(request, template_name='login.html')


class MainpageView(LoginRequiredMixin,View):
    def get(self, request):
        alltechtickets = Techticket.objects.filter(status='Pending').count()
        allapptickets = Appticket.objects.filter(status='Pending').count()
        allusers = CustomUser.objects.count()

        context = {
            'alltechtickets': alltechtickets,
            'allapptickets': allapptickets,
            'allusers': allusers
        }

        return render(request, template_name='mainpage.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, template_name='logout.html')


class ChooseFormView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='chooseform.html')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        person_id = request.user.id
        person = CustomUser.objects.get(id=person_id)
        first_name = str(person.first_name)
        last_name = str(person.last_name)
        person_name = (first_name + " " + last_name).upper()
        print(person_name)

        person_tech_tickets = Techticket.objects.filter(author=person, status='Approved')
        person_app_tickets = Appticket.objects.filter(author=person, status='Approved')

        return render(request, template_name='profile.html', context={'person': person, 'person_name':person_name, 'person_tech_tickets': person_tech_tickets, 'person_app_tickets': person_app_tickets })


class AddNewChooseView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='choosenewform.html')


class AddAppView(LoginRequiredMixin, View):
    def get(self, request):
        AddNewAppForm()
        return render(request, template_name='addapp.html', context={'form': AddNewAppForm})

    def post(self, request):
        form = AddNewAppForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            icon = form.cleaned_data['icon']

            new_app = App(name=name, desc=desc, icon=icon)
            new_app.save()

        return redirect('allapps')


class AllAppsView(LoginRequiredMixin, ListView):
    model = App
    template_name = 'allapps.html'
    context_object_name = 'apps'


class AddNewHardwereView(LoginRequiredMixin, View):
    def get(self, request):
        AddNewHardwereForm()
        return render(request, template_name='addhardwere.html', context={'form': AddNewHardwereForm})

    def post(self, request):
        form = AddNewHardwereForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            icon = form.cleaned_data['icon']

            new_hardwere = Tech(name=name, desc=desc, icon=icon)
            new_hardwere.save()

        return redirect('allhardwere')


class AllHardwereView(LoginRequiredMixin, ListView):
    model = Tech
    template_name = 'allhardwere.html'
    context_object_name = 'techs'


class NewTechTicketView(LoginRequiredMixin, View):
    def get(self, request):
        NewTechTicket()
        return render(request, template_name='techticket.html', context={'form': NewTechTicket})

    def post(self, request):
        form = NewTechTicket(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']

            person_id = request.user.id
            person = CustomUser.objects.get(id=person_id)
            author = person

            comment = form.cleaned_data['comment']
            status = "Pending"

            new_tech_ticket = Techticket(item=item, author=author, comment=comment,status=status)
            new_tech_ticket.save()

        return redirect('persontickets')


class AllTechTicketsView(LoginRequiredMixin, ListView):
    model = Techticket
    template_name = 'alltechtickets.html'
    context_object_name = 'techtickets'

    def get_queryset(self):
        return Techticket.objects.all().order_by('-created')


class NewAppTicketView(LoginRequiredMixin, View):
    def get(self, request):
        NewAppTicket()
        return render(request, template_name='appticket.html', context={'form': NewAppTicket})

    def post(self, request):
        form = NewAppTicket(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']

            person_id = request.user.id
            person = CustomUser.objects.get(id=person_id)
            author = person

            comment = form.cleaned_data['comment']
            status = "Pending"

            new_tech_ticket = Appticket(item=item, author=author, comment=comment,status=status)
            new_tech_ticket.save()

        return redirect('persontickets')


class AllAppTicketsView(LoginRequiredMixin, ListView):
    model = Appticket
    template_name = 'allapptickets.html'
    context_object_name = 'apptickets'

    def get_queryset(self):
        return Appticket.objects.all().order_by('-created')


class AllEmployeeTicketsView(LoginRequiredMixin, View):
    def get(self, request):
        person = request.user.id

        apptickets = Appticket.objects.filter(author=person)

        techtickets = Techticket.objects.filter(author=person)

        context = {'person':person, 'apptickets': apptickets, 'techtickets': techtickets}

        return render(request, template_name='persontickets.html', context=context)


class AppView(LoginRequiredMixin, View):
    def get(self, request, id):
        app = App.objects.get(id=id)
        return render(request, template_name='app.html', context={'app':app})


class AppTicketView(LoginRequiredMixin, View):
    def get(self, request, id):
        appticket = Appticket.objects.get(id=id)
        return render(request, template_name='appticketdetails.html', context={'appticket': appticket})

    def post(self, request, id):
        feedback = request.POST.get('feedback')
        appticket = Appticket.objects.get(id=id)
        app = appticket.item

        if 'negative' in request.POST :
            appticket.feedback = feedback
            appticket.status = 'Rejected'
            appticket.save()
            return redirect('apptickets')
        elif 'positive' in request.POST:
            appticket.feedback = feedback
            appticket.status = 'Approved'
            appticket.save()

            app.tickets.add(appticket)

            return redirect('apptickets')


class TechView(LoginRequiredMixin, View):
    def get(self, request, id):
        tech = Tech.objects.get(id=id)
        return render(request, template_name='tech.html', context={'tech': tech})


class TechTicketView(LoginRequiredMixin, View):
    def get(self, request, id):
        techticket = Techticket.objects.get(id=id)
        return render(request, template_name='techticketdetails.html', context={'techticket': techticket})

    def post(self, request, id):
        feedback = request.POST.get('feedback')
        techticket = Techticket.objects.get(id=id)
        tech = techticket.item

        if 'negative' in request.POST :
            techticket.feedback = feedback
            techticket.status = 'Rejected'
            techticket.save()
            return redirect('techtickets')
        elif 'positive' in request.POST:
            techticket.feedback = feedback
            techticket.status = 'Approved'
            techticket.save()

            tech.tickets.add(techticket)

            return redirect('techtickets')


class MyAppView(LoginRequiredMixin, View):
    def get(self, request, id):
        app = App.objects.get(id=id)
        return render(request, template_name='myapp.html', context={'app': app})

    def post(self, request, id):

        current_user = request.user
        item = App.objects.get(pk=id)

        app_ticket = Appticket.objects.filter(author=current_user, item=item, status='Approved').first()
        app_ticket.status = 'Returned/Removed'
        app_ticket.save()

        return redirect('profile')


class MyTechView(LoginRequiredMixin, View):
    def get(self, request, id):
        tech = Tech.objects.get(id=id)
        return render(request, template_name='mytech.html', context={'tech': tech})

    def post(self, request, id):
        current_user = request.user
        item = Tech.objects.get(pk=id)

        tech_ticket = Techticket.objects.filter(author=current_user, item=item, status='Approved').first()
        tech_ticket.status = 'Returned/Removed'
        tech_ticket.save()

        return redirect('profile')


class EqView(View):
    def get(self, request):
        return render(request, template_name='eq.html')


class OfficeView(View):
    def get(self, request):
        return render(request, template_name='office.html')


class SalesHelpView(View):
    def get(self, request):
        return render(request, template_name='saleshelp.html')


