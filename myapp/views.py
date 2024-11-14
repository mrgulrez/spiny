from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, CarImage
from django.db import models
from .forms import CarForm, CarImageForm
from django.forms import modelformset_factory

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView




class BaseView(View):
    template_name = None

    def get(self, request):
        return render(request, self.template_name, {})

class IndexView(LoginRequiredMixin, BaseView):
    template_name = 'myapp/index.html'

class AboutView(BaseView):
    template_name = 'myapp/about.html'

class ContactView(BaseView):
    template_name = 'myapp/contact.html'


class FeaturesView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'myapp/features.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = Car.objects.filter(user=self.request.user)
        
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(car_type__icontains=query)
            )
        return queryset



    



@login_required
def add_car(request):
    CarImageFormSet = modelformset_factory(CarImage, form=CarImageForm, extra=10, max_num=10)
    if request.method == 'POST':
        car_form = CarForm(request.POST)
        formset = CarImageFormSet(request.POST, request.FILES, queryset=CarImage.objects.none())
        if car_form.is_valid() and formset.is_valid():
            car = car_form.save(commit=False)
            car.user = request.user
            car.save()
            for form in formset:
                if form.cleaned_data.get('image'):
                    image = form.save(commit=False)
                    image.car = car
                    image.save()
            return redirect('myapp:features')
    else:
        car_form = CarForm()
        formset = CarImageFormSet(queryset=CarImage.objects.none())
    return render(request, 'myapp/add_car.html', {'car_form': car_form, 'formset': formset})



@login_required
def car_list(request):
    cars = Car.objects.filter(user=request.user)
    query = request.GET.get('search')
    if query:
        cars = cars.filter(models.Q(title__icontains=query) | models.Q(description__icontains=query) | models.Q(car_type__icontains=query))


    return render(request, 'myapp/car_list.html', {'cars': cars})


@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk, user=request.user)
    return render(request, 'myapp/car_detail.html', {'car': car})

def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk, user=request.user)
    CarImageFormSet = modelformset_factory(CarImage, form=CarImageForm, extra=10, max_num=10)
    
    if request.method == 'POST':
        car_form = CarForm(request.POST, instance=car)
        formset = CarImageFormSet(request.POST, request.FILES, queryset=car.images.all())
        
        if car_form.is_valid() and formset.is_valid():
            car_form.save() 
            
            for form in formset:
                image = form.save(commit=False) 
                image.car = car 
                image.save() 
            
            return redirect('myapp:car_detail', pk=car.pk)
    else:
        car_form = CarForm(instance=car)
        formset = CarImageFormSet(queryset=car.images.all())

    return render(request, 'myapp/edit_car.html', {
        'car_form': car_form,
        'formset': formset
    })


@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk, user=request.user)
    car.delete()
    return redirect('myapp:features')
