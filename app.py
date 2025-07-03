import streamlit as st
import modulos.calculadora as calculadora
from utils.css import aplicar_estilo
from modulos import (
    pagina_inicial, sobre, cadastro, registro, jornada,
    dashboard, tabela, download, jornada_contratual, login
)

# === Configurações iniciais ===
st.set_page_config(page_title="Cidade Viva Education", layout="wide")
aplicar_estilo()

# === Cabeçalho ===
col1, col2 = st.columns([6, 1])
with col1:
    st.image("imagens/logo_azul.png", width=220)

with col2:
    if 'autenticado' in st.session_state and st.session_state['autenticado']:
        st.markdown(
            f"""
            <div style='text-align:right;'>
                <strong>👤 {st.session_state['usuario_nome']}</strong>  
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)

# === Verificar Logout ===
query_params = st.query_params
if 'logout' in query_params:
    for chave in ['autenticado', 'usuario_nome', 'usuario_email', 'usuario_cargo']:
        if chave in st.session_state:
            del st.session_state[chave]
    st.rerun()

# === Controle de Login ===
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    login.login_usuario()  # Login padrão para usuários cadastrados
else:
    cargo = st.session_state['usuario_cargo']

    # === Menu com base no cargo ===
    if cargo == 'gerente':
        menu = [
            "Página Inicial", "Sobre", "Cadastro", "Registro de Negociação", "Jornada de Relacionamento", "Jornada Contratual", "Calculadora", 
            "Dashboard", "Tabela Geral", "Gestão de Usuários", "Formulário", "Download", "Sair"
        ]
    elif cargo in ['consultor', 'supervisor', 'assistente']:
        menu = [
            "Página Inicial", "Sobre", "Cadastro", "Registro de Negociação", "Jornada de Relacionamento", "Jornada Contratual", "Calculadora",
            "Dashboard", "Tabela Geral", "Formulário", "Download", "Sair"
        ]
    elif cargo == "formulario":
        menu = ["Formulário", "Sair"]
    else:
        menu = ["Sair"]

    escolha = st.sidebar.selectbox("Menu", menu)

    # === Abas conforme escolha ===
    if escolha == "Página Inicial":
        pagina_inicial.carregar()

    elif escolha == "Dashboard":
        dashboard.carregar()

    elif escolha == "Registro de Negociação":
        registro.carregar()

    elif escolha == "Jornada de Relacionamento":
        jornada.carregar()

    elif escolha == "Cadastro":
        cadastro.carregar()

    elif escolha == "Tabela Geral":
        tabela.carregar()

    elif escolha == "Jornada Contratual":
        jornada_contratual.carregar()

    elif escolha == "Gestão de Usuários":
        from modulos import gestao_usuarios
        gestao_usuarios.carregar()

    elif escolha == "Download":
        download.carregar()

    elif escolha == "Formulário":
        from modulos import formulario
        formulario.carregar()

    elif escolha == "Sobre":
        sobre.carregar()
    
    elif escolha == "Calculadora":
        calculadora.carregar()

    elif escolha == "Sair":
        for chave in ['autenticado', 'usuario_nome', 'usuario_email', 'usuario_cargo']:
            if chave in st.session_state:
                del st.session_state[chave]
        st.rerun()




# === Footer ===
st.markdown(
    """
    <div class='footer-custom'>
        <p style="margin: 0; font-weight: 600;">Relatórios e Inteligência Comercial</p>
        <p style="margin: 0; font-weight: 600;">Central de Inteligência Analítica</p>
        <p style="margin: 4px 0 0;">© 2025 Cidade Viva Education - Aplicativo de Gerenciamento Comercial</p>
    </div>
    """,
    unsafe_allow_html=True
)
