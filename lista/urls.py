from django.urls import path
from .views import ListaProducto, DetalleProducto, CrearProducto, ActualizarProducto, BorrarProducto, CustomLoginView, PaginaRegistro
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', ListaProducto.as_view(), name="producto"),
    path('crear-producto/', CrearProducto.as_view(), name="crear-producto"),
    path('login/', CustomLoginView.as_view(), name="login"),    
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),        
    path('registro/', PaginaRegistro.as_view(), name="registro"),
    path('producto/<int:pk>/', DetalleProducto.as_view(), name="detalle-producto"),
    path('actualizar-producto/<int:pk>/', ActualizarProducto.as_view(), name="actualizar-producto"),
    path('borrar-producto/<int:pk>/', BorrarProducto.as_view(), name="borrar-producto")


]

