import streamlit as st

def aplicar_estilo():
    st.markdown(
        '''
        <style>
            html, body, .stApp {
                background-color: #f5f7fa;
                color: #2c3e50;
                font-family: 'Segoe UI', sans-serif;
            }

            header[data-testid="stHeader"], footer {
                display: none;
            }
            input, textarea, select {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            

            .block-container {
                padding-top: 1rem !important;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 20px;
                padding-left: 20px;
                justify-content: center;
                border-bottom: 2px solid #007bff;
            }

            .stTabs [data-baseweb="tab"] {
                font-size: 22px;
                font-weight: 600;
                padding: 10px 20px;
                color: #2c3e50;
                border-bottom: none !important;
            }

            .stTabs [aria-selected="true"] {
                border-bottom: 3px solid #007bff !important;
                color: #007bff !important;
            }

            .caixa-branca {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }

            .caixa-branca h3 {
                color: #007bff;
            }

            .css-1aumxhk, .stButton button {
                padding: 0.25rem 1rem;
                font-size: 0.9rem;
                border-radius: 8px !important;
            }

            .stButton > button {
                height: auto !important;
                width: auto !important;
            }

            img[alt="Cidade Viva Education"] {
                width: 100%;
                max-width: 100%;
                height: auto;
                max-height: 200px;
                object-fit: cover;
                object-position: center;
            }

            .jornada-card {
                background-color: #ffffff;
                border-left: 5px solid #007bff;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                font-size: 16px;
                color: #2c3e50;
                transition: all 0.3s ease;
            }

            .jornada-card:hover {
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
                transform: translateY(-2px);
            }

            .card-jornada strong {
                color: #0056b3;
                font-weight: 600;
            }

            .footer-custom {
                text-align: center;
                padding: 10px;
                font-size: 13px;
                color: #777;
                border-top: 1px solid #ddd;
                margin-top: 30px;
            }

            body {
                background-color: #f4f4f4;
                font-family: 'Segoe UI', sans-serif;
            }

            .caixa-branca {
                background-color: #ffffff;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            }

            .card-destaque {
                background-color: #e8f0fe;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                font-size: 16px;
                line-height: 1.6;
            }

            .metricas-secao {
                font-size: 1.2em;
                font-weight: bold;
                color: #3366cc;
                margin-top: 25px;
                margin-bottom: 10px;
            }

            .titulo-secao {
                font-size: 22px;
                font-weight: bold;
                color: #1a73e8;
                margin-top: 30px;
            }

            .titulo-kpi {
                font-size: 18px;
                font-weight: 600;
                color: #333333;
                margin-top: 15px;
            }

            .rodape {
                margin-top: 50px;
                text-align: center;
                font-size: 12px;
                color: #999999;
            }

            /* Unificar fonte de todos os componentes */
            .stTextInput, .stNumberInput, .stSelectbox, .stMetric, .stDataFrame, .stMarkdown, .css-1aumxhk, .css-1offfwp, .css-1v0mbdj, .css-1dp5vir, .css-10trblm {
                font-family: 'Segoe UI', sans-serif !important;
            }

            /* === Banners === */
            img.banner {
                width: 100%;
                height: auto;
                max-height: 200px;
                object-fit: contain;
                border-radius: 10px;
                margin-bottom: 1rem;
            }

            /* === Cards / Caixas === */
            .caixa-branca {
                background-color: #ffffff;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                margin-bottom: 1.5rem;
                font-size: 16px;
                line-height: 1.5;
            }

            /* === Títulos === */
            h3, h4 {
                color: #004085;
                margin-top: 1rem;
            }

            /* === Métricas do Dashboard === */
            .metricas-dashboard {
                font-size: 18px;
                font-weight: bold;
                color: #1b1e21;
                margin-bottom: 0.75rem;
            }

            /* === Estilo da Jornada === */
            .jornada-card {
                background-color: #e9f5ff;
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                font-size: 15px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            }
            /* === Footer (caso necessário) === */
            footer {
                text-align: center;
                font-size: 14px;
                color: #6c757d;
                margin-top: 2rem;
                padding: 1rem;
            }
            canvas {
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            }
            /* Corrige aparência do selectbox do Streamlit */
            div[role="combobox"] {
                background-color: #ffffff !important;
                color: #2c3e50 !important;
                border: 1px solid #ccc !important;
                border-radius: 5px !important;
                padding: 0.375rem 0.75rem !important;
            }
            }
            input:focus, textarea:focus, select:focus {
                outline: none !important;
                border-color: #007bff !important;
                box-shadow: 0 0 4px rgba(0,123,255,0.25) !important;
            }
            /* === Responsividade === */
            @media only screen and (max-width: 768px) {
                .stTabs [data-baseweb="tab"] {
                    font-size: 16px;
                    padding: 8px 10px;
                }

                .caixa-branca {
                    padding: 1rem;
                    font-size: 15px;
                }

                .metricas-secao,
                .titulo-secao,
                .titulo-kpi {
                    font-size: 90%;
                }

                .stButton button {
                    font-size: 14px;
                    padding: 6px 10px;
                }

                img.banner,
                img[alt="Cidade Viva Education"] {
                    max-width: 100%;
                    height: auto;
                }

                .footer-custom {
                    font-size: 12px;
                }
            }

            @media only screen and (max-width: 480px) {
                .stTabs [data-baseweb="tab"] {
                    font-size: 14px;
                    padding: 6px 8px;
                }

                .footer-custom {
                    font-size: 11px;
                    padding: 5px;
                }
            }

        </style>
        ''',
        unsafe_allow_html=True
    )
