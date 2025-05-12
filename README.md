
# Aplicativo de Gerenciamento Comercial - Cidade Viva Education

Sistema de apoio à operação comercial e relacional da Cidade Viva Education. Desenvolvido com Streamlit, o projeto permite cadastrar escolas, registrar interações, visualizar métricas comerciais e realizar acompanhamentos estratégicos com base em dados.

O aplicativo permite integração com bancos de dados MySQL ou PostgreSQL, conforme configuração do ambiente.

---

## Funcionalidades

- Cadastro de escolas com campos administrativos, pedagógicos e estratégicos
- Registro de interações com leads: data, canal, encaminhamento, responsável
- Dashboard interativo com múltiplas dimensões:
  - Análise por estágio do lead e prontidão
  - Distribuição por responsável e meio de contato
  - Top escolas por potencial financeiro
  - Funil de negociação e taxa de conversão
  - Tempo médio entre interações e tempo desde o último contato
  - Nuvem de palavras com resumos dos registros
- Filtros dinâmicos por escola, responsável, estado, porte e período
- Tabela completa com dados da escola, contato, fase atual e interações

---

## Integração com Banco de Dados

Este sistema suporta integração com:

- MySQL
- PostgreSQL

O driver é definido em `utils/conexao.py`. As credenciais são armazenadas de forma segura em um arquivo `.env`. O ambiente de execução não depende do banco escolhido, desde que esteja corretamente configurado.

---

## Requisitos e Execução

1. Clone o repositório:

```bash
git clone https://github.com/Renatoassis86/app_comercial_education.git
cd app_comercial_education
```

2. Crie o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate  # ou source .venv/bin/activate no Linux/Mac
```

3. Instale os requisitos:

```bash
pip install -r requirements.txt
```

4. Configure o arquivo `.env` com as variáveis de conexão ao banco:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=usuario
DB_PASSWORD=senha
DB_NAME=comercialcve
```

5. Execute a aplicação:

```bash
streamlit run app.py
```

---

## Estrutura do Projeto

```
📦 paideia_app/
├── app.py
├── .env
├── requirements.txt
├── README.md
├── modulos/
│   ├── cadastro.py
│   ├── dashboard.py
│   ├── jornada.py
│   ├── registro.py
│   ├── sobre.py
│   ├── tabela.py
├── utils/
│   ├── conexao.py
│   ├── css.py
│   ├── banners.py
│   ├── helpers.py
```

---

## Licenciamento e Suporte

Este sistema foi desenvolvido para uso interno pela equipe Cidade Viva Education.  
Para contato institucional ou suporte técnico: renato.consultoria@cidadeviva.org
