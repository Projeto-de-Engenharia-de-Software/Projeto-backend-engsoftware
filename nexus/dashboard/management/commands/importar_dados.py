import csv
import os
import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from dashboard.models import RegistroViolencia
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa dados de violência de um arquivo CSV com debugging aprimorado.'

    ## Função que limpar e trata as colunas gerais (Tipo char)
    def sanitize(self, value, default="Não Informado"):
        if pd.isna(value) or value in ['', 'NaN', 'nan', None]:
            return default
        return value
    
    ## Função que limpar e trata as colunas do tipo Date (DT_OCOR etc.)
    def sanitize_date(self, value):
        if pd.isna(value) or value in ['', 'NaN', 'nan', None]:
            return None  # Para campo DateField, preferível usar None
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except Exception:
            return None
    
    ## Função que limpar e trata as colunas do tipo ID de municípios
    def sanitize_id(self, value):
        if value is None or str(value).strip() in ['', 'NaN', 'nan']:
            return "000000"
        try:
            return str(int(float(value))).zfill(6)
        except ValueError:
            return "000000"

    ## Função que limpar e trata as colunas do tipo Ano
    def sanitize_year(self, value):
        if value is None or str(value).strip() in ['', 'NaN', 'nan']:
            return "0000"
        try:
            return str(int(float(value))).zfill(4)
        except ValueError:
            return "0000"

    ## Função que limpar e trata as colunas do tipo ENUM
    def sanitize_response(self, value):
        if value is None or str(value).strip() in ['', 'NaN', 'nan']:
            return "Não Informado"
        try:
            value = str(int(float(value)))
            if value == '1':
                return "Sim"
            elif value == '2':
                return "Não"
            elif value == '8':
                return "Não se aplica"
            elif value == '9':
                return "Ignorado"
            else:
                return value  # caso algum outro número
        except ValueError:
            return "Não Informado"
    
    ## Função que limpar e trata a coluna de LOCAL_OCR que é um enum mais especicificado
    def sanitize_local_ocor(self, value):
        if value is None or str(value).strip() in ['', 'NaN', 'nan']:
            return "Não Informado"
        try:
            value = str(int(float(value)))
            if value == '1':
                return "Residência"
            elif value == '2':
                return "Habitação Coletiva"
            elif value == '3':
                return "Escola"
            elif value == '4':
                return "Local de prática esportiva"
            elif value == '5':
                return "Bar ou similar"
            elif value == '6':
                return "Via Pública"
            elif value == '7':
                return "Comércio/Serviços"
            elif value == '8':
                return "Industrias/Construção"
            elif value == '9':
                return "Outro"
            elif value == '99':
                return "Ignorado"
            else:
                return value
        except ValueError:
            return "Não Informado"

    ## Função principal que gera tudo e passa
    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(settings.BASE_DIR, 'database', 'VIOLBR14_filtrado.csv')
        self.stdout.write(self.style.NOTICE(f'Iniciando a importação do arquivo "{csv_file_path}"...'))

        line_num = 1
        registros_para_criar = []
        batch_size = 1000
        
        try:                

            with transaction.atomic():
                RegistroViolencia.objects.all().delete()
                self.stdout.write(self.style.WARNING('Tabela de registros de violência limpa.'))
            
            todos_municipios = requests.get(
            "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
            ).json()

            mapa_municipios = {
                str(m['id'])[:6]: m['nome']
            for m in todos_municipios if str(m['id']).startswith('26')
            }

            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    line_num += 1
                    if line_num % 1000 == 0:
                        self.stdout.write(f'Processando linha {line_num}...')
                    
                    id_municipio_str = self.sanitize(row.get('ID_MUNICIP'))

                    id_municipio_resi_str = self.sanitize(row.get('ID_MUNICIP'))
                    id_municipio_resi_str = self.sanitize_id(id_municipio_resi_str)

                    id_municipio_ocor_str = self.sanitize(row.get('ID_MUNICIP'))
                    id_municipio_ocor_str = self.sanitize_id(id_municipio_ocor_str)

                    if not id_municipio_str.startswith("26"):
                        continue  # pula registros de fora do estado

                    nome_municipio = mapa_municipios.get(id_municipio_str, "Desconhecido")
                    nome_municipio_ocor = mapa_municipios.get(id_municipio_ocor_str, "Desconhecido")
                    nome_municipio_resi = mapa_municipios.get(id_municipio_resi_str, "Desconhecido")


                    registro = RegistroViolencia(
                        NU_ANO=self.sanitize(row.get('NU_ANO')),
                        DT_NOTIFIC=self.sanitize_date(row.get('DT_NOTIFIC')),
                        MUNICIPIO=nome_municipio,
                        DT_OCOR=self.sanitize_date(row.get('DT_OCOR')),
                        DT_NASC=self.sanitize_year(row.get('DT_NASC')),
                        CS_SEXO=self.sanitize(row.get('CS_SEXO')),
                        CS_RACA=self.sanitize(row.get('CS_RACA')),
                        MUNIC_RESI=nome_municipio_resi,
                        MN_OCOR=nome_municipio_ocor,
                        LOCAL_OCOR=self.sanitize_local_ocor(row.get('LOCAL_OCOR')),
                        LOCAL_ESPEC=self.sanitize(row.get('LOCAL_ESPEC')),
                        OUT_VEZES=self.sanitize_response(row.get('OUT_VEZES')),
                        AG_FORCA=self.sanitize_response(row.get('AG_FORCA')),
                        AG_ENFOR=self.sanitize_response(row.get('AG_ENFOR')),
                        AG_OBJETO=self.sanitize_response(row.get('AG_OBJETO')),
                        AG_CORTE=self.sanitize_response(row.get('AG_CORTE')),
                        AG_QUENTE=self.sanitize_response(row.get('AG_QUENTE')),
                        AG_ENVEN=self.sanitize_response(row.get('AG_ENVEN')),
                        AG_FOGO=self.sanitize_response(row.get('AG_FOGO')),
                        AG_AMEACA=self.sanitize_response(row.get('AG_AMEACA')),
                        AG_OUTROS=self.sanitize_response(row.get('AG_OUTROS')),
                        AG_ESPEC=self.sanitize_response(row.get('AG_ESPEC')),
                        SEX_ASSEDI=self.sanitize_response(row.get('SEX_ASSEDI')),
                        SEX_ESTUPR=self.sanitize_response(row.get('SEX_ESTUPR')),
                        REL_PAI=self.sanitize_response(row.get('REL_PAI')),
                        REL_MAE=self.sanitize_response(row.get('REL_MAE')),
                        REL_PAD=self.sanitize_response(row.get('REL_PAD')),
                        REL_MA=self.sanitize_response(row.get('REL_MA')),
                        REL_CONJ=self.sanitize_response(row.get('REL_CONJ')),
                        REL_EXCON=self.sanitize_response(row.get('REL_EXCON')),
                        REL_NAMO=self.sanitize_response(row.get('REL_NAMO')),
                        REL_EXNAM=self.sanitize_response(row.get('REL_EXNAM')),
                        REL_FILHO=self.sanitize_response(row.get('REL_FILHO')),
                        REL_IRMAO=self.sanitize_response(row.get('REL_IRMAO')),
                        REL_CONHEC=self.sanitize_response(row.get('REL_CONHEC')),
                        REL_DESCO=self.sanitize_response(row.get('REL_DESCO')),
                        REL_CUIDA=self.sanitize_response(row.get('REL_CUIDA')),
                        REL_PATRAO=self.sanitize_response(row.get('REL_PATRAO')),
                        REL_INST=self.sanitize_response(row.get('REL_INST')),
                        REL_POL=self.sanitize_response(row.get('REL_POL')),
                        REL_PROPRI=self.sanitize_response(row.get('REL_PROPRI')),
                        REL_OUTROS=self.sanitize_response(row.get('REL_OUTROS')),
                        REL_ESPEC=self.sanitize_response(row.get('REL_ESPEC')),
                        AUTOR_SEXO=self.sanitize_response(row.get('AUTOR_SEXO')),
                        ENC_SAUDE=self.sanitize_response(row.get('ENC_SAUDE')),
                        ASSIST_SOC=self.sanitize_response(row.get('ASSIST_SOC')),
                        REDE_EDUCA=self.sanitize_response(row.get('REDE_EDUCA')),
                        ATEND_MULH=self.sanitize_response(row.get('ATEND_MULH')),
                        CONS_TUTEL=self.sanitize_response(row.get('CONS_TUTEL')),
                        CONS_IDO=self.sanitize_response(row.get('CONS_IDO')),
                        DELEG_IDOS=self.sanitize_response(row.get('DELEG_IDOS')),
                        DIR_HUMAN=self.sanitize_response(row.get('DIR_HUMAN')),
                        MPU=self.sanitize_response(row.get('MPU'))
                    )

                    registros_para_criar.append(registro)

                    if len(registros_para_criar) >= batch_size:
                        RegistroViolencia.objects.bulk_create(registros_para_criar)
                        self.stdout.write(self.style.SUCCESS(f'{len(registros_para_criar)} registros inseridos. Total processado: {line_num}'))
                        registros_para_criar = []

                if registros_para_criar:
                    RegistroViolencia.objects.bulk_create(registros_para_criar)
                    self.stdout.write(self.style.SUCCESS(f'Lote final de {len(registros_para_criar)} registros inserido.'))

            self.stdout.write(self.style.SUCCESS(f'Importação concluída! Total de linhas no arquivo: {line_num - 1}.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo "{csv_file_path}" não encontrado. Verifique o caminho.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado na linha {line_num} ou durante o salvamento. Detalhes: {e}'))
