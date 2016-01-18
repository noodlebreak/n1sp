# coding: utf-8

from theapp.models import *
usernames = ['jack', 'ginny', 'ralph']
passwords = ['password'] * 5
locations = ['Delhi', 'Noida', 'Bangalore']
emails = ['jack@mail.com', 'ginny@mail.com',
          'ralph@mail.com']
for loc in locations:
    City.objects.create(name=loc)
cities = City.objects.all()
for un, pwd, email, loc in zip(usernames, passwords, emails, cities):
    user = User(username=un, location=loc, email=email)
    user.set_password(pwd)
    user.save()
at1_group = Group.objects.create(name='AdminType1')
at2_group = Group.objects.create(name='AdminType2')

admin_L1 = User.objects.create_superuser(
    username='admin_l1', email='l1@admin.com',
    password='pass', location=City.objects.last())
admin_L2 = User.objects.create_superuser(
    username='admin_l2', email='gmail@superman.com',
    password='pass', location=City.objects.last())

admin_L1.groups.add(at1_group)
admin_L2.groups.add(at2_group)
