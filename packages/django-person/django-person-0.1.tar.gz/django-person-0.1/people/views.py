from django.shortcuts import render
from django.views.generic.edit import CreateView
from django import forms
from django.utils import timezone 
from people.models import Person 

# Create your views here.

class PersonCreate(CreateView):
    model = Person 
    fields = ['first_name', 'last_name', 'email', 'password'] 
    success_url = '/ideas/'

    def get_form(self, form_class=None):
        form = super(PersonCreate, self).get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.set_password(form.cleaned_data.get('password', None))
        self.object.date_joined = timezone.now() 
        self.object.save()
        return super(PersonCreate, self).form_valid(form)


