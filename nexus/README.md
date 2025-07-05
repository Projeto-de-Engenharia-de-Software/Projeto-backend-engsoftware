# Projeto Experimentos Projeto Piloto

Projeto back-end focado na utilização do Django(python) para desenvolvimento web e aplicações relacionadas ao Sistema de Agravos e Notificações relacionados à violência de gênero.

## Estrutura do Projeto

```bash
│ manage.py                            # Código .py para o funcionamento do servidor.
│ requirements.txt                     # Requisitos(Libraries) mínimos para o funcionamento do código.
│ .env.example                         # Exemplo de .env para completude de variáveis locais.
├───cadastro                           # App relacionado a função de cadastro do usuário na plataforma.
│   └───urls.py                        # Urls com suas funções aplicadas.
│   └───views.py                       # Funções aplicadas às urls, como a aparição da tela de cadastro de usuário.
├───gestor                             # App relacionado ao controle da classe de Gestor.
│   └───urls.py                        # Urls com suas funções aplicadas.
│   └───views.py                       # Funções aplicadas às urls, como a aparição da tela de boletins do gestor.
├───login                              # App relacionado a funcionalidade login do usuário.
│   └───urls.py                        # Urls com suas funções aplicadas.
│   └───views.py                       # Funções aplicadas às urls, como a aparição da tela de login de usuário.
├───nexus                              # Contém os arquivos base da aplicação, com suas configurações e urls principais.
│   └───settings.py                    # Configurações gerais do projeto, como apps e database.
│   └───urls.py                        # Urls com suas funções aplicadas.
│   └───views.py                       # Funções aplicadas às urls, como a aparição da home bar.
└───pds                                # App relacionado ao controle da classe de Profissional de Saúde.
│   └───urls.py                        # Urls com suas funções aplicadas.
│   └───views.py                       # Funções aplicadas às urls, como a aparição da tela inicial do Profissional.
    ├───experimento-1
    └───experimento-2
```

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente virtual Python e instalar as dependências necessárias:

### Requisitos

- Python 3.13.2^

### 1. Criar o Ambiente Virtual

1. Certifique-se de que o Python está instalado em sua máquina. Recomendamos a versão 3.8 ou superior.
2. No terminal, navegue até a pasta do projeto:
   ```bash
   cd Projeto-Backend-engsoftware
   ```
3. Crie o ambiente virtual:
   ```bash
   python -m venv venv
   ```

### 2. Ativar o Ambiente Virtual

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Renomeie o arquivo `.env.example` para `.env`.
Certifique-se de que o arquivo `.env` está configurado corretamente com as variáveis de ambiente necessárias, como `SECRET_KEY`.

## Executando o Projeto

Para executar o projeto e rodar o servidor, utilize o script principal `manage.py`:

```bash
python manage.py runserver
```

O script `manage.py` é o ponto de entrada para rodar o servidor e manter conexão estável com ele.