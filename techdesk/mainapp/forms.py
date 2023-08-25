from django import forms
from mainapp.models import CustomUser, App, Tech, Techticket, Appticket


class AddUserForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput,label="Password",)
    repassword = forms.CharField(widget=forms.PasswordInput,label="Re-enter Password")
    code = forms.CharField(label="Employee Code", max_length=8)
    department_choices = (
        ('IT', 'IT'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Management', 'Management'),
        ('Finances', 'Finances'),
        ('HR', 'HR'),
    )
    department = forms.ChoiceField(label="Your Department", choices=department_choices)


class LoginForm(forms.Form):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class AddNewAppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name','desc','icon']


class AddNewHardwereForm(forms.ModelForm):
    class Meta:
        model = Tech
        fields = ['name','desc','icon']


class NewTechTicket(forms.ModelForm):
    class Meta:
        model = Techticket
        fields = ['item','comment']


class NewAppTicket(forms.ModelForm):
    class Meta:
        model = Appticket
        fields = ['item','comment']