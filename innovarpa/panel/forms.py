from django import forms
from .models import Usuario

from django import forms
from .models import Inventario
#class LoginForm(forms.Form):
#    username = forms.CharField(max_length=50)
#    password = forms.CharField(widget=forms.PasswordInput)



class formLog(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username','password']




from django import forms
from .models import Inventario

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_producto','nombre_producto', 'cantidad_producto', 'tipo_unidad']  # Omite 'id_inventario' y 'empresa'



class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono']