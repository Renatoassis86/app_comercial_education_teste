import streamlit as st
import pandas as pd
import psycopg2.extras
from datetime import datetime
from utils.banners import exibir_banner
from utils.conexao import conectar
from utils.helpers import calcular_potencial_financeiro, calcular_probabilidade, calcular_classificacao


def carregar():
    exibir_banner("banner_registro")
    st.markdown("<h2 style='color:#1f538d;'>Registro de Relacionamento</h2>", unsafe_allow_html=True)

    # === Carregar Escolas ===
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_escola FROM escolas ORDER BY nome_escola")
    escolas = cursor.fetchall()
    conn.close()

    escolas_dict = {nome: id_ for id_, nome in escolas}

    st.markdown("### Dados da Escola")
    nome_escola = st.selectbox("Selecione a escola", [""] + list(escolas_dict.keys()))

    if nome_escola:
        st.markdown("### Dados do Registro")
        data_contato = st.date_input("Data do contato", value=datetime.now().date())
        hora_contato = datetime.now().time()  # Hora automática, não precisa ser preenchida manualmente

        resumo = st.text_area("Resumo do Contato (Resumo da conversa e pontos discutidos)")

        meio = st.selectbox("Meio do contato", ["", "Presencial", "WhatsApp", "E-mail", "Telefone", "Videoconferência"])
        responsavel = st.text_input("Responsável pelo contato")
        contato = st.text_input("Nome do contato da escola")
        cargo = st.selectbox("Cargo do contato", ["", "Mantenedor", "Gestor", "Diretor", "Coordenador", "Professor", "Secretário(a)", "Outro"])

        st.markdown("### Diagnóstico de Interesse")
        interesse = st.selectbox("Interesse (Nível de interesse percebido)", ["", "Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"])

        prontidao = st.selectbox("Prontidão (Fase da negociação)", [
            "", "Negociação Parada", "Nova Reunião Necessária", "Esperando Retorno", 
            "Apresentação em Andamento", "Contrato Enviado", "Atualizar Contrato", "Contrato Assinado"
        ])

        abertura = st.selectbox("Abertura para Proposta (Disposição para avançar)", ["", "Nenhuma", "Baixa", "Média", "Alta"])

        encaminhamentos = st.multiselect("Encaminhamento Atual (Próximo passo previsto)", [
            "Agendamento de Reunião", "Apresentação Currículo", "Envio de Material", "Nova Visita", 
            "Contato Futuro", "Elaboração de Contrato", "Contrato Enviado", "Contrato Assinado"
        ])

        st.markdown("### Informações Quantitativas")
        infantil = st.number_input("Qtd Infantil", min_value=0, step=1)
        fund1 = st.number_input("Qtd Fund1", min_value=0, step=1)
        fund2 = st.number_input("Qtd Fund2", min_value=0, step=1)
        medio = st.number_input("Qtd Médio", min_value=0, step=1)

        # === Calcular Métricas ===
        if st.button("🔍 Gerar Métricas"):
            potencial = calcular_potencial_financeiro(infantil, fund1, fund2, medio)
            probabilidade = calcular_probabilidade(interesse, prontidao, abertura, encaminhamentos)
            classificacao = calcular_classificacao(probabilidade, potencial)

            st.success(f"Potencial Financeiro: R$ {potencial:,.2f}")
            st.success(f"Probabilidade de Fechamento: {probabilidade}%")
            st.success(f"Classificação do Lead: {classificacao}")

        # === Salvar no Banco ===
        if st.button("💾 Salvar Registro"):
            try:
                potencial = calcular_potencial_financeiro(infantil, fund1, fund2, medio)
                probabilidade = calcular_probabilidade(interesse, prontidao, abertura, encaminhamentos)
                classificacao = calcular_classificacao(probabilidade, potencial)

                conn = conectar()
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # Verificar se já existe registro idêntico
                cursor.execute("""
                    SELECT COUNT(*) FROM registros 
                    WHERE id_escola = %s AND data_contato = %s AND hora_contato = %s AND resumo = %s
                """, (escolas_dict.get(nome_escola), data_contato, hora_contato, resumo))
                existe = cursor.fetchone()[0]

                if existe > 0:
                    st.warning("⚠️ Registro idêntico já existe. Altere alguma informação para salvar.")
                else:
                    cursor.execute("""
                        INSERT INTO registros (
                            id_escola, data_contato, hora_contato, resumo, meio_contato,
                            interesse, prontidao, abertura, encaminhamento,
                            responsavel, contato, cargo, qtd_infantil, qtd_fund1,
                            qtd_fund2, qtd_medio, potencial_financeiro,
                            classificacao_lead, probabilidade
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        escolas_dict.get(nome_escola),
                        data_contato,
                        hora_contato,
                        resumo,
                        meio,
                        interesse,
                        prontidao,
                        abertura,
                        ", ".join(encaminhamentos),
                        responsavel,
                        contato,
                        cargo,
                        infantil,
                        fund1,
                        fund2,
                        medio,
                        potencial,
                        classificacao,
                        probabilidade
                    ))
                    conn.commit()
                    conn.close()
                    st.success("✅ Registro salvo com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar no banco: {e}")

        # === Excluir Registro ===
        st.markdown("---")
        st.markdown("## Excluir Registro de Relacionamento")

        try:
            conn = conectar()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("""
                SELECT r.id, e.nome_escola, r.data_contato, r.hora_contato, r.resumo 
                FROM registros r
                JOIN escolas e ON r.id_escola = e.id
                WHERE r.id_escola = %s
                ORDER BY r.data_contato, r.hora_contato
            """, (escolas_dict.get(nome_escola),))
            registros = cursor.fetchall()
            conn.close()

            registros_dict = {
                f"{r['id']} - {r['data_contato'].strftime('%d/%m/%Y')} {r['hora_contato']} - {r['resumo'][:60]}": r['id']
                for r in registros
            }

            registro_selecionado = st.selectbox("Escolha o registro para excluir", [""] + list(registros_dict.keys()))

            if registro_selecionado:
                if st.button("❌ Excluir Registro"):
                    try:
                        conn = conectar()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM registros WHERE id = %s", (registros_dict[registro_selecionado],))
                        conn.commit()
                        conn.close()
                        st.success("Registro excluído com sucesso.")
                    except Exception as e:
                        st.error(f"Erro ao excluir: {e}")
        except Exception as e:
            st.error(f"Erro ao carregar registros para exclusão: {e}")
