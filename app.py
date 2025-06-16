
import streamlit as st
from utils.css import aplicar_estilo
from utils.banners import exibir_banner
from modulos import pagina_inicial, sobre, cadastro, registro, jornada, dashboard, tabela, download, jornada_contratual


st.set_page_config(page_title="Cidade Viva Education", layout="wide")
aplicar_estilo()

# Topo com logo e status
col1, col2 = st.columns([6, 1])
with col1:
    st.image("imagens/logo_azul.png", width=200)

st.markdown("<hr>", unsafe_allow_html=True)

# Menu de navegação em abas centralizado
abas = st.tabs([
    "Página Inicial", "Sobre", "Cadastro", "Registro",
    "Jornada", "Dashboard", "Tabela", "Download", "Jornada Contratual"
])

# Conteúdo por aba
with abas[0]:
    pagina_inicial.carregar()
with abas[1]:
    sobre.carregar()
with abas[2]:
    cadastro.carregar()
with abas[3]:
    registro.carregar()
with abas[4]:
    jornada.carregar()
with abas[5]:
    dashboard.carregar()
with abas[6]:
    tabela.carregar()
with abas[7]:
    download.carregar()  
with abas[8]:
    jornada_contratual.carregar()


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




