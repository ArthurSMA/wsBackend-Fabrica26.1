from django.contrib import admin
from .models import Piloto, EscolhaPiloto, ContaFinanceira

admin.site.register(Piloto)
admin.site.register(EscolhaPiloto)
admin.site.register(ContaFinanceira)