from django.contrib import admin
from .models import Aposta, ContaFinanceira # O nome aqui deve ser igual ao do models.py

admin.site.register(Aposta)
admin.site.register(ContaFinanceira)