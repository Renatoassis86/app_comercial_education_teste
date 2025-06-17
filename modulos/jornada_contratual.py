import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.banners import exibir_banner
from utils.conexao import conectar


def carregar():
    exibir_banner("banner_acompanhamento")
    st.markdown("<h2 style='color:#1f538d;'>Gestão de Contratos e Fechamentos</h2>", unsafe_allow_html=True)

    conn = conectar()
    escolas_df = pd.read_sql("SELECT id, nome_escola FROM escolas ORDER BY nome_escola", conn)
    escola_selecionada = st.selectbox("Selecione uma escola", [""] + escolas_df['nome_escola'].tolist())

    if escola_selecionada:
        id_escola = int(escolas_df[escolas_df['nome_escola'] == escola_selecionada]['id'].values[0])
        dados_existentes = pd.read_sql(f"SELECT * FROM contratos WHERE id_escola = {id_escola}", conn)

        st.subheader("📄 Status e Encaminhamentos")

        col1, col2, col3 = st.columns(3)

        status_formulario = col1.selectbox("Formulário enviado?", ["", "Sim", "Não"],
                                           index=(["", "Sim", "Não"].index(dados_existentes['status_formulario'].iloc[0])
                                                  if not dados_existentes.empty else 0))

        formulario_recebido = col2.selectbox("Formulário recebido?", ["", "Sim", "Não"],
                                             index=(["", "Sim", "Não"].index(dados_existentes['formulario_recebido'].iloc[0])
                                                    if not dados_existentes.empty else 0))

        status_minuta = col3.selectbox("Minuta enviada?", ["", "Sim", "Não"],
                                       index=(["", "Sim", "Não"].index(dados_existentes['status_minuta'].iloc[0])
                                              if not dados_existentes.empty else 0))

        retorno_minuta = st.selectbox("Retorno sobre minuta?", ["", "Sim", "Não"],
                                      index=(["", "Sim", "Não"].index(dados_existentes['retorno_minuta'].iloc[0])
                                             if not dados_existentes.empty else 0))

        observacao_minuta = st.text_area(
            "🗒️ Observações ou principais pontos levantados pela escola sobre a minuta:",
            value=(dados_existentes['observacao_minuta'].iloc[0] if not dados_existentes.empty else ""))

        atualizar_minuta = st.selectbox("Atualização da minuta?", ["", "Sim", "Não"],
                                        index=(["", "Sim", "Não"].index(dados_existentes['atualizar_minuta'].iloc[0])
                                               if not dados_existentes.empty else 0))

        contrato_enviado = st.selectbox("Contrato enviado para assinatura?", ["", "Sim", "Não"],
                                        index=(["", "Sim", "Não"].index(dados_existentes['contrato_enviado'].iloc[0])
                                               if not dados_existentes.empty else 0))

        contrato_assinado = st.selectbox("Contrato assinado?", ["", "Sim", "Não"],
                                         index=(["", "Sim", "Não"].index(dados_existentes['contrato_assinado'].iloc[0])
                                                if not dados_existentes.empty else 0))

        contrato_arquivado = st.selectbox("Contrato arquivado?", ["", "Sim", "Não"],
                                          index=(["", "Sim", "Não"].index(dados_existentes['contrato_arquivado'].iloc[0])
                                                 if not dados_existentes.empty else 0))

        registros = pd.read_sql(f"""
            SELECT encaminhamento 
            FROM registros 
            WHERE id_escola = {id_escola} 
            ORDER BY data_contato DESC, hora_contato DESC LIMIT 1
        """, conn)
        encaminhamento_default = registros.iloc[0]['encaminhamento'] if not registros.empty else ""

        encaminhamento_final = st.text_input("Encaminhamento final",
                                             value=(dados_existentes['encaminhamento_final'].iloc[0]
                                                    if not dados_existentes.empty else encaminhamento_default))

        st.subheader("Detalhes dos Alunos e Valores")

        col1, col2 = st.columns(2)

        with col1:
            infantil2_qtd = st.number_input("Qtd Infantil 2", min_value=0,
                                             value=int(dados_existentes['infantil2_qtd'].iloc[0]) if not dados_existentes.empty else 0)
            infantil3_qtd = st.number_input("Qtd Infantil 3", min_value=0,
                                             value=int(dados_existentes['infantil3_qtd'].iloc[0]) if not dados_existentes.empty else 0)
            infantil4_qtd = st.number_input("Qtd Infantil 4", min_value=0,
                                             value=int(dados_existentes['infantil4_qtd'].iloc[0]) if not dados_existentes.empty else 0)
            infantil5_qtd = st.number_input("Qtd Infantil 5", min_value=0,
                                             value=int(dados_existentes['infantil5_qtd'].iloc[0]) if not dados_existentes.empty else 0)
            fund1_qtd = st.number_input("Qtd 1º Ano Fund I", min_value=0,
                                        value=int(dados_existentes['fund1_qtd'].iloc[0]) if not dados_existentes.empty else 0)

        with col2:
            valor_inf2 = st.number_input("Valor Infantil 2", min_value=0.0, format="%.2f",
                                         value=float(dados_existentes['valor_inf2'].iloc[0]) if not dados_existentes.empty else 0.0)
            valor_inf3 = st.number_input("Valor Infantil 3", min_value=0.0, format="%.2f",
                                         value=float(dados_existentes['valor_inf3'].iloc[0]) if not dados_existentes.empty else 0.0)
            valor_inf4 = st.number_input("Valor Infantil 4", min_value=0.0, format="%.2f",
                                         value=float(dados_existentes['valor_inf4'].iloc[0]) if not dados_existentes.empty else 0.0)
            valor_inf5 = st.number_input("Valor Infantil 5", min_value=0.0, format="%.2f",
                                         value=float(dados_existentes['valor_inf5'].iloc[0]) if not dados_existentes.empty else 0.0)
            valor_fund1 = st.number_input("Valor 1º Ano Fund I", min_value=0.0, format="%.2f",
                                          value=float(dados_existentes['valor_fund1'].iloc[0]) if not dados_existentes.empty else 0.0)

        tempo_contrato_anos = st.number_input("Tempo de contrato (anos)", min_value=1,
                                               value=(dados_existentes['tempo_contrato'].iloc[0] // 12) if not dados_existentes.empty else 1)
        tempo_contrato = tempo_contrato_anos * 12

        total = (
            infantil2_qtd * valor_inf2 +
            infantil3_qtd * valor_inf3 +
            infantil4_qtd * valor_inf4 +
            infantil5_qtd * valor_inf5 +
            fund1_qtd * valor_fund1
        )

        st.markdown(f"**💰 Valor Total Estimado para 2026:** R$ {total:,.2f}")

        if st.button("💾 Salvar Contrato"):
            try:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM contratos WHERE id_escola = %s", (id_escola,))

                cursor.execute("""
                    INSERT INTO contratos (
                        id_escola, status_formulario, formulario_recebido, status_minuta, retorno_minuta,
                        atualizar_minuta, contrato_enviado, contrato_assinado, contrato_arquivado,
                        observacao_minuta, encaminhamento_final, tempo_contrato, valor_total,
                        infantil2_qtd, infantil3_qtd, infantil4_qtd, infantil5_qtd, fund1_qtd,
                        valor_inf2, valor_inf3, valor_inf4, valor_inf5, valor_fund1
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    id_escola, status_formulario, formulario_recebido, status_minuta, retorno_minuta,
                    atualizar_minuta, contrato_enviado, contrato_assinado, contrato_arquivado,
                    observacao_minuta, encaminhamento_final, tempo_contrato, total,
                    infantil2_qtd, infantil3_qtd, infantil4_qtd, infantil5_qtd, fund1_qtd,
                    valor_inf2, valor_inf3, valor_inf4, valor_inf5, valor_fund1
                ))

                conn.commit()
                st.success("✅ Dados do contrato salvos com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

    st.subheader("Acompanhamento Geral")
    try:
        df = pd.read_sql("""
            SELECT c.*, e.nome_escola, e.estado
            FROM contratos c
            JOIN escolas e ON c.id_escola = e.id
            WHERE c.status_formulario = 'Sim'
        """, conn)

        if df.empty:
            st.info("Nenhum contrato encontrado com formulário confirmado.")
        else:
            df["total_alunos"] = (
                df['infantil2_qtd'] + df['infantil3_qtd'] + df['infantil4_qtd'] +
                df['infantil5_qtd'] + df['fund1_qtd']
            )

            st.dataframe(df[[
                'nome_escola', 'estado', 'encaminhamento_final',
                'status_formulario', 'formulario_recebido', 'status_minuta',
                'retorno_minuta', 'observacao_minuta',
                'contrato_assinado', 'total_alunos', 'valor_total'
            ]])

            total_alunos = df["total_alunos"].sum()
            total_receita = df["valor_total"].sum()

            st.markdown("### 🎯 Acompanhamento de Metas")

            # === Gráfico de Alunos ===
            meta_alunos = 3000
            percentual_alunos = (total_alunos / meta_alunos) * 100

            fig1, ax1 = plt.subplots(figsize=(6, 0.8))
            ax1.barh(['Alunos'], [meta_alunos], color='#e9ecef', height=0.4)
            ax1.barh(['Alunos'], [min(total_alunos, meta_alunos)], color='#28a745', height=0.4)
            ax1.text(meta_alunos, 0, "Meta: 3000", va='center', ha='right', fontsize=9, color='#6c757d')
            ax1.text(total_alunos + 50, 0, f"{total_alunos} alunos", va='center', ha='left', fontsize=9, color='#212529')
            ax1.text(meta_alunos * 0.5, 0, f"{percentual_alunos:.1f}%", va='center', ha='center',
                     fontsize=10, color='#212529', weight='bold')
            ax1.set_xlim(0, meta_alunos * 1.1)
            ax1.axis('off')
            st.pyplot(fig1)

            # === Gráfico de Receita ===
            meta_revenue = 3000000
            percentual_receita = (total_receita / meta_revenue) * 100

            fig2, ax2 = plt.subplots(figsize=(6, 0.8))
            ax2.barh(['Receita'], [meta_revenue], color='#e9ecef', height=0.4)
            ax2.barh(['Receita'], [min(total_receita, meta_revenue)], color='#007bff', height=0.4)
            ax2.text(meta_revenue, 0, "Meta: R$ 3M", va='center', ha='right', fontsize=9, color='#6c757d')
            ax2.text(total_receita + 50000, 0, f"R$ {total_receita:,.2f}", va='center', ha='left', fontsize=9,
                     color='#212529')
            ax2.text(meta_revenue * 0.5, 0, f"{percentual_receita:.1f}%", va='center', ha='center',
                     fontsize=10, color='#212529', weight='bold')
            ax2.set_xlim(0, meta_revenue * 1.1)
            ax2.axis('off')
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"Erro ao carregar dados de acompanhamento: {e}")
