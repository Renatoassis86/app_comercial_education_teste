import streamlit as st
import psycopg2.extras
from utils.conexao import conectar
from utils.estados_cidades import carregar_estados
from utils.banners import exibir_banner


def carregar():
    exibir_banner("banner_cadastro")
    st.markdown("<h2 style='color:#1f538d;'>Formulário de Cadastro das Escolas</h2>", unsafe_allow_html=True)

    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT nome_escola FROM escolas")
    escolas_cadastradas = [row[0] for row in cursor.fetchall()]

    nome_escola_selecionada = st.selectbox(
        "Selecionar Escola para Atualizar (opcional)", [""] + escolas_cadastradas)

    estados = carregar_estados()
    estado_siglas = [e[0] for e in estados]

    dados = {}
    if nome_escola_selecionada:
        cursor.execute(
            "SELECT * FROM escolas WHERE nome_escola = %s", (nome_escola_selecionada,))
        dados = cursor.fetchone()

    st.subheader("Dados da Escola")
    nome_escola = st.text_input("Nome da Escola", value=dados.get("nome_escola", "") if dados else "")
    cnpj = st.text_input("CNPJ", value=dados.get("cnpj", "") if dados else "")

    col1, col2 = st.columns(2)
    rua = col1.text_input("Rua", value=dados.get("rua", "") if dados else "")
    numero = col2.text_input("Número", value=dados.get("numero", "") if dados else "")

    bairro = st.text_input("Bairro", value=dados.get("bairro", "") if dados else "")

    col3, col4 = st.columns(2)
    cidade = col3.text_input("Cidade", value=dados.get("cidade", "") if dados else "")
    estado = col4.selectbox(
        "Estado",
        options=[""] + estado_siglas,
        index=(estado_siglas.index(dados["estado"]) + 1 if dados and dados.get("estado") in estado_siglas else 0)
    )

    cep = st.text_input("CEP", value=dados.get("cep", "") if dados else "")
    telefone = st.text_input("Telefone", value=dados.get("telefone", "") if dados else "")
    email = st.text_input("Email", value=dados.get("email", "") if dados else "")
    complemento = st.text_input("Complemento", value=dados.get("complemento", "") if dados else "")

    st.subheader("Dados do Contato")
    contato_nome = st.text_input("Nome do Contato", value=dados.get("contato_nome", "") if dados else "")
    contato_cargo = st.selectbox(
        "Cargo do Contato",
        ["", "Mantenedor", "Gestor", "Diretor", "Coordenador"],
        index=(["Mantenedor", "Gestor", "Diretor", "Coordenador"].index(dados.get("contato_cargo")) + 1 if dados and dados.get("contato_cargo") in ["Mantenedor", "Gestor", "Diretor", "Coordenador"] else 0)
    )

    diretor_nome = st.text_input("Nome do Diretor", value=dados.get("diretor_nome", "") if dados else "")

    perfil_pedagogico = st.selectbox(
        "Perfil Pedagógico",
        ["", "Cristã católica", "Cristã Evangelica", "Educação por princípio", "Cristã Clássica", "Convencional (Educação Moderna)"],
        index=(["Cristã católica", "Cristã Evangelica", "Educação por princípio", "Cristã Clássica", "Convencional (Educação Moderna)"].index(dados.get("perfil_pedagogico")) + 1 if dados and dados.get("perfil_pedagogico") in [
            "Cristã católica", "Cristã Evangelica", "Educação por princípio", "Cristã Clássica", "Convencional (Educação Moderna)"] else 0)
    )

    origem_lead = st.selectbox(
        "Origem do Lead",
        ["", "Feira", "Instagram", "Network", "Envio de material (Livros)", "Opening Company", "ABEKA", "ACSI", "Congresso Internacional de ECC", "Indicação de outra escola", "Outros"],
        index=(["Feira", "Instagram", "Network", "Envio de material (Livros)", "Opening Company", "ABEKA", "ACSI", "Congresso Internacional de ECC", "Indicação de outra escola", "Outros"].index(
            dados.get("origem_lead")) + 1 if dados and dados.get("origem_lead") in [
            "Feira", "Instagram", "Network", "Envio de material (Livros)", "Opening Company", "ABEKA", "ACSI", "Congresso Internacional de ECC", "Indicação de outra escola", "Outros"] else 0)
    )

    responsavel_pedagogico = st.selectbox(
        "Responsável pelo Cadastro",
        ["", "Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"],
        index=(["Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"].index(
            dados.get("responsavel_pedagogico")) + 1 if dados and dados.get("responsavel_pedagogico") in [
            "Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"] else 0)
    )

    escola_paideia = st.selectbox(
        "A escola é Paideia?", ["", "Sim", "Não"],
        index=(["Sim", "Não"].index(dados.get("escola_paideia")) + 1 if dados and dados.get("escola_paideia") in ["Sim", "Não"] else 0)
    )

    st.subheader("Quantidade Estimada de Alunos")
    infantil = st.number_input("Infantil", min_value=0, step=1, value=int(dados.get("qtd_infantil", 0)) if dados else 0)
    fund1 = st.number_input("Fundamental 1", min_value=0, step=1, value=int(dados.get("qtd_fund1", 0)) if dados else 0)
    fund2 = st.number_input("Fundamental 2", min_value=0, step=1, value=int(dados.get("qtd_fund2", 0)) if dados else 0)
    medio = st.number_input("Ensino Médio", min_value=0, step=1, value=int(dados.get("qtd_medio", 0)) if dados else 0)

    if st.button("Salvar Dados"):
        try:
            if nome_escola_selecionada:
                cursor.execute("""
                    UPDATE escolas SET
                        nome_escola=%s, cnpj=%s, rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s, cep=%s,
                        telefone=%s, email=%s, complemento=%s, contato_nome=%s, contato_cargo=%s, diretor_nome=%s,
                        perfil_pedagogico=%s, origem_lead=%s, responsavel_pedagogico=%s, escola_paideia=%s,
                        qtd_infantil=%s, qtd_fund1=%s, qtd_fund2=%s, qtd_medio=%s
                    WHERE nome_escola = %s
                """, (
                    nome_escola, cnpj, rua, numero, bairro, cidade, estado, cep, telefone, email, complemento,
                    contato_nome, contato_cargo, diretor_nome, perfil_pedagogico, origem_lead, responsavel_pedagogico,
                    escola_paideia, infantil, fund1, fund2, medio, nome_escola_selecionada
                ))
            else:
                cursor.execute("""
                    INSERT INTO escolas (
                        nome_escola, cnpj, rua, numero, bairro, cidade, estado, cep, telefone, email, complemento,
                        contato_nome, contato_cargo, diretor_nome, perfil_pedagogico, origem_lead,
                        responsavel_pedagogico, escola_paideia, qtd_infantil, qtd_fund1, qtd_fund2, qtd_medio
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nome_escola, cnpj, rua, numero, bairro, cidade, estado, cep, telefone, email, complemento,
                    contato_nome, contato_cargo, diretor_nome, perfil_pedagogico, origem_lead,
                    responsavel_pedagogico, escola_paideia, infantil, fund1, fund2, medio
                ))

            conn.commit()
            st.success("✅ Dados salvos com sucesso!")

        except Exception as e:
            st.error(f"❌ Erro ao salvar: {e}")

    cursor.close()
    conn.close()
