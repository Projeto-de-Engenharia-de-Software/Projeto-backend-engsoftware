import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard.models import RegistroViolencia 

class Command(BaseCommand):
    help = 'Importa dados de violência de um arquivo CSV com debugging aprimorado.'

    def handle(self, *args, **kwargs):
        caminho_arquivo = r'C:\\Users\\Wellington Viana\\eng-software\\Projeto-backend-engsoftware\nexus\\database\\VIOLBR14_filtrado.csv'
        self.stdout.write(self.style.NOTICE(f'Iniciando a importação do arquivo "{caminho_arquivo}"...'))

        line_num = 1 # Contador de linhas pra debugar o código
        registros_para_criar = []
        batch_size = 1000

        try:
            # Limpa a tabela dentro de uma transação para segurança
            with transaction.atomic():
                RegistroViolencia.objects.all().delete()
                self.stdout.write(self.style.WARNING('Tabela de registros de violência limpa.'))

            with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    line_num += 1
                    if line_num % 100 == 0:
                        self.stdout.write(f'Processando linha {line_num}...')

                    try:
                        ano_str = row.get('NU_ANO')
                        ano_int = int(float(ano_str))


                        ocorrencias_int = row

                        id_municip = row.get('ID_MUNICIP', '')
                        uf_str = id_municip[:2] if id_municip else ''
                        if not uf_str:
                             self.stdout.write(self.style.WARNING(f'Linha {line_num}: Não foi possível extrair UF de ID_MUNICIP "{id_municip}". Pulando linha.'))
                             continue

                        tipo_crime_str = row.get('AG_ESPEC')
                        if not tipo_crime_str or not tipo_crime_str.strip():
                            tipo_crime_str = 'Não especificado'

                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f'Erro de VALOR na linha {line_num}: {row}. Detalhes: {e}'))
                        continue
                    except KeyError as e:
                        self.stdout.write(self.style.ERROR(f'Erro de CHAVE na linha {line_num}: {row}. Chave não encontrada: {e}'))
                        continue

                    # Cria a instância do objeto do modelo
                    registro = RegistroViolencia(
                        ano=ano_int,
                        uf=uf_str,
                        tipo_crime=tipo_crime_str,
                        ocorrencias=ocorrencias_int
                    )
                    registros_para_criar.append(registro)

                    # Quando o lote estiver cheio, insere no banco de dados
                    if len(registros_para_criar) >= batch_size:
                        RegistroViolencia.objects.bulk_create(registros_para_criar)
                        self.stdout.write(self.style.SUCCESS(f'{len(registros_para_criar)} registros inseridos. Total processado: {line_num}'))
                        registros_para_criar = [] 

                # Insere os registros restantes que não completaram um lote
                if registros_para_criar:
                    RegistroViolencia.objects.bulk_create(registros_para_criar)
                    self.stdout.write(self.style.SUCCESS(f'Lote final de {len(registros_para_criar)} registros inserido.'))

            self.stdout.write(self.style.SUCCESS(f'Importação concluída! Total de linhas no arquivo: {line_num - 1}.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo "{caminho_arquivo}" não encontrado. Verifique o caminho.'))
        except Exception as e:
            # Este bloco pegará qualquer outro erro e nos dirá a linha
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado na linha {line_num} ou durante o salvamento. Detalhes: {e}'))

