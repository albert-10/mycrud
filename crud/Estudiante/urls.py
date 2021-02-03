from django.urls import path, include, re_path
from Estudiante import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt


import os
from django.conf.urls.static import static
from crud.settings import BASE_DIR
from crud.settings import DEBUG
from crud.settings import STATIC_ROOT

router = DefaultRouter()
router.register(r'adminUsuario', views.AdminUsuario)
router.register(r'obtenerUsuario', views.ObtenerUsuario)

urlpatterns = [
    path('estudiantes', views.ListarEstudiantes.as_view()),
    path('crearEstudiante', views.CrearEstudiante.as_view()),
    path('eliminarEstudiante/<int:pk>', views.EstudianteDetail.as_view()),
    path('obtenerEstudiante/<int:pk>', views.EstudianteDetail.as_view()),
    path('editarEstudiante/<int:pk>', views.EstudianteDetail.as_view()),
    path('eliminarEstudiante/<int:pk>', views.EstudianteDetail.as_view()),
    path('usuarios', views.ListarUsuarios.as_view()),
    path('permisos', views.ListarPermisos.as_view()), 
    path('autenticar', views.Autenticar.as_view(), name='autenticar'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('salirSesion',  views.SalirSesion.as_view()),    
]

urlpatterns += router.urls

# A continuacion agregamos un path comodin a urlpatterns. Este path se emplea para mostrar el template vista inicio.html
# donde se encuentra la aplicacion de Angular. Esta se usa por ejemplo cuando recargamos una pagina, donde la url del na-
# vegador son las rutas de angular, por lo tanto no van a matchear con las url de django. En ese caso se quiere que se na-
# vegue hacia el componente inicial de angular

urlpatterns += [re_path(r'^.*', views.PassToAngular.as_view())]