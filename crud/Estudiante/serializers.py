from rest_framework import serializers
from .models import Estudiante
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from rest_framework.authtoken.models import Token



class EstudianteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estudiante
        fields = '__all__'

# El siguiente serializer permite serializar usuarios     

class UsuarioSerializer(serializers.ModelSerializer):

    '''
    En la siguiete clase Meta especificamos los atributo del model Usuario a serializar. Tambien
    especificamos que el atributo password solo sea de escritura
    '''

    class Meta:
        model = User
        fields = ('pk','username', 'password', 'user_permissions')
        extra_kwargs = {'password' : {'write_only': True}}
        
    # El siguiente metodo permite crear un user

    def create(self, validated_data):
            usuario = User(
                username = validated_data['username'],
                password = validated_data['password'],
            )

            usuario.set_password(raw_password=validated_data['password'])
            usuario.save()
            usuario.user_permissions.set(validated_data['user_permissions'])          
            return usuario

    '''
    El siguiente metodo recibe como argumento un model Usuario y el nombre de un grupo. Aqui asignamos el
    grupo al usuario
    '''

    def agregarPermiso(self, usuario, permisoPk):        
        usuario.user_permissions.set([permisoPk])

    '''
    A continuacion sobrescribimos el metodo update() de ModelSerializer. De esta forma logramos editar
    el password del usuario con forma de hash. Tambien podemos editar su permiso, ademas de su username
    '''

    def update(self, instance, validated_data):        
        instance.username = validated_data.get('username',instance.username)      
        if 'password' in validated_data:
            instance.set_password(raw_password=validated_data.get('password',instance.password))
        if 'user_permissions' in validated_data:            
            instance.user_permissions.clear()
            permisoPk = validated_data.get('user_permissions',instance.user_permissions)[0]
            self.agregarPermiso(instance, permisoPk)  
    
        instance.save()
        return instance

# El siguiente serializer permite serializar permisos

class PermisoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('pk', 'name')

# El siguiente serializer permite serializar los usuarios, para que estos se muestren con todos los atributos de Per-
# mission

class MostrarUsuarioSerializer(serializers.ModelSerializer):

    user_permissions = PermisoSerializer(many=True)

    class Meta:
        model = User
        fields = ('pk','username', 'user_permissions')

# El siguiente serializer permite serializar un usuarios, para que estos se muestren con todos los atributos de Per-
# mission

class ObtenerUsuarioSerializer(serializers.ModelSerializer):

    user_permissions = PermisoSerializer(many=True)

    class Meta:
        model = User
        fields = ('pk','username', 'user_permissions')