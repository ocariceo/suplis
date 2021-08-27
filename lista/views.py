from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from . models import Producto

class ListaProducto(LoginRequiredMixin, ListView):
    model = Producto
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = context['producto'].filter(user=self.request.user)
        context['count'] = context['producto'].filter(comprado=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['producto'] = context['producto'].filter(producto__icontains = search_input)
            context['search_input'] = search_input
        return context
    

class DetalleProducto(LoginRequiredMixin, DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name= 'lista/producto.html'

class CrearProducto(LoginRequiredMixin, CreateView):
    model = Producto
    fields = ['producto', 'marca', 'cantidad']
    success_url = reverse_lazy('producto')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CrearProducto, self).form_valid(form)

class ActualizarProducto(LoginRequiredMixin, UpdateView):
    model = Producto
    #fields = "__all__"
    fields = ['producto', 'marca', 'cantidad', 'comprado']
    success_url = reverse_lazy('producto')

class BorrarProducto(LoginRequiredMixin, DeleteView):
    model = Producto
    context_object_name = 'producto'
    success_url = reverse_lazy('producto')

class CustomLoginView(LoginView):
    template_name = 'lista/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('producto')

class PaginaRegistro(FormView):
    template_name = 'lista/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('producto')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(PaginaRegistro, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('producto')
        return super(PaginaRegistro, self).get(*args, *kwargs)

