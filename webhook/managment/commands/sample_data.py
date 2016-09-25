# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from webhook.models import Denuncia
import os, sys, shutil
from django.core.management import call_command
import names

class Command(BaseCommand):
    help = 'Setup the initial content for the app'

    def handle(self, *args, **options):
        # Create 200 sample denuncias
        denuncias = []
        for i in list(range(200)):

            denuncias.append(Denuncia(
                fb_user_id='1168371943253552',
                closed=True,
                nombre_funcionario=names.get_first_name() + ' ' + names.get_last_name(),
                descripcion="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
                fecha_suceso='2016',
                lugar='cancun MX',
                current_step=6,


            ))
            Denuncia.objects.bulk_create(denuncias)

        self.stdout.write("Sample data")

