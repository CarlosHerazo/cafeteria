from django.db.models.signals import post_migrate
from django.dispatch import receiver
from cafe_app.models import Empleado, Cafeteria, Usuario
from django.contrib.auth.hashers import make_password

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):

    if not Cafeteria.objects.exists():
            # Crear cafetería si no existe
            Cafeteria.objects.create(nombre="Cafeteria Casa del marques", direccion="Cra. 5 #33-15, El Centro, Cartagena de Indias, Provincia de Cartagena, Bolívar")
            print("Cafetería creada con éxito.")
    
    if sender.name == "cafe_app":  # Asegúrate de que la señal proviene de tu aplicación específica

        if not Empleado.objects.filter(cedula='202020').exists():
            # Crear usuario administrador si no existe
            Empleado.objects.create(cedula='202020', nombre='senaCoffe', direccion='Cra. 5 #33-15, El Centro, Cartagena de Indias, Provincia de Cartagena, Bolívar', telefono='', rol='admin', cafeteria_id=1)
            print("Usuario creado con éxito.")

        if not Usuario.objects.filter(usuario='senaCoffeAdmin').exists():
            # Crear usuario administrador si no existe
            Usuario.objects.create(correo='senacoffeMarques@gmail.com', contrasena=make_password("senaCoffe2024*"), usuario="senaCoffeAdmin", empleado_id='202020')
            print("Usuario creado con éxito.")     
        
        

       
        