
from urllib import request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
#from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

#from django.template import RequestContext
from .models import Empresa, Inventario, Usuario, Transaccion, Alertas
#from .forms import  formLog
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from random  import randrange

from django.shortcuts import render
from .models import Inventario

from django.contrib.auth.hashers import make_password ,check_password
from .forms import InventarioForm
from django.shortcuts import render, redirect
from .models import Usuario



# middleware.py
#from django.urls import reverse

#def mi_vista_protegida(request):
#    if not request.user.is_authenticated:
#        return redirect('login')  # Redirige a la página de inicio de sesión
#    return render(request, 'dashboard')
    





    


#def login_view(request):
#    if request.method == 'POST':
#        username = request.POST['username']
#        password = request.POST['password']
#        print(f'Username: {username}, Password: {password}') 
#        try:
#            usuario = Usuario.objects.get(username=username)
#            if usuario.check_password(password):  # Verifica la contraseña
#                # Aquí puedes establecer la sesión del usuario
#                request.session['id'] = usuario.id  # Guarda el ID del usuario en la sesión
#                return redirect('dashboard')  # Cambia esto a tu URL deseada
#            else:
#                error = "Contraseña incorrecta"
#        except Usuario.DoesNotExist:
#            error = "Usuario no encontrado"

#        return render(request, 'login.html', {'error': error})

#    return render(request, 'login.html')







from django.shortcuts import render, redirect
from .models import Usuario  # Asegúrate de importar tu modelo de usuario

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(username=username)
            if usuario.check_password(password):  # Verifica la contraseña
                # Aquí puedes establecer la sesión del usuario
                request.session['user_id'] = usuario.id
                request.session['username'] = usuario.username
                
                # Redirige a la URL especificada en 'next' o a un destino predeterminado
                next_url = request.POST.get('next')  # Obtiene el valor de 'next'
                if next_url:  # Verifica que next_url no sea None
                    return redirect(next_url)
                else:
                    return redirect('dashboard')  # Cambia 'dashboard' a tu URL predeterminada
            else:
                error = "Contraseña incorrecta"
        except Usuario.DoesNotExist:
            error = "Usuario no encontrado"

        return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')








# Para crear un usuario
#usuario = Usuario(username='username', password=make_password('password'))
#usuario.save()




#def loginn(request):
    #if request.method == 'POST':
        #username = request.POST.get('username')
        #password = request.POST.get('password')

       # try:
       #     usuario = Usuario.objects.get(username=username)
           # print("Usuario encontrado:", usuario.username)

          #  if check_password(password, usuario.password):
             #   request.session['username'] = usuario.username
             #   print("Contraseña válida, redirigiendo a indicador")
             #   if check_password(password, usuario.password):
            #       print("Contraseña correcta")
    # Redirección a indicador
           #     else:
          #         print("Hash en la base de datos:", usuario.password)
         #          print("Contraseña ingresada:", password)
         #          print("Contraseña incorrecta")

      #          return redirect('indicador')
       #     else:
      #          messages.error(request, 'Contraseña incorrecta.')
     #           print("Contraseña incorrecta")
     #   except Usuario.DoesNotExist:
     #        print("Usuario no encontrado")

    #return render(request, 'login.html')



#def loginn(request):
#    if request.method=='POST':
#        try:
#            detalleusuario = Usuario.object.get(username=request.POST['username'], password=request.POST['password'])
#            print("Usuario=", detalleusuario)
#            request.session['username']=detalleusuario.username
#            return render(request, 'index_master.html')
#        except Usuario.DoesNotExist as e:
#            messages.success(request, 'Nombre de usuario o contaseña invalido')
#    return render(request, 'index_junior.html')




#def login_view(request):
#    if request.method == 'POST':
#        formulario = formLog(request.POST)
#        if formulario.is_valid:
#            usuario = request.POST['username']
#            clave = request.POST['password']
#
#            verificacion = Usuario.objects.filter(usuario=usuario, password=clave).exists()
#            print(verificacion)

#            if verificacion == True:
#                return HttpResponseRedirect('/indicador')
#            else:
#                return HttpResponseRedirect('/login')
        
#    else:
#        formulario = formLog()
#    return render('crud_usuarios/indicador.html', {'formulario': formulario}, context_instance=RequestContext(request))


#def login_view(request):
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid(): 
#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            try:
#                usuario = Usuario.objects.get(username=username)
#                if check_password(password, usuario.password):
#                    request.session['username'] = usuario.username
#                    login(request, usuario)  # Utiliza Django's login para iniciar sesión
#                    return redirect('indicador')
#                else:
#                    form.add_error(None, 'Usuario o contraseña incorrectos.')
#            except Usuario.DoesNotExist:
#                form.add_error(None, 'Usuario o contraseña incorrectos.')
##    else:
#        form = LoginForm()
#    return render(request, 'login.html', {'form': form})

def index(request):
    return render(request, "index.html")

@login_required
def lista(request):
    user_id = request.session.get('user_id')
    if user_id:
        usuario = Usuario.objects.get(id=user_id)     
        empresa_id = usuario.empresa_id       
        inventario = Inventario.objects.filter(empresa_id=empresa_id).values(
            'id_producto', 'nombre_producto', 'cantidad_producto', 'tipo_unidad'
        )      
        return render(request, "crud_usuarios/lista.html", {'inventario': inventario})
    else:
        return redirect('login')







from .forms import InventarioForm


@login_required
def agregar(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        user_id = request.session.get('user_id')
        if form.is_valid():
            # Obtén el usuario autenticado
            try:
                usuario = Usuario.objects.get(id=user_id)  # Busca por username
            except Usuario.DoesNotExist:
                # Maneja el caso donde el usuario no tiene un perfil asociado
                return redirect('lista')  # Cambia esto por la vista que desees

            inventario = form.save(commit=False)
            inventario.empresa = usuario.empresa  # Asocia el producto a la empresa del usuario
            inventario.save()
            return redirect('lista')  # Cambia esto por el nombre de tu vista de lista
    else:
        form = InventarioForm()
    
    return render(request, 'crud_usuarios/agregar.html', {'form': form})




def actualizar(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        try:
            user = Usuario.objects.get(id=user_id)
            user.nombre = request.POST.get('nombre')
            user.apellido = request.POST.get('apellido')
            user.telefono = request.POST.get('telefono')
            user.save()
            return redirect('lista')
        except Usuario.DoesNotExist:
            return render(request, "crud_usuarios/actualizar.html", {'error': 'Usuario no encontrado'})
    else:
        users = Usuario.objects.all()
        return render(request, "crud_usuarios/actualizar.html", {'usuario': users})






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Inventario, Usuario

@login_required
def eliminar(request):
    user_id = request.session.get('user_id')
    
    # Obtén el usuario autenticado
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del usuario.')
        return redirect('lista')

    if request.method == 'POST':
        id_inventario = request.POST.get('id_inventario')  # Asegúrate de usar 'id_inventario'
        producto = get_object_or_404(Inventario, id_inventario=id_inventario)  # Buscar por id_inventario

        # Verifica que el usuario pertenezca a la misma empresa que el producto
        if usuario.empresa == producto.empresa:
            producto.delete()  # Elimina el producto
            messages.success(request, 'Producto eliminado correctamente.')
        else:
            messages.error(request, 'No tienes permiso para eliminar este producto.')
        
        return redirect('eliminar')  # Redirige a la misma página o a donde desees

    # Si es un GET, muestra la lista de productos de la empresa del usuario
    productos = Inventario.objects.filter(empresa=usuario.empresa)
    return render(request, 'crud_usuarios/eliminar.html', {'productos': productos})




# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import UsuarioForm
from django.contrib import messages

@login_required
def configuracion(request):
    # Suponiendo que el modelo Usuario tiene una relación con el User de Django
    try:
        usuario = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('crud_usuarios/configuracion.html')  # Redirigir a una página de error o inicio

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los cambios se han guardado correctamente.')
            return redirect('crud_usuarios/configuracion.html')  # Redirige a la misma página
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'crud_usuarios/configuracion.html', {'form': form})


    

@login_required
def indicador(request):
    user_id = request.session.get('user_id')
    if user_id:
        usuario = Usuario.objects.get(id=user_id)     
        empresa_id = usuario.empresa_id    
   
        inventario = Inventario.objects.filter(empresa_id=empresa_id).values(
            'id_producto', 'nombre_producto', 'cantidad_producto', 'tipo_unidad', 'empresa_id'
        )

        # Obtener los valores de cantidad_producto para el gráfico
        cantidades = [item['cantidad_producto'] for item in inventario]
        if cantidades:
            stock_minimo = min(cantidades)
            stock_maximo = max(cantidades)
        else:
            stock_minimo = 0
            stock_maximo = 0

        return render(request, "crud_usuarios/indicador.html", {
            'inventario': inventario,
            'stock_minimo': stock_minimo,
            'stock_maximo': stock_maximo,
        })
    else:
        return redirect('login')


@login_required
def alertas(request):
    user_id = request.session.get('user_id')
    if user_id:
       empresa_id = Usuario.empresa_id
       alertas_list = Alertas.objects.all().values('descripcion', 'calidad_alerta', 'fecha', 'empresa_id')
       return render(request, "crud_usuarios/alertas.html", {'alertass': alertas_list})
    else:
        return redirect('login')


@login_required
def notifica(request):
    return render(request, "crud_usuarios/notifica.html")


def registro(request):
    return render(request, "registro.html")




from collections import defaultdict

@login_required
def dashboard(request):
    user_id = request.session.get('user_id')
    if user_id:
        usuario = Usuario.objects.get(id=user_id)
        empresa_id = usuario.empresa_id
        
        # Filtrar los productos del inventario por la empresa del usuario
        productos = Inventario.objects.filter(empresa_id=empresa_id).values(
            'id_producto', 'nombre_producto', 'cantidad_producto', 'tipo_unidad'
        )
        
        # Preparar datos para el gráfico de barras
        cantidad_por_tipo = defaultdict(int)
        for producto in productos:
            cantidad_por_tipo[producto['tipo_unidad']] += producto['cantidad_producto']
        
        # Convertir a listas para el gráfico de barras
        tipos = list(cantidad_por_tipo.keys())
        cantidades = list(cantidad_por_tipo.values())
        
        # Preparar datos para el gráfico circular (por producto)
        nombres_productos = []
        cantidades_productos = []
        
        for producto in productos:
            nombres_productos.append(producto['nombre_producto'])
            cantidades_productos.append(producto['cantidad_producto'])
        
        # Calcular el producto con mayor y menor stock
        if productos:
            producto_mayor_stock = max(productos, key=lambda x: x['cantidad_producto'])
            producto_menor_stock = min(productos, key=lambda x: x['cantidad_producto'])
        else:
            producto_mayor_stock = None
            producto_menor_stock = None
        
        # Mensaje de bienvenida
        mensaje_bienvenida = f"¡Bienvenido, {usuario.username}!"

        return render(request, 'crud_usuarios/dashboard.html', {
            'usuario': usuario,
            'productos': productos,
            'tipos': tipos,
            'cantidades': cantidades,
            'nombres_productos': nombres_productos,
            'cantidades_productos': cantidades_productos,
            'mensaje_bienvenida': mensaje_bienvenida,
            'producto_mayor_stock': producto_mayor_stock,
            'producto_menor_stock': producto_menor_stock,
        })
    else:
        return redirect('login')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la vista de login

@login_required
def index_jr(request):
    return render(request, 'index_junior.html')



def grafico_circular(request):
    # Obtener la cantidad de transacciones por nombre de pro
    datos = Transaccion.objects.values('nombre_producto').annotate(total=Count('id')).order_by('nombre_producto')


    nombres_productos = [dato['nombre_producto'] for dato in datos]
    cantidades = [dato['total'] for dato in datos]

    context = {
        'nombres_productos': nombres_productos,
        'cantidades': cantidades,
    }
    return render(request, 'grafico_circular.html', context)



def get_chart(_request):

    serie = []
    counter = 0
    while(counter < 7):

        serie.append(randrange(100,400))
        counter += 1
    chart = {
        'xAxis': [
            {
                'type': "category",
                'data': ["Lun","Mar","Mie","Jue","Vie","Sab","Dom"],
            }
        ],
        'yaXis': [
            {
                'type': "value"
            }
            
        ],
        'series':[
            {
                'data': serie,
                'type': "line"
            }
        ]






    }
    return JsonResponse(chart)













#from django.shortcuts import render, redirect
##from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
## Create your views her.

#from django.http import HttpResponse
#from .models import Empresa, Inventario, Usuario
#from django.views import generic

#from django.contrib.auth import authenticate, login
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.hashers import make_password, check_password


#from .forms import LoginForm
#from .models import Usuario  # Asegúrate de que este modelo esté definido correctamente.

#def login_view(request):
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            try:
#                # Aquí se busca al usuario en la base de datos Oracle
#                usuario = Usuario.objects.get(username=username)
#                # Verifica la contraseña usando el hash almacenado
#                if check_password(password, usuario.password):
#                    # Almacena el nombre de usuario en la sesión
#                    request.session['username'] = usuario.username
#                    return redirect('indicador')  # Redirige a indicador.html
#                else:
#                    form.add_error(None, 'Usuario o contraseña incorrectos.')
#            except Usuario.DoesNotExist:
#                form.add_error(None, 'Usuario o contraseña incorrectos.')
#    else:
#        form = LoginForm()
#    return render(request, 'login.html', {'form': form})





#TEMPLATE_DIRS = (
#    'os.path.join(BASE_DIR, "templates")'
#)


#def index(request):
#    return render(request, "index.html")

#def lista(request):
#    users = Usuario.objects.all()
#    datos = {'usuario' : users}
#    return render(request, "crud_usuarios/lista.html", datos)

#def agregar(request):
#    # mi_aplicacion/views.py
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#        nombre = request.POST.get('nombre')
#        apellido = request.POST.get('apellido')
#        rut = request.POST.get('rut')
#        empresa = request.POST.get('empresa')  # Este debe ser el ID de la empresa
#        telefono = request.POST.get('telefono')
#        
#        # Obtén la instancia de Empresa
#        try:
#            empresa = Empresa.objects.get(id=empresa)
#        except Empresa.DoesNotExist:
#            # Manejar el caso donde la empresa no existe
#            return render(request, 'crud_usuarios/agregar.html', {'error': 'Empresa no encontrada'})
#
#        # Crea un nuevo usuario
#        nuevo_usuario = Usuario(
#            username=username,
#            password=make_password(password),  # Asegúrate de usar un hash
#            nombre=nombre,
#            apellido=apellido,
#            rut=rut,
#            empresa=empresa,
#            telefono=telefono  # Asigna la instancia de Empresa
#        )
#        nuevo_usuario.save()  # Guarda el usuario
#        return redirect('lista')  # Cambia esto a tu URL de redirección

#    return render(request, 'crud_usuarios/agregar.html')


















##    if request.method=='POST':
##        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('rut')  and request.POST.get('username')  and request.POST.get('password') and request.POST.get('empresa'):
# ##          user.nombre = request.POST.get('nombre')
#    #        user.apellido = request.POST.get('apellido')
#   #         user.rut = request.POST.get('rut')
#     #       user.username = request.POST.get('username')
#      #      user.password = request.POST.get('password')
#       #     user.empresa = request.POST.get('empresa')
#        #    user.save() 
#         #   return redirect('lista')
# #   else:
#      # return render(request, "crud_usuarios/agregar.html")

#def actualizar(request):
#    if request.method == 'POST':
#        if request.POST.get('id') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('correo') and request.POST.get('telefono') and request.POST.get('empresa'):
#            user = Usuario()
#            user.id = request.POST.get('id')
#            user.nombre = request.POST.get('nombre')
#            user.apellido = request.POST.get('apellido')
#            user.correo = request.POST.get('correo')
#            user.telefono = request.POST.get('telefono')
#            user.empresa = request.POST.get('empresa')
#            user.save() 
#            return redirect('lista')
        

#    else:
#         users = Usuario.objects.all()
#         datos = {'usuario' : users}
#         return render(request, "crud_usuarios/actualizar.html", datos)



#def eliminar(request):
#    if request.method == 'POST':
#        if request.POST.get('id'):
#             id_a_borrar = request.POST.get('id')
#             tupla = Usuario.objects.get(id = id_a_borrar)
#             tupla.delete()
#             return redirect('lista')
#    else:
#        users = Usuario.objects.all()
#        datos = {'usuarios' : users}
#    return render(request, "crud_usuarios/eliminar.html")


#aqui empezara vuista y funciones de panel de usuario






#def login(request):
 #   return render(request, "registration/login.html")


#def lista(request):
#    users = Usuario.objects.all()
#    datos = {'usuario' : users}
#    return render(request, "crud_usuarios/lista.html", datos)

#@login_required 
#def indicador(request):
#    Prod = Inventario.objects.all()
#    datos = {'inventario' : Prod}  
#    return render(request, "crud_usuarios/indicador.html", datos)

#def alertas(request):
 #   return render(request, "crud_usuarios/alertas.html")

#def notifica(request):
 #   return render(request, "crud_usuarios/notifica.html")

#def login_view_admin(request):
#    return render(request, "registration/login_admin.html")

#def signin(request):
  #  if request.method == 'GET':
  #      return render(request, 'signin.html',{
  #          'form': AuthenticationForm
  #      })
  #  else:
  #      user = authenticate(
  #          request, username=request.POST['user'], password=request.POST
  #          ['password'])
  #      if user is None:
  #          return render(request, 'signin.html', {
  #              'form':  AuthenticationForm,
  #              'error': "Nombre e usuario o contraseña incorrecto"
  #          })
  #      else:
  #          login(request, user)
  #          return redirect('registration/indicador.html')


