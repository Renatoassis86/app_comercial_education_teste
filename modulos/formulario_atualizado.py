
import streamlit as st
from datetime import date
from utils.conexao import conectar
from utils.email_utils import enviar_email_notificacao

def carregar():
    st.markdown("<h2 style='color:#1f538d;'>Formulário de Pré-Cadastro Escolar</h2>", unsafe_allow_html=True)

    st.markdown("#### Responsável pelo Preenchimento")
    email_responsavel = st.text_input("Seu email", placeholder="Digite e pressione Enter", key="email_responsavel")

    st.markdown("#### Dados da Escola")
    nome_escola = st.text_input("Nome da Escola", key="nome_escola")
    cnpj = st.text_input("CNPJ", key="cnpj")
    rua = st.text_input("Rua", key="rua")
    numero = st.text_input("Número", key="numero")
    complemento = st.text_input("Complemento", key="complemento")
    bairro = st.text_input("Bairro", key="bairro")
    cidade = st.text_input("Cidade", key="cidade")
    estado = st.selectbox("Estado (UF)", ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                                          "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                                          "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], key="estado")
    cep = st.text_input("CEP", key="cep")

    st.markdown("#### Informações Acadêmicas")
    infantil2 = st.number_input("Qtd Infantil 2", min_value=0, key="infantil2")
    infantil3 = st.number_input("Qtd Infantil 3", min_value=0, key="infantil3")
    infantil4 = st.number_input("Qtd Infantil 4", min_value=0, key="infantil4")
    infantil5 = st.number_input("Qtd Infantil 5", min_value=0, key="infantil5")
    fund1_ano1 = st.number_input("Qtd 1º Ano Fund I", min_value=0, key="fund1_ano1")
    data_inicio = st.date_input("Previsão início do ano letivo 2026", key="data_inicio")
    data_fim = st.date_input("Previsão fim do ano letivo 2026", key="data_fim")
    formato_ano = st.selectbox("Formato do ano letivo", ["Bimestre", "Trimestre"], key="formato_ano")
    observacoes = st.text_area("Observações adicionais", key="observacoes")

    st.markdown("#### Representante Legal")
    rl_nome = st.text_input("Nome", key="rl_nome")
    rl_cpf = st.text_input("CPF", key="rl_cpf")
    rl_rg = st.text_input("RG", key="rl_rg")
    rl_orgao = st.text_input("Órgão Emissor", key="rl_orgao")
    rl_rua = st.text_input("Rua", key="rl_rua")
    rl_numero = st.text_input("Número", key="rl_numero")
    rl_complemento = st.text_input("Complemento", key="rl_complemento")
    rl_bairro = st.text_input("Bairro", key="rl_bairro")
    rl_cidade = st.text_input("Cidade", key="rl_cidade")
    rl_estado = st.selectbox("Estado (UF)", ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                                             "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                                             "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], key="rl_estado")
    rl_cep = st.text_input("CEP", key="rl_cep")
    rl_email = st.text_input("Email", key="rl_email")
    rl_celular = st.text_input("Celular", key="rl_celular")

    st.markdown("#### Representante Financeiro")
    rf_nome = st.text_input("Nome", key="rf_nome")
    rf_cpf = st.text_input("CPF", key="rf_cpf")
    rf_rg = st.text_input("RG", key="rf_rg")
    rf_orgao = st.text_input("Órgão Emissor", key="rf_orgao")
    rf_email = st.text_input("Email", key="rf_email")
    rf_celular = st.text_input("Celular", key="rf_celular")

    st.markdown("#### Representante Pedagógico")
    rp_nome = st.text_input("Nome", key="rp_nome")
    rp_cpf = st.text_input("CPF", key="rp_cpf")
    rp_rg = st.text_input("RG", key="rp_rg")
    rp_orgao = st.text_input("Órgão Emissor", key="rp_orgao")
    rp_email = st.text_input("Email", key="rp_email")
    rp_celular = st.text_input("Celular", key="rp_celular")

    if st.button("📤 Enviar Formulário"):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO formularios (
                    data_envio, email_responsavel,
                    nome_escola, cnpj, rua, numero, complemento, bairro, cidade, estado, cep,
                    infantil2, infantil3, infantil4, infantil5, fund1_ano1,
                    data_inicio_letivo, data_fim_letivo, formato_ano_letivo, observacoes,
                    nome_representante_legal, cpf_representante_legal, rg_representante_legal, orgao_emissor_representante_legal,
                    rua_representante_legal, numero_representante_legal, complemento_representante_legal, bairro_representante_legal,
                    cidade_representante_legal, estado_representante_legal, cep_representante_legal,
                    email_representante_legal, celular_representante_legal,
                    nome_representante_financeiro, cpf_representante_financeiro, rg_representante_financeiro, orgao_emissor_representante_financeiro,
                    email_representante_financeiro, celular_representante_financeiro,
                    nome_representante_pedagogico, cpf_representante_pedagogico, rg_representante_pedagogico, orgao_emissor_representante_pedagogico,
                    email_representante_pedagogico, celular_representante_pedagogico
                ) VALUES (
                    CURRENT_TIMESTAMP, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s,
                    %s, %s, %s, %s,
                    %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                )
            """, (
                email_responsavel,
                nome_escola, cnpj, rua, numero, complemento, bairro, cidade, estado, cep,
                infantil2, infantil3, infantil4, infantil5, fund1_ano1,
                data_inicio, data_fim, formato_ano, observacoes,
                rl_nome, rl_cpf, rl_rg, rl_orgao,
                rl_rua, rl_numero, rl_complemento, rl_bairro,
                rl_cidade, rl_estado, rl_cep,
                rl_email, rl_celular,
                rf_nome, rf_cpf, rf_rg, rf_orgao,
                rf_email, rf_celular,
                rp_nome, rp_cpf, rp_rg, rp_orgao,
                rp_email, rp_celular
            ))
            conn.commit()
            cursor.close()
            conn.close()
            enviar_email_notificacao(nome_escola, email_responsavel)
            st.success("✅ Formulário enviado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao enviar formulário: {e}")
