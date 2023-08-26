import os

import pytest
from django.test import Client
from django.urls import reverse
from mainapp.views import *
from mainapp.views import CustomUser
from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def custom_user():
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
        department='testdepartment',
        code='12345678'
    )


User = get_user_model()


@pytest.mark.django_db
def test_user_registration_form(client):

    path = reverse('register')
    response = client.post(path, {
        'email': 'new.user.it@td.com',
        'password': 'newpassword',
        'repassword': 'newpassword',
        'department': 'IT',
        'code': 'NU765432'
    })

    assert response.status_code == 302
    assert User.objects.all().count() == 1


@pytest.mark.django_db
def test_user_login(client, custom_user):

    path_main = reverse('main')
    client.force_login(custom_user)
    response_main = client.get(path_main)
    assert response_main.status_code == 200
    assert custom_user.is_authenticated


@pytest.mark.django_db
def test_user_logout(client, custom_user):
    path_logout = reverse('logout')
    client.force_login(custom_user)
    response_logout = client.get(path_logout)
    assert response_logout.status_code == 200
    assert not response_logout.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_add_new_app_and_upload_image_form(client, custom_user):
    client.force_login(custom_user)

    image = Image.new('RGB', (100, 100), 'white')
    image_io = BytesIO()
    image.save(image_io, format='PNG')

    icon_file = SimpleUploadedFile('test_icon.png', image_io.getvalue())

    form_data = {
        'name': 'Test App',
        'desc': 'Test Description'
    }

    form_files = {'icon': icon_file}

    form = AddNewAppForm(data=form_data, files=form_files)

    if form.is_valid():
        form.save()
    app_count = App.objects.count()
    assert app_count == 1

    response = client.post(reverse('addapp'), form_data)

    expected_url = reverse('allapps')
    assert response.status_code == 302
    assert response.url == expected_url

    form_data2 = {
        'name': 'Test App2',
        'desc': 'Test Description',
        'icon': 'icon.png'
    }

    response = client.post(reverse('addapp'), form_data2)

    expected_url = reverse('allapps')
    assert response.status_code == 302
    assert response.url == expected_url

@pytest.mark.django_db
def test_add_new_hardwere_upload_image_form(client, custom_user):
    client.force_login(custom_user)
    path = reverse('addhardwere')
    response = client.get(path, follow=True)

    assert response.status_code == 200

    image = Image.new('RGB', (100, 100), 'white')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    icon_file = SimpleUploadedFile('test_icon.png', image_io.getvalue(), content_type='image/jpeg')

    form_data = {'name': 'test_hw', 'desc': 'test', 'icon': icon_file}

    response_post = client.post(path, form_data)

    tech_count = Tech.objects.count()
    assert tech_count == 1

@pytest.mark.django_db
def test_add_new_app_upload_image_form(client, custom_user):
    client.force_login(custom_user)
    path = reverse('addapp')
    response = client.get(path, follow=True)

    assert response.status_code == 200

    image = Image.new('RGB', (100, 100), 'white')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    icon_file = SimpleUploadedFile('test_icon.png', image_io.getvalue(), content_type='image/jpeg')

    form_data = {'name': 'test_hw', 'desc': 'test', 'icon': icon_file}

    response_post = client.post(path, form_data)

    app_count = App.objects.count()
    assert app_count == 1

@pytest.mark.django_db
def test_add_new_hardwere_and_upload_image_form(client, custom_user):
    client.force_login(custom_user)

    image = Image.new('RGB', (100, 100), 'white')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')

    icon_file = SimpleUploadedFile('test_icon.png', image_io.getvalue(), content_type='image/jpeg')

    form_data = {
        'name': 'Test Tech',
        'desc': 'Test Description'

    }

    form_files = {'icon': icon_file}

    form = AddNewHardwereForm(data=form_data, files=form_files)

    if form.is_valid():
        form.save()
    tech_count = Tech.objects.count()
    assert tech_count == 1

    response = client.post(reverse('addhardwere'), form_data)

    expected_url = reverse('allhardwere')
    assert response.status_code == 302
    assert response.url == expected_url


@pytest.mark.django_db
def test_new_app_ticket_form_with_post(client, custom_user):
    client.force_login(custom_user)

    app = App.objects.create(name='Test App', desc='Test Description', icon='test_icon.png')
    form_data = {
        'item': app.id,
        'comment': 'Test Comment'
    }

    response = client.post(reverse('newappticket'), form_data)

    app_ticket_count = Appticket.objects.count()

    expected_url = reverse('persontickets')

    assert app_ticket_count == 1
    assert response.status_code == 302
    assert response.url == expected_url


@pytest.mark.django_db
def test_new_app_ticket_form_with_post(client, custom_user):
    client.force_login(custom_user)

    app = App.objects.create(name='Test App', desc='Test Description', icon='test_icon.png')
    form_data = {
        'item': app.id,
        'comment': 'Test Comment'
    }

    response = client.post(reverse('newappticket'), form_data)

    app_ticket_count = Appticket.objects.count()

    expected_url = reverse('persontickets')

    assert app_ticket_count == 1
    assert response.status_code == 302
    assert response.url == expected_url


@pytest.mark.django_db
def test_update_tech_ticket(client, custom_user):
    client.force_login(custom_user)

    tech = Tech.objects.create(name='Test Tech', desc='Test Description', icon='test_icon.png')

    tech_ticket = Techticket.objects.create(
        item=tech,
        author=custom_user,
        comment='Test Comment',
        status='Pending'
    )

    url = reverse('techticketdetails', kwargs={'id': tech_ticket.id})
    response = client.get(url)

    assert response.status_code == 200

    updated_feedback = 'Test Feedback'
    updated_status = 'Approved'
    response = client.post(url, {'feedback': updated_feedback,'status':updated_status, 'positive': 'Submit'})

    tech_ticket.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('techtickets')
    assert tech_ticket.feedback == updated_feedback
    assert tech_ticket.status == updated_status

    tech2 = Tech.objects.create(name='Test Tech', desc='Test Description', icon='test_icon.png')

    tech_ticket2 = Techticket.objects.create(
        item=tech2,
        author=custom_user,
        comment='Test Comment',
        status='Pending'
    )

    url = reverse('techticketdetails', kwargs={'id': tech_ticket2.id})
    response = client.get(url)

    assert response.status_code == 200

    updated_feedback = 'Test Feedback'
    updated_status = 'Rejected'
    response = client.post(url, {'feedback': updated_feedback,'status':updated_status, 'negative': 'Submit'})

    tech_ticket2.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('techtickets')
    assert tech_ticket2.feedback == updated_feedback
    assert tech_ticket2.status == updated_status


@pytest.mark.django_db
def test_update_app_ticket(client, custom_user):
    client.force_login(custom_user)

    app = App.objects.create(name='Test App', desc='Test Description', icon='test_icon.png')

    app_ticket = Appticket.objects.create(
        item=app,
        author=custom_user,
        comment='Test Comment',
        status='Pending'
    )

    url = reverse('appticketdetails', kwargs={'id': app_ticket.id})
    response = client.get(url)

    assert response.status_code == 200

    updated_feedback = 'Test Feedback'
    updated_status = 'Approved'
    response = client.post(url, {'feedback': updated_feedback,'status':updated_status, 'positive': 'Submit'})

    app_ticket.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('apptickets')
    assert app_ticket.feedback == updated_feedback
    assert app_ticket.status == updated_status

    app2 = App.objects.create(name='Test App', desc='Test Description', icon='test_icon.png')

    app_ticket2 = Appticket.objects.create(
        item=app2,
        author=custom_user,
        comment='Test Comment',
        status='Pending'
    )

    url = reverse('appticketdetails', kwargs={'id': app_ticket2.id})
    response = client.get(url)

    assert response.status_code == 200

    updated_feedback = 'Test Feedback'
    updated_status = 'Rejected'
    response = client.post(url, {'feedback': updated_feedback, 'status': updated_status, 'negative': 'Submit'})

    app_ticket2.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('apptickets')
    assert app_ticket2.feedback == updated_feedback
    assert app_ticket2.status == updated_status

@pytest.mark.django_db
def test_delete_tech(custom_user, client):
    tech5 = Tech.objects.create(name='Test Tech5', desc='Test Description', icon='test_icon.png')
    test_tech_ticket5 = Techticket.objects.create(item=tech5, author=custom_user, comment='Test Comment',feedback='OK', status='Approved')
    client.force_login(custom_user)

    response = client.post(reverse('mytech', kwargs={'id': tech5.id}))

    test_tech_ticket5.refresh_from_db()

    expected_url = reverse('profile')
    assert response.status_code == 302
    assert response.url == expected_url
    assert test_tech_ticket5.status == 'Returned/Removed'


@pytest.mark.django_db
def test_delete_app(custom_user, client):
    app = App.objects.create(name='Test App', desc='Test Description', icon='test_icon.png')
    test_app_ticket = Appticket.objects.create(item=app, author=custom_user, comment='Test Comment',feedback='OK', status='Approved')

    client.force_login(custom_user)

    response = client.post(reverse('myapp', kwargs={'id': app.id}))

    test_app_ticket.refresh_from_db()

    expected_url = reverse('profile')
    assert response.status_code == 302
    assert response.url == expected_url
    assert test_app_ticket.status == 'Returned/Removed'


@pytest.mark.django_db
def test_profile_view(client, custom_user):
    client.force_login(custom_user)

    client.login(username='testuser', password='testpassword')

    app = App.objects.create(name='Test App', desc='t', icon='test_icon.png')
    tech = Tech.objects.create(name='Test Tech', desc='t', icon='test_icon.png')
    app_ticket = Appticket.objects.create(item=app, author=custom_user, comment='Test Comment',feedback='OK', status='Approved')
    tech_ticket = Techticket.objects.create(item=tech, author=custom_user, comment='Test Comment',feedback='OK', status='Approved')

    response = client.get(reverse('profile'))
    assert response.status_code == 200

    person_tech_tickets_count = response.context['person_tech_tickets'].count()
    person_app_tickets_count = response.context['person_app_tickets'].count()

    assert person_tech_tickets_count == 1
    assert person_app_tickets_count == 1


@pytest.mark.django_db
def test_mainpage_and_counters_view(client, custom_user):
    client.force_login(custom_user)
    app = App.objects.create(name='Test App', desc='t', icon='test_icon.png')
    tech = Tech.objects.create(name='Test Tech', desc='t', icon='test_icon.png')
    app_ticket = Appticket.objects.create(author=custom_user, item=app, comment='OK', status='Pending')
    tech_ticket1 = Techticket.objects.create(author=custom_user, item=tech,comment='OK', status='Pending')
    tech_ticket2 = Techticket.objects.create(author=custom_user, item=tech,comment='OK', status='Pending')

    response = client.get(reverse('main'))
    assert response.status_code == 200

    context = response.context

    all_users_count = context['allusers']
    all_app_tickets_count = context['allapptickets']
    all_tech_tickets_count = context['alltechtickets']

    assert all_users_count == 1
    assert all_app_tickets_count == 1
    assert all_tech_tickets_count == 2


@pytest.mark.parametrize("view_name", [
    'login',
    'register',
    'main',
    'chooseform',
    'profile',
    'choosenewform',
    'addapp',
    'allapps',
    'addhardwere',
    'allhardwere',
    'newtechticket',
    'techtickets',
    'newappticket',
    'apptickets',
    'persontickets',
    'eqandapps',
    'office',
    'saleshelp',
])
@pytest.mark.django_db
def test_views_without_id(client, custom_user, view_name):
    client.force_login(custom_user)

    app = App.objects.create(name='Test App', desc='t', icon='test_icon.png')
    tech = Tech.objects.create(name='Test Tech', desc='t', icon='test_icon.png')
    app_ticket = Appticket.objects.create(author=custom_user, item=app,comment='T', status='Approved')
    tech_ticket = Techticket.objects.create(author=custom_user, item=tech,comment='T', status='Approved')

    if view_name in ['app','tech','appticketdetails','techticketdetails','myapp','mytech',]:
        view = view_name.replace('details', '')
        url = reverse(view, args={'id':1})
    else:
        url = reverse(view_name)

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("view_name, model", [
    ('app', App),
    ('tech', Tech),
    ('appticketdetails', Appticket),
    ('techticketdetails', Techticket),
    ('myapp', App),
    ('mytech', Tech),
])
@pytest.mark.django_db
def test_views_with_id(client, custom_user, view_name, model):
    client.force_login(custom_user)

    app = App.objects.create(name='Test App', desc='t', icon='test_icon.png')
    tech = Tech.objects.create(name='Test Tech', desc='t', icon='test_icon.png')
    app_ticket = Appticket.objects.create(author=custom_user, item=app,comment='T', status='Approved')
    tech_ticket = Techticket.objects.create(author=custom_user, item=tech,comment='T', status='Approved')

    instance = model.objects.first()
    url = reverse(view_name, args=[instance.id])

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("view_name, expected_status", [
    ('login', 200),
    ('register', 200),
    ('main', 302),
    ('chooseform', 302),
    ('profile', 302),
    ('choosenewform', 302),
    ('addapp', 302),
    ('allapps', 302),
    ('addhardwere', 302),
    ('allhardwere', 302),
    ('newtechticket', 302),
    ('techtickets', 302),
    ('newappticket', 302),
    ('apptickets', 302),
    ('persontickets', 302),
    ('eqandapps', 200),
    ('office', 200),
    ('saleshelp', 200),
])
def test_views_without_id(client, view_name, expected_status):
    url = reverse(view_name)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize("view_name, expected_status",[
     ('app', 404),
    ('tech', 404),
    ('appticketdetails', 404),
    ('techticketdetails', 404),
    ('myapp', 404),
    ('mytech', 404)
])
def test_views_with_id(client, view_name, expected_status):

    url = reverse(view_name, args=[1])
    response = client.get(url)
    assert response.status_code in [404, 302]
    assert not response.status_code == 200

