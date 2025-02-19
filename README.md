# JOTA Backend Assessment

Implementação do backend para o projeto **JOTA News**, desenvolvido utilizando **Django** e **Django REST Framework**. 

## Requisitos

Requisitos:

- **Docker** e **Docker Compose**
- **Python 3.12**
- **Poetry**

## Configuração do Ambiente

1. **Clone o repositório:**

```sh
git clone https://github.com/pgpostit/jota_backend_assessment.git
cd jota_backend_assessment
```

2. **Configuração do ambiente:**

Crie um arquivo `.env` na raiz do projeto com o conteúdo:

```env
POSTGRES_DB=db
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=chave-secreta
DEBUG=True
```

ps: caso alguma das variáveis de ambiente postgres não esteja no .env, a solução passará a utilizar o sqlite padrão no desenvolvimento do Django. Essa configuração se dá para mostrar, no intuito da avaliação, meus registros, testes e formação de raciocínio. Não daria essa opção em um ambiente de produção.

3. **As dependências podem ser instaladas separadamente com:**

```sh
poetry install
```

4. **Migrações do banco de dados:**

```sh
poetry run python manage.py migrate
```

5. **Crie um superusuário:**

```sh
poetry run python manage.py createsuperuser
```

## Executando o Projeto com Docker

1. **Inicie os serviços:**

```sh
docker-compose up --build
```

2. **Acesse a aplicação:**

A API estará disponível em: `http://localhost:8000`

A documentação Swagger estará disponível em: `http://localhost:8000/swagger/`

## Testes

Para rodar os testes automatizados:

```sh
poetry run pytest
```

## Acesso ao Painel Admin

- URL: `http://localhost:8000/admin/`
- Utilize as credenciais do superusuário criado anteriormente.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.12
- **Framework:** Django 5.1.6, Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JWT (SimpleJWT)
- **Filas Assíncronas:** Celery com Redis
- **CI/CD:** GitHub Actions
- **Containerização:** Docker e Docker Compose

## Obserações de Possíveis Melhorias

- **Mais rotas:** implementar rotas com filtros avançados, permitindo a busca por atributos como nome, autor, categoria, data de publicação, status e outros. Isso agregaria flexibilidade e praticidade ao consumo da API.
- **Programação assíncrona:** para rotas que demandam maior processamento ou acesso a recursos externos, a adoção de programação assíncrona pode melhorar a performance e a experiência do usuário. No entanto, considerando o escopo atual do projeto, essa melhoria é opcional.
- **Modularização da aplicação**: dividir a aplicação em módulos, como news, users, subscriptions, entre outros. Essa abordagem favorece a escalabilidade e a manutenção do código, especialmente em cenários onde categorias, níveis de usuário e regras de leitura podem crescer. Para o escopo atual, a centralização em um único app é aceitável.
- **Modularização dos settings:** separar as configurações do settings.py em múltiplos arquivos facilita a gestão de diferentes ambientes torna o projeto mais seguro e configurável.
- **Paginação**: principalmente os endpoints relacionados a news, pensando em um escopo maior, devem passar por paginação.
- **Documentação e Testes**: Ampliar a documentação da API, detalhando não apenas os endpoints, mas também os fluxos de uso recomendados. Adicionar testes de integração para que todos os cenários de uso sejam cobertos.
- **Observabilidade**: incluir ferramentas de monitoramento e logging.
- **Padrão de commits**: não mantive a frequência e mensagens de commits em um padrão usual de trabalho.