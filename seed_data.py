from django.core.management.base import BaseCommand
from core.models import Configuracao, Provincia, Categoria


class Command(BaseCommand):
    help = 'Insere dados iniciais: províncias, categorias e configurações.'

    def handle(self, *args, **options):
        self.stdout.write('═' * 50)
        self.stdout.write('  Seed Data — Crowdfunding Angola')
        self.stdout.write('═' * 50)

        # Províncias
        n = Provincia.criar_todas()
        self.stdout.write(self.style.SUCCESS(f'  Províncias criadas: {n}'))

        # Categorias
        n = Categoria.criar_todas()
        self.stdout.write(self.style.SUCCESS(f'  Categorias criadas: {n}'))

        # Configurações
        n = Configuracao.criar_defaults()
        self.stdout.write(self.style.SUCCESS(f'  Configurações criadas: {n}'))

        self.stdout.write('═' * 50)
        self.stdout.write(self.style.SUCCESS('  Seed concluído com sucesso!'))
        self.stdout.write('═' * 50)
