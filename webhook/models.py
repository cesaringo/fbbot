from django.db import models
from django.utils import timezone


class Denuncia(models.Model):
    fb_user_id = models.CharField(max_length=200)
    nombre_funcionario = models.CharField(max_length=200) # o institución
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    fecha_suceso= models.CharField(max_length=200, null=True, blank=True)
    lugar = models.CharField(max_length=200, null=True, blank=True)
    current_step = models.IntegerField()
    closed = models.BooleanField(default=False)


class File(models.Model):
    url = models.CharField(max_length=200)
    denuncia = models.ForeignKey(Denuncia, related_name='files')



