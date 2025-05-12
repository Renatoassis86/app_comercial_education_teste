import streamlit as st
import psycopg2.extras
import pandas as pd
from utils.banners import exibir_banner
from utils.conexao import conectar

# === Funções Auxiliares === #

def calcular_potencial_financeiro(infantil, fund1, fund2, medio, ticket=1000):
    return (infantil + fund1 + fund2 + medio) * ticket

def calcular_classificacao(probabilidade, potencial):
    # Exemplo simples com base em benchmarks de CRM
    if probabilidade >= 70 and potencial >= 100000:
        return "Lead Quente"
    elif probabilidade >= 40 and potencial >= 50000:
        return "Lead Morno"
    else:
        return "Lead Frio"

def calcular_probabilidade(interesse, prontidao, abertura):
    pesos = {
        "Muito Baixo": 0, "Baixo": 1, "Médio": 2, "Alto": 3, "Muito Alto": 4,
        "Negociação Parada": 0, "Nova Reunião Necessária": 1, "Esperando Retorno": 2, 
        "Apresentação em Andamento": 3, "Contrato Enviado": 4, "Contrato Assinado": 5,
        "Nenhuma": 0, "Baixa": 1, "Média": 2, "Alta": 3
    }
    total = pesos.get(interesse, 0) + pesos.get(prontidao, 0) + pesos.get(abertura, 0)
    return int((total / 12) * 100)

def get_nomes_escolas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_escola FROM escolas")
        resultados = cursor.fetchall()
        conn.close()
        return {nome: id for id, nome in resultados}
    except:
        return {}

# === Página === #
def carregar():
    exibir_banner("banner_registro")
    st.markdown("<h2 style='color:#1f538d;'>Registro de Relacionamento Comercial</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='caixa-branca'>
    <p>Este formulário tem como objetivo registrar todas as interações comerciais e pedagógicas com as escolas, permitindo análise contínua e estratégica do relacionamento.</p>
    <p>Essas informações permitem:</p>
    <ul>
        <li>Diagnóstico da maturidade do lead;</li>
        <li>Priorização por potencial de retorno;</li>
        <li>Identificação de gargalos no processo de negociação;</li>
        <li>Geração automática de métricas com base estatística, como:</li>
        <ul>
            <li><strong>Probabilidade de Fechamento</strong>: média ponderada de interesse, prontidão e abertura para proposta, normalizada de 0 a 100;</li>
            <li><strong>Classificação do Lead</strong>: categorização com base em clusters comerciais (Frio, Morno, Quente) pela combinação de probabilidade e potencial financeiro;</li>
            <li><strong>Potencial Financeiro</strong>: multiplicação da quantidade de alunos por segmento pelo ticket médio (R$ 1.000);</li>
        </ul>
    </ul>
    <p>Essas métricas seguem lógica semelhante às utilizadas em CRMs de mercado como Salesforce, Pipedrive e RD Station, com fundamentação prática e estatística.</p>
    </div>
    """, unsafe_allow_html=True)

    escolas_dict = get_nomes_escolas()
    escolas_nomes = list(escolas_dict.keys())

    with st.form("formulario_registro"):
        st.markdown("### 📝 Informações da Negociação")
        nome_escola = st.selectbox("Nome da Escola (Escolha uma escola previamente cadastrada)", [""] + escolas_nomes, key="registro_escola")
        st.date_input("Data do Contato (Data da interação)", key="registro_data")
        st.text_area("Resumo do Contato (Resumo da conversa e pontos discutidos)", key="registro_resumo")
        st.selectbox("Meio de Contato (Canal utilizado para interação)", ["", "Presencial", "WhatsApp", "E-mail", "Telefone", "Videoconferência"], key="registro_meio")
        st.text_input("Contato da Escola (Pessoa que participou da conversa)", key="registro_contato")
        st.selectbox("Cargo do Contato (Cargo da pessoa da escola)", ["", "Mantenedor", "Gestor", "Diretor", "Coordenador", "Professor", "Secretário(a)", "Outro"], key="registro_cargo")
        st.selectbox("Responsável pelo Contato (Agente do Education)", ["", "Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"], key="registro_responsavel")

        st.markdown("### 🔍 Diagnóstico de Interesse")
        st.selectbox("Interesse (Nível de interesse percebido)", ["", "Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"], key="registro_interesse")
        st.selectbox("Prontidão (Fase da negociação)", ["", "Negociação Parada", "Nova Reunião Necessária", "Esperando Retorno", "Apresentação em Andamento", "Contrato Enviado", "Contrato Assinado"], key="registro_prontidao")
        st.selectbox("Abertura para Proposta (Disposição para avançar)", ["", "Nenhuma", "Baixa", "Média", "Alta"], key="registro_abertura")
        st.selectbox("Encaminhamento Atual (Próximo passo previsto)", ["", "Agendamento de Reunião", "Apresentação Currículo", "Envio de Material", "Nova Visita", "Contato Futuro", "Elaboração de Contrato", "Contrato Enviado", "Contrato Assinado"], key="registro_encaminhamento")

        gerar = st.form_submit_button("📊 Gerar Métricas")

        infantil = fund1 = fund2 = medio = 0
        if nome_escola and escolas_dict.get(nome_escola):
            try:
                conn = conectar()
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("SELECT qtd_infantil, qtd_fund1, qtd_fund2, qtd_medio FROM escolas WHERE id = %s", (escolas_dict[nome_escola],))
                dados = cursor.fetchone()
                if dados:
                    infantil = dados["qtd_infantil"] or 0
                    fund1 = dados["qtd_fund1"] or 0
                    fund2 = dados["qtd_fund2"] or 0
                    medio = dados["qtd_medio"] or 0
                conn.close()
            except Exception as e:
                st.warning(f"Erro ao buscar dados da escola: {e}")

        if gerar:
            potencial = calcular_potencial_financeiro(infantil, fund1, fund2, medio)
            probabilidade = calcular_probabilidade(st.session_state.registro_interesse, st.session_state.registro_prontidao, st.session_state.registro_abertura)
            classificacao = calcular_classificacao(probabilidade, potencial)

            st.markdown("### 🔎 Métricas Estratégicas")
            col1, col2, col3 = st.columns(3)
            col1.metric("Potencial Financeiro", f"R$ {potencial:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            col2.metric("Probabilidade", f"{probabilidade}%")
            col3.metric("Classificação", classificacao)

        salvar = st.form_submit_button("💾 Salvar Registro")
        if salvar:
            if not nome_escola or nome_escola not in escolas_dict:
                st.warning("⚠️ Por favor, selecione uma escola cadastrada para registrar o relacionamento.")
            else:
                try:
                    # Recalcular as métricas antes de salvar
                    potencial = calcular_potencial_financeiro(infantil, fund1, fund2, medio)
                    probabilidade = calcular_probabilidade(
                        st.session_state.registro_interesse,
                        st.session_state.registro_prontidao,
                        st.session_state.registro_abertura
                    )
                    classificacao = calcular_classificacao(probabilidade, potencial)

                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO registros (
                            id_escola, data_contato, resumo, meio_contato,
                            interesse, prontidao, abertura, encaminhamento,
                            responsavel, contato, cargo, qtd_infantil, qtd_fund1,
                            qtd_fund2, qtd_medio, potencial_financeiro,
                            classificacao_lead, probabilidade
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        escolas_dict.get(nome_escola),
                        st.session_state.registro_data,
                        st.session_state.registro_resumo,
                        st.session_state.registro_meio,
                        st.session_state.registro_interesse,
                        st.session_state.registro_prontidao,
                        st.session_state.registro_abertura,
                        st.session_state.registro_encaminhamento,
                        st.session_state.registro_responsavel,
                        st.session_state.registro_contato,
                        st.session_state.registro_cargo,
                        infantil, fund1, fund2, medio,
                        potencial,
                        classificacao,
                        probabilidade
                    ))
                    conn.commit()
                    conn.close()
                    st.success("✅ Registro salvo com sucesso! Atualize a página para novo cadastro.")
                except Exception as e:
                    st.error(f"Erro ao salvar no banco de dados: {e}")
