# data_analytics/management/commands/import_regional_data.py
import csv
from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Regiao, DadosMensaisRegiao 

class Command(BaseCommand):
    help = 'Importa dados regionais de um arquivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV com os dados regionais.')
        parser.add_argument('--ano', type=int, required=True, help='O ano ao qual os dados do CSV se referem (ex: 2024).')
        # O delimitador padrão do CSV é vírgula, mas podemos permitir que seja configurável
        parser.add_argument('--delimitador', type=str, default=',', help='O delimitador do CSV (padrão: vírgula).')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        ano_dado = options['ano']
        delimitador = options['delimitador']

        # Mapeamento dos nomes dos meses para seus números (do CSV para o modelo)
        meses_map = {
            'Janeiro': 1, 'Fevereiro': 2, 'Marco': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6,
            'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
        }
        # Ordem dos cabeçalhos das colunas de mês no CSV
        meses_colunas_csv = [
            'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]

        self.stdout.write(self.style.WARNING(f"Iniciando importação para o ano: {ano_dado}"))
        self.stdout.write(self.style.WARNING(f"Usando delimitador: '{delimitador}'"))

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimitador) # csv.DictReader usa os cabeçalhos

                # Verifica se os cabeçalhos esperados estão no CSV
                if not all(col in reader.fieldnames for col in ['Regiao', 'Total'] + meses_colunas_csv):
                    raise CommandError("O arquivo CSV não possui todos os cabeçalhos esperados: 'Regiao', 'Janeiro'...'Dezembro', 'Total'.")

                for i, row in enumerate(reader):
                    # Pega os dados da linha
                    regiao_nome = row['Regiao'].strip()
                    total_somado_str = row['Total'].strip()

                    # Processa a coluna 'Total'
                    try:
                        total_somado = float(total_somado_str)
                    except ValueError:
                        self.stderr.write(self.style.ERROR(f"Linha {i+1}: 'Total' '{total_somado_str}' não é um número. Pulando total para esta linha."))
                        total_somado = None # Define como None se houver erro

                    # Tenta obter ou criar a Regiao
                    regiao_obj, created_regiao = Regiao.objects.get_or_create(
                        nome=regiao_nome,
                        defaults={'total_anual_csv': total_somado}
                    )
                    if created_regiao:
                        self.stdout.write(self.style.SUCCESS(f'Criada nova região: {regiao_obj.nome}'))
                    elif regiao_obj.total_anual_csv != total_somado:
                        # Se a região já existe e o total é diferente, atualiza
                        regiao_obj.total_anual_csv = total_somado
                        regiao_obj.save()
                        self.stdout.write(self.style.WARNING(f'Total anual de "{regiao_obj.nome}" atualizado para: {total_somado}'))
                    else:
                        self.stdout.write(self.style.NOTICE(f'Região "{regiao_obj.nome}" já existe e total não alterado.'))

                    # Processa os valores mensais
                    for mes_nome_csv in meses_colunas_csv:
                        mes_num = meses_map[mes_nome_csv]
                        valor_str = row[mes_nome_csv].strip()

                        try:
                            valor = float(valor_str)

                            # Cria ou atualiza o DadoMensal para aquele mês
                            dado_mensal, created_dado = DadosMensaisRegiao.objects.get_or_create(
                                regiao=regiao_obj,
                                ano=ano_dado,
                                mes=mes_num,
                                defaults={'valor': valor}
                            )
                            if not created_dado: # Se o dado já existia, atualiza o valor
                                if dado_mensal.valor != valor: # Só atualiza se o valor mudou
                                    dado_mensal.valor = valor
                                    dado_mensal.save()
                                    self.stdout.write(self.style.WARNING(f'Atualizado dado de {regiao_obj.nome} - {mes_nome_csv}/{ano_dado}: {valor}'))
                                # else: self.stdout.write(self.style.NOTICE(f'Dado mensal de {regiao_obj.nome} - {mes_nome_csv}/{ano_dado} já existe e não alterado.'))
                            else:
                                self.stdout.write(self.style.SUCCESS(f'Adicionado dado de {regiao_obj.nome} - {mes_nome_csv}/{ano_dado}: {valor}'))

                        except ValueError:
                            self.stderr.write(self.style.ERROR(f"Linha {i+1}: Valor '{valor_str}' para '{mes_nome_csv}' não é um número. Pulando este mês."))
                            continue
                        except IndexError: # Caso a linha esteja incompleta para os meses
                            self.stderr.write(self.style.ERROR(f"Linha {i+1}: Faltam colunas para meses. Pulando meses restantes."))
                            break # Sai do loop de meses para esta linha

            self.stdout.write(self.style.SUCCESS('Importação de dados regionais concluída com sucesso!'))

        except FileNotFoundError:
            raise CommandError(f'O arquivo CSV "{csv_file_path}" não foi encontrado.')
        except KeyError as e:
            raise CommandError(f'Cabeçalho CSV ausente: {e}. Verifique se as colunas "Regiao", "Janeiro" a "Dezembro" e "Total" existem no CSV.')
        except Exception as e:
            raise CommandError(f'Ocorreu um erro inesperado: {e}. Verifique o formato do CSV e as colunas.')