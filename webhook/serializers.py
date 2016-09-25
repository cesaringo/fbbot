from rest_framework.response import Response
from .models import *
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id","url"]


class DenunciaSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True,read_only=True)
    class Meta:
        model = Denuncia
        fields = ["id","fb_user_id", "nombre_funcionario", "descripcion","fecha","fecha_suceso","lugar","files"]
