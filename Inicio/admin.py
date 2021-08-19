from django.contrib import admin


from .models import Preguntas

class PreguntasAdmin(admin.ModelAdmin):
	list_display = ['id','pregunta','respuestaCorr','categoria','nivel' ]

admin.site.register(Preguntas,PreguntasAdmin)

