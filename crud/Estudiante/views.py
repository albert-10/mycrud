from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .models import Estudiante
from .serializers import EstudianteSerializer, UsuarioSerializer, PermisoSerializer, MostrarUsuarioSerializer, ObtenerUsuarioSerializer
from .permisos import PermisoGestionGeneral, PermisoGestion, PermisoVisualizador
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# El siguiente metodo muestra la pagina inicial de la aplicacion

def inicio(request):
    return render(request, 'inicio.html')

# La siguiente clase permitira insertar estudiantes

class CrearEstudiante(generics.CreateAPIView):
    serializer_class = EstudianteSerializer
    permission_classes = ( PermisoGestionGeneral | PermisoGestion,) 
    
# La siguiente clase permitira mostrar estudiantes

class ListarEstudiantes(generics.ListAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = ( PermisoGestionGeneral | PermisoGestion | PermisoVisualizador,) 

# La siguiente clase permitira eliminar u obtener un estudiante

class EstudianteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = ( PermisoGestionGeneral | PermisoGestion,)

# La siguiente clase permitira insertar, eliminar, obtener y editar usuarios

class AdminUsuario(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer 
    permission_classes = ( PermisoGestionGeneral,)
   

# La siguiente clase permitira mostrar usuarios con sus permisos

class ListarUsuarios(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = MostrarUsuarioSerializer
    permission_classes = ( PermisoGestionGeneral | PermisoGestion,)


# La siguiente clase permitira obtener un usuario con sus permisos

class ObtenerUsuario(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ObtenerUsuarioSerializer
    permission_classes = ( PermisoGestionGeneral,)


# La siguiente clase permitira mostrar permisos

class ListarPermisos(generics.ListAPIView):
    queryset = Permission.objects.filter(Q(name='Gestion') | Q(name='Gestion General') | Q(name='Visualizador'))
    serializer_class = PermisoSerializer
    permission_classes = ( PermisoGestionGeneral,) 


# La siguiente clase permite que los usuarios se autentiquen

class Autenticar(APIView):  
    permission_classes = ()


    """  El siguiente metodo recibe como argumento las credenciales de un usuario que desea autenticarse, si estas estan co-
    rrectas, el metodo retorna: el username del usuario, su permiso y un token para el usuario. Si las credenciales es-
    tan incorrectas el metodo retorna un mensaje de error. """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        usuario = authenticate(username=username, password=password)
        
        if usuario is not None:         
            token, _ = Token.objects.get_or_create(user=usuario)
            user = self.getUser(username)
            permiso = self.getPermiso(user)
            return Response({'token': token.key, 'username': username, 'permiso': permiso})
        else:
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)

    # El siguiente metodo resive el username de un usuario y retorna el usuario poseedor del username

    def getUser(self, username):
        return User.objects.get(username=username)

    # El siguiente metodo recibe como argumento un User y retorna el permiso de ese User

    def getPermiso(self, user):
        return ObtenerUsuarioSerializer(user).data['user_permissions'][0].popitem()[1]

# La siguiente clase permite que el token asosiado a un usuario, se elimine, es decir eliminar la sesion del usuario

class SalirSesion(APIView):
    permission_classes = ()

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"Salio de sesion": "ok"}) 

# La siguiente clase se ejecuta cuando al escribir una url en el navegador no matchea con ninguna url. Esta clase nos
# conducira al inicio.html, que es donde se encuentra la aplicacion de angular. Esta clase generalmente es llamada cuando
# se recarga la pagina y en el navegador se encuentra una url de angular la cual no coincide con ninguna url de django,
# por lo tanto se ejecuta en Estudiante/url.py la url: re_path(r'^.*$'... la cual esta asociada a esta clase. Esto permiti-
# ra que se muestre la pagina de inicio de angular con el componente colocado en: <router-outlet></router-outlet>


class PassToAngular(TemplateView):
    
    def get(self, request, **kwargs):
        return render(request, 'inicio.html', context= {})

""" def passToAngular(self, request, **kwargs):
    return render(request, 'inicio.html', context= None) """