#from django.contrib.auth.models import Usuario 
from django.contrib.auth.models import AbstractUser 
from django.db import models
from django.contrib.auth.hashers import make_password, check_password







# Tabla de Empresa
class Empresa(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        db_table = 'empresa'

    def __str__(self):
        return self.nombre
    

# Tabla de Usuario
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=30)
    rut = models.CharField(max_length=10)
    # Aquí hacemos que 'empresa' sea obligatorio, no permitiendo valores nulos
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        # Hashear la contraseña antes de guardarla
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'usuario'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Tabla de Roles
class Roles(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    permisos = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre

# Tabla de Inventario
class Inventario(models.Model):
    # Aquí también hacemos que 'empresa' sea obligatorio
    id_inventario = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    id_producto = models.IntegerField()
    nombre_producto = models.CharField(max_length=200)
    cantidad_producto = models.FloatField(null=True, blank=True)
    tipo_unidad = models.CharField(max_length=50, null=True, blank=True)       
    class Meta:
        db_table = 'inventario'
        unique_together = ['empresa', 'id_producto']

    def __str__(self):
        return self.nombre_producto
    

# Tabla de Transacciones
class Transaccion(models.Model):
    nombre_producto = models.CharField(max_length=200)
    id_producto = models.IntegerField()
    # Aquí también 'empresa' es obligatorio
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    fecha = models.DateTimeField(auto_now=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'transacciones'

    def __str__(self):
        return f"{self.nombre_producto} ({self.fecha})"

# Tabla de Alertas
class Alertas(models.Model):
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    calidad_alerta = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now=True)
    # Aquí también 'empresa' es obligatorio
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)
    
    class Meta:
        db_table = 'alertas'

    def __str__(self):
        return f"Alerta de {self.empresa.nombre} - {self.calidad_alerta}"












#class Empresa(models.Model):
#    id = models.AutoField(primary_key=True)
#    nombre = models.CharField(max_length=250)

#    class Meta:
#        db_table = 'empresa'

 #   def __str__(self):
#        return self.nombre


#class Usuario(models.Model):
#    id = models.AutoField(primary_key=True)
#    nombre = models.CharField(max_length=100)
#    apellido = models.CharField(max_length=100)
#    rut = models.CharField(max_length=15)
#    username = models.CharField(max_length=100, unique=True)
#    password = models.CharField(max_length=500)  # Hash seguro
#    telefono = models.CharField(max_length=15, blank=True, null=True)
#    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

#    class Meta:
#        db_table = 'usuario'

#    def __str__(self):
#        return self.username


#class Alertas(models.Model):
#    id = models.AutoField(primary_key=True)
#    descripcion = models.CharField(max_length=250, blank=True, null=True)
#    fecha = models.DateTimeField()
#    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

#    class Meta:
#        db_table = 'alertas'

#    def __str__(self):
#        return self.descripcion or "Sin descripción"


#class Inventario(models.Model):
#    id_producto = models.AutoField(primary_key=True)
#    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
#    nombre_producto = models.CharField(max_length=250)
#    cantidad_producto = models.IntegerField()

#    class Meta:
#        db_table = 'inventario'
#        unique_together = ('empresa', 'nombre_producto')  # Asegura unicidad por empresa y nombre de producto

#    def __str__(self):
#        return f"{self.nombre_producto} - {self.empresa.nombre}"


#class Roles(models.Model):
#    id = models.AutoField(primary_key=True)
#    nombre = models.CharField(max_length=50)
#    descripcion = models.CharField(max_length=250)
#    permisos = models.CharField(max_length=200)
#    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

#    class Meta:
#        db_table = 'roles'

#    def __str__(self):
#        return self.nombre


#class Transacciones(models.Model):
#    id = models.AutoField(primary_key=True)
#    nombre_producto = models.CharField(max_length=250)
#    id_producto = models.IntegerField()
#    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
#    fecha = models.DateTimeField()
#    descripcion = models.CharField(max_length=200, blank=True, null=True)

#    class Meta:
#        db_table = 'transacciones'

#    def __str__(self):
#        return self.nombre_producto
