"""
Comando de seed de dados demo para o Finnancer.
Cria utilizadores, campanhas, doações e transacções realistas para Angola.

Uso: python manage.py seed_demo
"""

import random
import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from core.models import (
    Campanha, Categoria, Doacao, Provincia, Transacao, Usuario,
)

# ────────────────────────────────────────────────────────────────
# Dados base
# ────────────────────────────────────────────────────────────────

NOMES_INDIVIDUAIS = [
    'Ana Luísa Rodrigues', 'Carlos Manuel Teixeira', 'Beatriz Fonseca da Silva',
    'David Neto Ferreira', 'Elisa Marcelina Cunha', 'Filipe Santos Carvalho',
    'Graça Tomás Pereira', 'Hélder António Martins', 'Isabel Ferreira dos Santos',
    'João Paulo Lopes', 'Kátia Mendes Alves', 'Luís Eduardo Gonçalves',
    'Maria Clara Sousa', 'Nelson Afonso Pires', 'Olívia Costa Ribeiro',
    'Pedro Jorge Tavares', 'Rosa Amélia Batista', 'Samuel Ndombe Kiala',
    'Teresa Vieira Monteiro', 'Victor Augusto Nzamba',
]

NOMES_ORGS = [
    ('Fundação Esperança Angola', 'ong', 'apoio_social'),
    ('Associação Sementes do Futuro', 'associacao', 'educacao'),
    ('ONG Água Limpa Luanda', 'ong', 'agua_saneamento'),
    ('Associação Jovens Empreendedores AO', 'associacao', 'empreend_social'),
    ('Fundação Saúde para Todos', 'ong', 'saude'),
    ('Associação Cultural Ngola', 'associacao', 'cultura'),
    ('ONG Verde Angola', 'ong', 'ambiente'),
    ('Associação Desporto e Vida', 'associacao', 'desporto'),
]

CAMPANHAS_DATA = [
    # (titulo, categoria_nome, meta, dias, descricao_curta, status)
    ('Construção de Sala de Aula em Malanje', 'Educação', 2500000, 90,
     'Precisamos construir uma nova sala de aula para 45 crianças do ensino primário no município do Cacuso, Malanje.', 'ativa'),
    ('Poço de Água Potável no Huambo', 'Água e Saneamento', 1800000, 60,
     'Construção de um poço artesiano para abastecer 3 aldeias com acesso a água potável limpa no Huambo.', 'ativa'),
    ('Kit Escolar para 200 Crianças do Uíge', 'Educação', 960000, 45,
     'Distribuição de material escolar completo a 200 crianças carenciadas no início do ano lectivo no Uíge.', 'ativa'),
    ('Reabilitação do Centro de Saúde do Bié', 'Saúde', 4200000, 120,
     'Reabilitação urgente do centro de saúde comunitário de Kuito, que serve mais de 8.000 pessoas.', 'ativa'),
    ('Horta Comunitária no Lubango', 'Alimentação', 750000, 30,
     'Criação de uma horta comunitária para garantir alimentação saudável a 60 famílias vulneráveis no Lubango.', 'ativa'),
    ('Programa de Alfabetização de Adultos — Cabinda', 'Educação', 1200000, 75,
     'Curso de alfabetização gratuito para 80 adultos em situação de vulnerabilidade em Cabinda.', 'ativa'),
    ('Ambulância para Comunidade Rural do Cunene', 'Saúde', 6500000, 180,
     'Aquisição de uma ambulância para o posto de saúde do Ombadja, que serve aldeias a mais de 60 km do hospital.', 'ativa'),
    ('Reflorestação das Margens do Kwanza', 'Meio Ambiente', 890000, 60,
     'Plantação de 5.000 árvores nativas nas margens do Rio Kwanza para combater a erosão e preservar o ecossistema.', 'ativa'),
    ('Apoio a Crianças Órfãs de Benguela', 'Apoio Social', 3100000, 90,
     'Programa de apoio psicossocial, alimentação e material escolar para 35 crianças órfãs em Benguela.', 'ativa'),
    ('Laboratório Digital para Escola do Moxico', 'Educação', 5200000, 150,
     'Instalação de 20 computadores e internet para criar o primeiro laboratório digital numa escola do Moxico.', 'ativa'),
    ('Campanha de Vacinação Comunitária — Malanje', 'Saúde', 1450000, 45,
     'Financiamento de vacinas e equipamentos para campanha de vacinação infantil em 5 aldeias de Malanje.', 'ativa'),
    ('Casa de Acolhimento para Mulheres — Luanda', 'Apoio Social', 8900000, 200,
     'Construção de uma casa de acolhimento para mulheres vítimas de violência doméstica em Luanda.', 'ativa'),
    ('Torneio de Futebol Juvenil — Huíla', 'Desporto e Juventude', 420000, 25,
     'Organização do 1º Torneio de Futebol Juvenil da Huíla para promover o desporto e reduzir a violência juvenil.', 'ativa'),
    ('Biblioteca Itinerante para o Interior', 'Educação', 1650000, 80,
     'Criação de uma biblioteca móvel que percorra 12 municípios do interior levando livros e leitura às comunidades.', 'ativa'),
    ('Energia Solar para Posto de Saúde — Cuando Cubango', 'Saúde', 3800000, 100,
     'Instalação de painéis solares no posto de saúde de Menongue para garantir electricidade 24 horas.', 'ativa'),
    ('Reabilitação de Habitações Danificadas — Namibe', 'Habitação', 2700000, 70,
     'Reabilitação de 15 habitações danificadas pelas cheias no Namibe, afectando 85 pessoas.', 'ativa'),
    ('Centro de Formação Profissional — Lunda Norte', 'Empreendedorismo Social', 7200000, 180,
     'Construção de centro de formação em carpintaria, costura e informática para jovens desempregados da Lunda Norte.', 'ativa'),
    ('Preservação do Museu de Mbanza Kongo', 'Cultura', 1900000, 90,
     'Restauro e digitalização do acervo histórico do Museu do Zaire, preservando 500 anos de história angolana.', 'ativa'),
    ('Canalização de Água — Aldeia do Uíge', 'Água e Saneamento', 2200000, 60,
     'Extensão da rede de canalização de água potável para 3 bairros periféricos do município do Uíge.', 'encerrada'),
    ('Apoio Emergencial às Vítimas das Cheias — Cuanza Sul', 'Emergência', 950000, 15,
     'Resposta de emergência às famílias afectadas pelas cheias no Cuanza Sul — alimentos, tendas e medicamentos.', 'encerrada'),
    ('Bicicletas para Estudantes Rurais — Bié', 'Educação', 680000, 40,
     'Doação de 30 bicicletas para estudantes que percorrem mais de 10 km diários para chegar à escola no Bié.', 'encerrada'),
    ('Reforço Escolar para Crianças em Risco — Benguela', 'Educação', 540000, 50,
     'Programa de aulas de reforço gratuito para 60 crianças em risco de abandono escolar em Benguela.', 'aguardando_revisao'),
    ('Mercado Comunitário Coberto — Malanje', 'Desenvolvimento Comunitário', 3400000, 120,
     'Construção de um mercado coberto para proteger 80 vendedores informais das chuvas em Malanje.', 'aguardando_revisao'),
    ('Equipamento Desportivo para Escola — Huambo', 'Desporto e Juventude', 390000, 30,
     'Compra de material desportivo (bolas, redes, coletes) para 4 escolas secundárias do Huambo.', 'aguardando_revisao'),
    ('Apoio a Idosos Sem Abrigo — Luanda', 'Apoio Social', 1850000, 60,
     'Programa de refeições diárias e cuidados básicos de saúde para 50 idosos sem abrigo em Luanda.', 'rascunho'),
    ('Festival de Música Tradicional — Cabinda', 'Cultura', 720000, 35,
     'Organização do Festival de Música e Dança Tradicional de Cabinda para preservar o património cultural local.', 'rascunho'),
]

MENSAGENS_DOACOES = [
    'Boa sorte nesta causa nobre!',
    'Que Deus abençoe este projecto.',
    'A nossa comunidade precisa disto.',
    'Pequena contribuição, grande impacto.',
    'Juntos conseguimos mudar Angola.',
    'Estou muito orgulhoso desta iniciativa.',
    'Continuem o excelente trabalho!',
    'Doação feita com muito carinho.',
    '',
    '',
    '',  # algumas sem mensagem
]


class Command(BaseCommand):
    help = 'Insere dados demo realistas (utilizadores, campanhas, doações)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Apaga dados existentes antes de inserir (excepto admins e config)',
        )

    def handle(self, *args, **options):
        if options['limpar']:
            self._limpar()

        self.stdout.write(self.style.WARNING('A inserir dados demo...'))

        provincias = list(Provincia.objects.all())
        categorias = {c.nome: c for c in Categoria.objects.all()}

        if not provincias:
            self.stderr.write('Sem províncias. Corre seed_data primeiro.')
            return
        if not categorias:
            self.stderr.write('Sem categorias. Corre seed_data primeiro.')
            return

        senha_hash = make_password('Demo1234!')

        # ── 1. Utilizadores individuais ──────────────────────────────
        self.stdout.write('  → Utilizadores individuais...')
        individuais = []
        for i, nome in enumerate(NOMES_INDIVIDUAIS):
            email = self._email(nome, i)
            u, criado = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    'nome': nome,
                    'tipo_conta': 'individual',
                    'password': senha_hash,
                    'is_active': True,
                    'telefone': self._telefone(900000000 + i * 7 + 1),
                    'provincia': random.choice(provincias),
                    'bio': f'Cidadão angolano comprometido com o desenvolvimento do país.',
                },
            )
            if criado:
                individuais.append(u)
            else:
                individuais.append(u)
        self.stdout.write(f'     {len(individuais)} utilizadores individuais')

        # ── 2. Utilizadores Business ─────────────────────────────────
        self.stdout.write('  → Utilizadores Business...')
        business_users = []
        estados_biz = ['aprovado', 'aprovado', 'aprovado', 'em_analise', 'pendente', 'aprovado', 'aprovado', 'em_analise']
        for i, (nome_org, tipo_org, setor) in enumerate(NOMES_ORGS):
            email = f'admin@{slugify(nome_org)[:20].replace("-", "")}.ao'
            nome_rep = NOMES_INDIVIDUAIS[i % len(NOMES_INDIVIDUAIS)]
            estado = estados_biz[i]
            u, criado = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    'nome': nome_rep,
                    'tipo_conta': 'business',
                    'password': senha_hash,
                    'is_active': True,
                    'telefone': self._telefone(912000000 + i * 13 + 1),
                    'provincia': random.choice(provincias),
                    'nome_organizacao': nome_org,
                    'nome_representante': nome_rep,
                    'tipo_organizacao': tipo_org,
                    'setor_atividade': setor,
                    'estado_conta': estado,
                    'descricao_organizacao': f'{nome_org} é uma organização dedicada ao desenvolvimento comunitário em Angola, actuando há mais de 5 anos nas áreas de impacto social.',
                    'data_verificacao': timezone.now() - timedelta(days=random.randint(30, 365)) if estado == 'aprovado' else None,
                    'slug': slugify(nome_org)[:100],
                },
            )
            business_users.append(u)
        self.stdout.write(f'     {len(business_users)} utilizadores business')

        todos_utilizadores = individuais + business_users

        # ── 3. Campanhas ─────────────────────────────────────────────
        self.stdout.write('  → Campanhas...')
        campanhas_criadas = []
        agora = timezone.now()

        for i, (titulo, cat_nome, meta, dias, descricao, status) in enumerate(CAMPANHAS_DATA):
            criador = todos_utilizadores[i % len(todos_utilizadores)]
            cat = categorias.get(cat_nome)
            provincia = random.choice(provincias)

            slug_base = slugify(titulo)[:200]
            slug = slug_base
            contador = 1
            while Campanha.objects.filter(slug=slug).exists():
                slug = f'{slug_base}-{contador}'
                contador += 1

            data_pub = agora - timedelta(days=random.randint(5, 60))
            data_fim = data_pub + timedelta(days=dias) if status == 'ativa' else None
            data_enc = data_pub + timedelta(days=dias - random.randint(1, 5)) if status == 'encerrada' else None

            score = random.randint(55, 98)

            c, criado = Campanha.objects.get_or_create(
                slug=slug,
                defaults={
                    'titulo': titulo,
                    'criador': criador,
                    'categoria': cat,
                    'provincia': provincia,
                    'municipio': provincia.nome,
                    'descricao': f'<p>{descricao}</p><p>O financiamento será utilizado para cobrir os custos de materiais, mão de obra local e logística. Todo o processo será documentado e partilhado com os doadores através de actualizações regulares.</p><p>Contamos com o apoio de parceiros locais e da comunidade para garantir o sucesso deste projecto.</p>',
                    'resumo': descricao[:160],
                    'meta_financeira': Decimal(meta),
                    'duracao_dias': dias,
                    'beneficiarios_estimados': random.randint(50, 500),
                    'status': status,
                    'score_impacto': score,
                    'data_publicacao': data_pub if status != 'rascunho' else None,
                    'data_fim': data_fim,
                    'data_encerramento': data_enc,
                    'ao_atingir_meta': random.choice(['continuar', 'encerrar']),
                    'destaque': i < 4,  # primeiras 4 em destaque
                    'multicaixa_express_numero': self._telefone(923000000 + i * 17),
                },
            )
            campanhas_criadas.append(c)

        self.stdout.write(f'     {len(campanhas_criadas)} campanhas')

        # ── 4. Doações e Transacções ─────────────────────────────────
        self.stdout.write('  → Doações e transacções...')
        total_doacoes = 0
        campanhas_ativas = [c for c in campanhas_criadas if c.status in ('ativa', 'encerrada')]

        for campanha in campanhas_ativas:
            n_doacoes = random.randint(8, 30)
            soma = Decimal('0')
            n_confirmadas = 0

            for _ in range(n_doacoes):
                doador = random.choice(todos_utilizadores)
                valor = Decimal(random.choice([500, 1000, 1500, 2000, 2500, 5000, 7500, 10000, 15000, 25000]))
                anonima = random.random() < 0.2
                metodo = random.choice(['multicaixa_express', 'paypay_app'])
                estado_doacoes = random.choices(
                    ['confirmada', 'pendente', 'cancelada'],
                    weights=[75, 15, 10],
                )[0]

                dias_atras = random.randint(1, 55)
                data_criacao = timezone.now() - timedelta(days=dias_atras, hours=random.randint(0, 23))

                d = Doacao.objects.create(
                    campanha=campanha,
                    doador=doador,
                    valor=valor,
                    anonima=anonima,
                    mensagem=random.choice(MENSAGENS_DOACOES),
                    estado=estado_doacoes,
                    data_confirmacao=data_criacao + timedelta(minutes=random.randint(2, 25)) if estado_doacoes == 'confirmada' else None,
                )
                # Forçar data_criacao (auto_now_add não é editável directamente)
                Doacao.objects.filter(pk=d.pk).update(data_criacao=data_criacao)

                ref = uuid.uuid4().hex[:12].upper()
                status_tx = 'confirmada' if estado_doacoes == 'confirmada' else (
                    'pendente' if estado_doacoes == 'pendente' else 'falhou'
                )
                Transacao.objects.create(
                    doacao=d,
                    metodo_pagamento=metodo,
                    referencia=ref,
                    status=status_tx,
                    data_expiracao=data_criacao + timedelta(minutes=30),
                    data_confirmacao=data_criacao + timedelta(minutes=random.randint(2, 25)) if status_tx == 'confirmada' else None,
                    dados_gateway={
                        'tipo': metodo,
                        'referencia': ref,
                        'entidade': '11333' if metodo == 'multicaixa_express' else None,
                        'valor': float(valor),
                    },
                )

                if estado_doacoes == 'confirmada':
                    soma += valor
                    n_confirmadas += 1

                total_doacoes += 1

            # Actualizar totais da campanha
            Campanha.objects.filter(pk=campanha.pk).update(
                valor_arrecadado=soma,
                total_doadores=n_confirmadas,
            )

        self.stdout.write(f'     {total_doacoes} doações / transacções')

        # ── Resumo ───────────────────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS('Dados demo inseridos com sucesso!'))
        self.stdout.write(f'  Utilizadores individuais : {Usuario.objects.filter(tipo_conta="individual", is_staff=False).count()}')
        self.stdout.write(f'  Utilizadores business    : {Usuario.objects.filter(tipo_conta="business").count()}')
        self.stdout.write(f'  Campanhas                : {Campanha.objects.count()}')
        self.stdout.write(f'  Doações                  : {Doacao.objects.count()}')
        self.stdout.write(f'  Transacções              : {Transacao.objects.count()}')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write('  Password de todos os utilizadores demo: Demo1234!')
        self.stdout.write(self.style.SUCCESS('═' * 50))

    # ── Helpers ──────────────────────────────────────────────────────

    def _email(self, nome, idx):
        partes = nome.lower().split()
        base = f'{partes[0]}.{partes[-1]}'
        base = ''.join(c for c in base if c.isalnum() or c == '.')
        return f'{base}{idx}@demo.ao'

    def _telefone(self, numero):
        return str(numero)[:9]

    def _limpar(self):
        from core.models import (
            CampanhaActualizacao, Denuncia, ListaNegra,
            LogActividade, LogRevisaoCampanha, LogVerificacao,
            Notificacao, VerificacaoBusiness, DocumentoVerificacao,
        )
        self.stdout.write(self.style.WARNING('A limpar dados existentes...'))
        Transacao.objects.all().delete()
        Doacao.objects.all().delete()
        Denuncia.objects.all().delete()
        Notificacao.objects.all().delete()
        CampanhaActualizacao.objects.all().delete()
        LogRevisaoCampanha.objects.all().delete()
        Campanha.objects.all().delete()
        DocumentoVerificacao.objects.all().delete()
        LogVerificacao.objects.all().delete()
        VerificacaoBusiness.objects.all().delete()
        ListaNegra.objects.all().delete()
        LogActividade.objects.all().delete()
        Usuario.objects.filter(is_staff=False, is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('  Limpeza concluída.'))
