import streamlit as st
import psycopg2.extras
import pandas as pd
from utils.conexao import conectar
from utils.estados_cidades import carregar_estados
from utils.banners import exibir_banner

def escola_ja_existe(cursor, nome_digitado, cnpj_digitado):
    cursor.execute("""
        SELECT COUNT(*) FROM escolas 
        WHERE LOWER(TRIM(nome_escola)) = %s
    """, (nome_digitado,))
    duplicado_nome = cursor.fetchone()[0]

    duplicado_cnpj = 0
    if cnpj_digitado:
        cursor.execute("""
            SELECT COUNT(*) FROM escolas 
            WHERE REPLACE(REPLACE(REPLACE(cnpj, '.', ''), '/', ''), '-', '') = %s
        """, (cnpj_digitado,))
        duplicado_cnpj = cursor.fetchone()[0]

    return duplicado_nome > 0 or duplicado_cnpj > 0, duplicado_nome, duplicado_cnpj

def carregar():
    exibir_banner("banner_cadastro")
    st.markdown("<h2 style='color:#1f538d;'>Formulário de Cadastro das Escolas</h2>", unsafe_allow_html=True)

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_escola FROM escolas")
        escolas_existentes = [row[0] for row in cursor.fetchall()]
        conn.close()
    except:
        escolas_existentes = []

    nome_escola_selecionada = st.selectbox("Selecionar Escola para Atualizar (opcional)", [""] + escolas_existentes, key="form_escola_selecionada")

    estados = carregar_estados()
    estado_siglas = [e[0] for e in estados]

    dados = {}
    if nome_escola_selecionada:
        try:
            conn = conectar()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM escolas WHERE nome_escola = %s", (nome_escola_selecionada,))
            dados = cursor.fetchone()
            conn.close()
        except:
            st.warning("Erro ao carregar dados da escola.")

    mensagem_sucesso = False

    with st.form("formulario_escola", clear_on_submit=False):
        st.subheader("Dados da Escola")
        st.text_input("Nome da Escola", value=dados.get("nome_escola", "") if dados else "", key="form_nome_escola")
        st.text_input("CEP", value=dados.get("cep", "") if dados else "", key="form_cep")
        st.text_input("Telefone", value=dados.get("telefone", "") if dados else "", key="form_telefone")
        st.text_input("Email", value=dados.get("email", "") if dados else "", key="form_email")
        st.text_input("CNPJ", value=dados.get("cnpj", "") if dados else "", key="form_cnpj")
        st.text_input("Rua", value=dados.get("rua", "") if dados else "", key="form_rua")
        st.text_input("Bairro", value=dados.get("bairro", "") if dados else "", key="form_bairro")
        st.text_input("Número", value=dados.get("numero", "") if dados else "", key="form_numero")
        st.text_input("Complemento", value=dados.get("complemento", "") if dados else "", key="form_complemento")
        st.selectbox("Estado", options=[""] + estado_siglas, index=(estado_siglas.index(dados["estado"]) + 1 if dados and dados["estado"] in estado_siglas else 0), key="form_estado")
        st.text_input("Cidade", value=dados.get("cidade", "") if dados else "", key="form_cidade")

        st.subheader("Dados do Contato")
        st.text_input("Nome do Contato Principal", value=dados.get("contato_nome", "") if dados else "", key="form_contato_nome")
        st.selectbox("Cargo do Contato", ["", "Mantenedor", "Gestor", "Diretor", "Coordenador"], index=(["Mantenedor", "Gestor", "Diretor", "Coordenador"].index(dados.get("contato_cargo")) + 1 if dados and dados.get("contato_cargo") in ["Mantenedor", "Gestor", "Diretor", "Coordenador"] else 0), key="form_contato_cargo")
        st.text_input("Nome do Diretor", value=dados.get("diretor_nome", "") if dados else "", key="form_diretor_nome")

        st.selectbox("Perfil Pedagógico", ["", "Cristã católica", "Cristã Evangelica", "Educação por princípio", "Cristã Clássica", "Convencional (Educação Moderna)"], index=(["Cristã católica", "Cristã Evangelica", "Educação por princípio", "Cristã Clássica", "Convencional (Educação Moderna)"].index(dados.get("perfil_pedagogico")) + 1 if dados and dados.get("perfil_pedagogico") in ["Cristã católica", "Cristã Evangelica", "Educação por princípio", "Cristã Clássica", "Convencional (Educação Moderna)"] else 0), key="form_perfil_pedagogico")

        st.selectbox("Origem do Lead", ["", "Feira", "Instagram", "Network", "Envio de material (Livros)", "Opening Company", "ABEKA", "ACSI", "Outros"], index=(["Feira", "Instagram", "Network", "Envio de material (Livros)", "Opening Company", "ABEKA", "ACSI", "Outros"].index(dados.get("origem_lead")) + 1 if dados and dados.get("origem_lead") in ["Feira", "Instagram", "Network", "Envio de material (Livros)", "Opening Company", "ABEKA", "ACSI", "Outros"] else 0), key="form_origem_lead")

        st.selectbox("Responsável pelo Cadastro", ["", "Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"], index=(["Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"].index(dados.get("responsavel_pedagogico")) + 1 if dados and dados.get("responsavel_pedagogico") in ["Raissa Fernandes", "Ranieri França", "Emmanuel Pires", "Isabela Rolim", "Renato Assis", "Thiago Dutra", "Bia Ruggeri", "Jhon Jarison", "Layla Ramos"] else 0), key="form_responsavel_pedagogico")

        st.selectbox("A escola é Paideia?", ["", "Sim", "Não"], index=(["Sim", "Não"].index(dados.get("escola_paideia")) + 1 if dados and dados.get("escola_paideia") in ["Sim", "Não"] else 0), key="form_escola_paideia")

        st.subheader("Quantidade Estimada de Alunos")
        st.number_input("Infantil", min_value=0, step=1, format="%d", value=int(dados.get("qtd_infantil", 0)) if dados else 0, key="form_qtd_infantil")
        st.number_input("Fundamental 1", min_value=0, step=1, format="%d", value=int(dados.get("qtd_fund1", 0)) if dados else 0, key="form_qtd_fund1")
        st.number_input("Fundamental 2", min_value=0, step=1, format="%d", value=int(dados.get("qtd_fund2", 0)) if dados else 0, key="form_qtd_fund2")
        st.number_input("Ensino Médio", min_value=0, step=1, format="%d", value=int(dados.get("qtd_medio", 0)) if dados else 0, key="form_qtd_medio")

        salvar = st.form_submit_button("📂 Salvar/Atualizar")

    if salvar:
        try:
            conn = conectar()
            cursor = conn.cursor()

            nome_digitado = st.session_state.form_nome_escola.strip().lower()
            cnpj_digitado = st.session_state.form_cnpj.replace(".", "").replace("/", "").replace("-", "").strip()

            if nome_escola_selecionada:
                cursor.execute("""UPDATE escolas SET nome_escola=%s, cep=%s, telefone=%s, email=%s, cnpj=%s, rua=%s, bairro=%s,
                    numero=%s, complemento=%s, estado=%s, cidade=%s, contato_nome=%s, contato_cargo=%s,
                    diretor_nome=%s, perfil_pedagogico=%s, origem_lead=%s, responsavel_pedagogico=%s,
                    escola_paideia=%s, qtd_infantil=%s, qtd_fund1=%s, qtd_fund2=%s, qtd_medio=%s
                    WHERE nome_escola=%s""", (
                    st.session_state.form_nome_escola.strip(),
                    st.session_state.form_cep,
                    st.session_state.form_telefone,
                    st.session_state.form_email,
                    st.session_state.form_cnpj.strip(),
                    st.session_state.form_rua,
                    st.session_state.form_bairro,
                    st.session_state.form_numero,
                    st.session_state.form_complemento,
                    st.session_state.form_estado,
                    st.session_state.form_cidade,
                    st.session_state.form_contato_nome,
                    st.session_state.form_contato_cargo,
                    st.session_state.form_diretor_nome,
                    st.session_state.form_perfil_pedagogico,
                    st.session_state.form_origem_lead,
                    st.session_state.form_responsavel_pedagogico,
                    st.session_state.form_escola_paideia,
                    st.session_state.form_qtd_infantil,
                    st.session_state.form_qtd_fund1,
                    st.session_state.form_qtd_fund2,
                    st.session_state.form_qtd_medio,
                    nome_escola_selecionada
                ))
                mensagem_sucesso = True

            else:
                ja_existe, duplicado_nome, duplicado_cnpj = escola_ja_existe(cursor, nome_digitado, cnpj_digitado)
                st.write(f"🔎 Duplicado por nome? {duplicado_nome} | Duplicado por CNPJ? {duplicado_cnpj}")

                if ja_existe:
                    st.warning("⚠️ Já existe uma escola cadastrada com este nome ou CNPJ (mesmo com grafia diferente).")
                    conn.close()
                    return

                cursor.execute("""INSERT INTO escolas (
                    nome_escola, cep, telefone, email, cnpj, rua, bairro, numero, complemento,
                    estado, cidade, contato_nome, contato_cargo, diretor_nome,
                    perfil_pedagogico, origem_lead, responsavel_pedagogico, escola_paideia,
                    qtd_infantil, qtd_fund1, qtd_fund2, qtd_medio
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    st.session_state.form_nome_escola.strip(),
                    st.session_state.form_cep,
                    st.session_state.form_telefone,
                    st.session_state.form_email,
                    st.session_state.form_cnpj.strip(),
                    st.session_state.form_rua,
                    st.session_state.form_bairro,
                    st.session_state.form_numero,
                    st.session_state.form_complemento,
                    st.session_state.form_estado,
                    st.session_state.form_cidade,
                    st.session_state.form_contato_nome,
                    st.session_state.form_contato_cargo,
                    st.session_state.form_diretor_nome,
                    st.session_state.form_perfil_pedagogico,
                    st.session_state.form_origem_lead,
                    st.session_state.form_responsavel_pedagogico,
                    st.session_state.form_escola_paideia,
                    st.session_state.form_qtd_infantil,
                    st.session_state.form_qtd_fund1,
                    st.session_state.form_qtd_fund2,
                    st.session_state.form_qtd_medio
                ))
                mensagem_sucesso = True

            conn.commit()
            conn.close()

            if mensagem_sucesso:
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✅ Escola cadastrada ou atualizada com sucesso! Atualize a página para iniciar um novo cadastro.")

        except Exception as e:
            st.error(f"❌ Erro ao salvar: {e}")


    st.markdown("---")
    st.subheader("📥 Importar Escolas via Planilha Excel")

    arquivo = st.file_uploader("Escolha um arquivo Excel com os dados das escolas (exceto coluna 'id')", type=["xlsx"])

    if arquivo is not None:
        try:
            df = pd.read_excel(arquivo).fillna("")
            st.write("Pré-visualização dos dados:", df)

            with st.form("formulario_importacao_escolas"):
                importar = st.form_submit_button("📤 Importar escolas para o banco de dados")

                if importar:
                    try:
                        conn = conectar()
                        cursor = conn.cursor()
                        total_importadas = 0
                        total_linhas = len(df)
                        log_erros = []


                        for index, row in df.iterrows():
                            try:
                                nome_original = str(row.get("nome_escola", "")).strip()
                                nome_normalizado = nome_original.lower()

                                cnpj = str(row.get("cnpj", "")).strip()
                                cnpj_normalizado = cnpj.replace(".", "").replace("/", "").replace("-", "")

                                estado = str(row.get("estado", "")).strip().upper()

                                # Validações
                                if len(estado) > 2:
                                    msg = f"Linha {index + 2}: estado inválido '{estado}'"
                                    st.warning(f"⚠️ {msg}")
                                    log_erros.append(msg)
                                    continue
                                if len(nome_normalizado) > 255:
                                    msg = f"Linha {index + 2}: nome da escola excede 255 caracteres"
                                    st.warning(f"⚠️ {msg}")
                                    log_erros.append(msg)
                                    continue
                                if len(cnpj_normalizado) > 20:
                                    msg = f"Linha {index + 2}: CNPJ excede 20 caracteres"
                                    st.warning(f"⚠️ {msg}")
                                    log_erros.append(msg)
                                    continue

                                # Inserção
                                cursor.execute("""
                                    INSERT INTO escolas (
                                        nome_escola, telefone, email, cep, rua, bairro, cidade, estado, complemento, numero,
                                        contato_nome, contato_cargo, perfil_pedagogico, origem_lead, responsavel_pedagogico,
                                        escola_paideia, cnpj, diretor_nome, qtd_infantil, qtd_fund1, qtd_fund2, qtd_medio
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    nome_original,
                                    str(row.get("telefone", "")),
                                    str(row.get("email", "")),
                                    str(row.get("cep", "")),
                                    str(row.get("rua", "")),
                                    str(row.get("bairro", "")),
                                    str(row.get("cidade", "")),
                                    estado,
                                    str(row.get("complemento", "")),
                                    str(row.get("numero", "")),
                                    str(row.get("contato_nome", "")),
                                    str(row.get("contato_cargo", "")),
                                    str(row.get("perfil_pedagogico", "")),
                                    str(row.get("origem_lead", "")),
                                    str(row.get("responsavel_pedagogico", "")),
                                    str(row.get("escola_paideia", "")),
                                    cnpj_normalizado,
                                    str(row.get("diretor_nome", "")),
                                    int(float(row["qtd_infantil"])) if str(row["qtd_infantil"]).strip() != "" else 0,
                                    int(float(row["qtd_fund1"])) if str(row["qtd_fund1"]).strip() != "" else 0,
                                    int(float(row["qtd_fund2"])) if str(row["qtd_fund2"]).strip() != "" else 0,
                                    int(float(row["qtd_medio"])) if str(row["qtd_medio"]).strip() != "" else 0
                                ))

                                total_importadas += 1
                                st.info(f"✅ Linha {index + 2}: {nome_original} importada com sucesso.")

                            except Exception as linha_erro:
                                msg = f"❌ Erro na linha {index + 2}: {linha_erro}"
                                st.error(msg)
                                log_erros.append(msg)

                        conn.commit()
                        conn.close()

                        st.success(f"🎯 Total de linhas processadas: {total_linhas}")
                        st.success(f"📥 Total de escolas importadas: {total_importadas}")

                        # Salvar relatório de erros
                        if log_erros:
                            log_path = "/mnt/data/relatorio_erros_importacao.txt"
                            with open(log_path, "w", encoding="utf-8") as f:
                                for linha in log_erros:
                                    f.write(f"{linha}\n")
                            st.download_button("📄 Baixar relatório de erros", data=open(log_path, "rb"), file_name="relatorio_erros_importacao.txt", mime="text/plain")

                    except Exception as e:
                        st.error(f"❌ Erro ao conectar ou importar: {e}")

        except Exception as e:
            st.error(f"❌ Erro ao ler o arquivo: {e}")
