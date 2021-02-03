from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework import status


# La siguiente clase permite manejar el permisos que poseen los Gestores Generales

class PermisoGestionGeneral(permissions.BasePermission):
    
    '''
    El siguiente metodo comprueba que el usuario este autenticado y tenga el permiso de Gestion General. Si el usuario cum-
    ple con las condiciones tendra el permiso, de lo contrario se lanzaran excepciones de usuario no autenticado o usuario
    sin permiso
    '''
    
    def has_permission(self, request, view):              
        try:            
            nombrePermiso = request.user.user_permissions.all()[0].name                    
        except:
            raise NotAuthenticated
        if nombrePermiso =='Gestion General':
            return True
        return False

class PermisoGestion(permissions.BasePermission):
    
    '''
    El siguiente metodo comprueba que el usuario este autenticado y tenga el permiso de Gestion. Si el usuario cumple con
    las condiciones tendra el permiso, de lo contrario se lanzaran excepciones de usuario no autenticado o usuario sin per-
    miso
    '''
    
    def has_permission(self, request, view):
        try:
            nombrePermiso = request.user.user_permissions.all()[0].name
        except:
            raise NotAuthenticated
        if nombrePermiso == 'Gestion':
            return True
        return False

class PermisoVisualizador(permissions.BasePermission):
    
    '''
    El siguiente metodo comprueba que el usuario este autenticado y tenga el permiso de Gestion. Si el usuario cumple con
    las condiciones tendra el permiso, de lo contrario se lanzaran excepciones de usuario no autenticado o usuario sin per-
    miso
    '''
    
    def has_permission(self, request, view):   
        try:
            nombrePermiso = request.user.user_permissions.all()[0].name
        except:
            raise NotAuthenticated
        if nombrePermiso =='Visualizador':
            return True
        return False