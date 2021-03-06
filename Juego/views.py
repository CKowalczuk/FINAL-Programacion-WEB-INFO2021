from django.shortcuts 		import render, redirect, get_object_or_404
from django.contrib.auth 	import authenticate, login, logout,get_user_model
from .forms 				import RegistroFormulario, UsuarioLoginFormulario,RespuestaFormset
from .models 				import JuegoUsuario, Pregunta, Respuesta, PreguntasRespondidas
from django 					import forms
from django.views.generic.list 	import ListView
from django.views.generic.edit 	import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


def inicio(request):
	template_name = 'base.html'
	ctx = {
			}
	return render(request, template_name, ctx)

# crea un registro con el usuario y el puntaje obtenido
@login_required(login_url='login')
def jugar(request):
	template_name = 'Juego/jugar.html'
	
	# JuegoUser = JuegoUsuario.objects.create(usuario=request.user)
	# no funnciona, se cambió el create por el get_or_create

	JuegoUser, created = JuegoUsuario.objects.get_or_create(usuario=request.user)

	if request.method == 'POST':
		preg_pk = request.POST.get('preg_pk')
		pregunta_respondida = JuegoUser.intentos.select_related('pregunta').get(pregunta__pk=preg_pk)
		respuesta_pk = request.POST.get('respuesta_pk')
	
	
		try:
			opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
		except:
			return redirect('resultado', pregunta_respondida.pk)
	
		JuegoUser.validar_intento(pregunta_respondida, opcion_seleccionada)
		return redirect('resultado', pregunta_respondida.pk)
	else:

		pregunta = JuegoUser.renovar_preguntas()
		if pregunta is not None:
			JuegoUser.crear_intentos(pregunta)

		ctx = {
			'pregunta':pregunta
		}

	return render(request, template_name, ctx)

# toma el resultado y lo envía a resultados html para informar
# si es correcta o incorrecta

def resultado_pregunta(request, pregunta_respondida_pk):
	template_name = 'Juego/resultados.html'
	respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

	ctx = {
		'respondida':respondida
	}
	return render(request, template_name, ctx)

@staff_member_required
def administrar_preguntas(request):
	template_name = 'Juego/Administrar.html'
	model = Pregunta,Respuesta
	Preguntas = Pregunta.objects.all()
	Respuestas = Respuesta.objects.all()
	ctx = {
		'preguntas': Preguntas,
		'respuestas': Respuestas,

	}

	return render(request, template_name, ctx)	
	

# cuenta los usuarios registrados y los ordena por la cantidad de puntos
def ranking(request):
	template_name = 'Juego/ranking.html'
	total_usuarios_juego = JuegoUsuario.objects.order_by('-puntaje_total')[:10]
	contador = total_usuarios_juego.count()

	ctx = {

		'usuario_juego':total_usuarios_juego,
		'cant_usuarios':contador
	}

	return render(request, template_name, ctx)
@staff_member_required
def estadistica(request):
	model = User
	template_name = 'Usuario/estadistica.html'
	
	usuarios = User.objects.order_by('-date_joined')

	ctx = {
		'info' : usuarios 

	}
	
	
	return render(request, template_name, ctx)


# login para usuarios registrados

def loginView(request):
	template_name = 'Usuario/login.html'
	titulo = 'login'
	form = UsuarioLoginFormulario(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		usuario = authenticate(username=username, password=password)
		login(request, usuario)
		return redirect('HomeUsuario')

	ctx = {
		'form':form,
		'titulo':titulo
	}

	return render(request, template_name, ctx)



def HomeUsuario(request):
	template_name = 'inicio.html'
	ctx = {

	}
	
	return render(request, template_name, ctx)


def registro(request):
	template_name = 'Usuario/registro.html'
	titulo = 'Crear una Cuenta'
	if request.method == 'POST':
		form = RegistroFormulario(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = RegistroFormulario()

	ctx = {

		'form':form,
		'titulo': titulo

	}

	return render(request, template_name, ctx)


def logout_vista(request):
	logout(request)
	return redirect('/')


@staff_member_required
class PreguntaListView(ListView):
    model = Pregunta

class PreguntaCreateView(CreateView):
	model = Pregunta
	fields = ["consigna","puntaje"]
	def get_context_data(self, **kwargs):
		
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data["respuesta"] = RespuestaFormset(self.request.POST)
		else:
			data["respuesta"] = RespuestaFormset()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		respuesta = context['respuesta']
		self.object = form.save()
		if respuesta.is_valid():
			respuesta.instance = self.object
			respuesta.save()

		return self.render_to_response(self.get_context_data(form=form))


	def get_success_url(self):
		return redirect('inicio')