from .models import Denuncia, File
from django.contrib import admin


class DenunciaAdmin(admin.ModelAdmin):
    list_display = ("fb_user_id", "nombre_funcionario", "fecha", "lugar")


class FileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Denuncia, DenunciaAdmin)
admin.site.register(File, FileAdmin)
