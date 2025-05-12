import streamlit as st
from utils.banners import exibir_banner

def carregar():
    
    # Exibe o banner correspondente à página inicial
    exibir_banner("banner_inicio")
    
    st.markdown("<h2 style='color:#1f538d;'>Bem-vindo ao Cidade Viva Education</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Missão</h3>
        <p>Conduzir pessoas ao deslumbramento a partir de uma educação cristã de excelência.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Visão</h3>
        <p>Ser uma ponte que resgata presentes do passado, educando mentes e corações para a contemplação, a virtude, o serviço e a glória de Deus.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Valores Organizacionais</h3>

        <h4>Eixo Cristão</h4>
        <ul>
            <ul><strong>Piedade:</strong> Relacionamento íntimo e reverente com Deus.</li>
            <ul><strong>Sabedoria:</strong> Discernimento e prudência aplicados na vida.</li>
            <ul><strong>Amor:</strong> Expressar o amor de Cristo em todas as relações.</li>
            <ul><strong>Cosmovisão Cristã:</strong> Visão de mundo moldada pela Palavra de Deus.</li>
        </ul>

        <h4>Eixo Pedagógico</h4>
        <ul>
            <ul><strong>Liberdade:</strong> Formação de indivíduos capazes de agir com responsabilidade.</li>
            <ul><strong>Excelência:</strong> Buscar sempre padrões elevados em todas as atividades.</li>
            <ul><strong>Integralidade:</strong> Educação completa para corpo, mente e espírito.</li>
            <ul><strong>Beleza:</strong> Reconhecimento da beleza como reflexo da criação divina.</li>
            <ul><strong>Tradição:</strong> Preservar e valorizar legados essenciais para a educação.</li>
            <ul><strong>Verdade:</strong> Compromisso com princípios imutáveis e eternos.</li>
        </ul>

        <h4>Eixo de Inovação</h4>
        <ul>
            <ul><strong>Estética:</strong> Desenvolvimento da sensibilidade para o belo.</li>
            <ul><strong>Criatividade:</strong> Estímulo à criação de novas soluções educativas.</li>
            <ul><strong>Regionalidade:</strong> Valorização das raízes e cultura local.</li>
            <ul><strong>Tecnologia:</strong> Uso ético e inteligente de recursos tecnológicos.</li>
            <ul><strong>Experiência:</strong> Aprendizado vivencial e prático.</li>
            <ul><strong>Inovação Criacional:</strong> Renovação com base na criação de Deus.</li>
        </ul>

        <h4>Eixo Organizacional</h4>
        <ul>
            <ul><strong>Transparência:</strong> Clareza e abertura nas ações institucionais.</li>
            <ul><strong>Prudência:</strong> Tomada de decisões cuidadosas e responsáveis.</li>
            <ul><strong>Mordomia:</strong> Gestão responsável dos recursos confiados por Deus.</li>
            <ul><strong>Comprometimento:</strong> Dedicação total à missão e aos valores da organização.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Diferenciais Estratégicos</h3>
        <ul>
            <ul><strong>Beleza do Material:</strong> Design e acabamento gráfico de alto nível.</li>
            <ul><strong>Produções Autorais:</strong> Materiais exclusivos como músicas, poemas e catecismos.</li>
            <ul><strong>Qualidade Gráfica:</strong> Excelência na impressão e materiais didáticos.</li>
            <ul><strong>Padrões Elevados:</strong> Educação acima dos parâmetros da BNCC.</li>
            <ul><strong>Plataforma de Suporte:</strong> Apoio pedagógico, jurídico e administrativo completo.</li>
            <ul><strong>Disciplinas Integradas:</strong> Currículo clássico cristão estruturado desde a infância.</li>
            <ul><strong>Experiência Educacional:</strong> Relacional, visual e formativa.</li>
            <ul><strong>Mentoria:</strong> Acompanhamento pedagógico e jurídico.</li>
            <ul><strong>Parceria com Faculdade:</strong> Vínculo com a Faculdade Internacional Cidade Viva (FICV).</li>
            <ul><strong>Único Currículo:</strong> Material didático unificado para todo o ciclo escolar.</li>
            <ul><strong>Sem fins lucrativos:</strong> Todos os recursos revertidos para a missão educacional.</li>
            <ul><strong>Vínculo afetivo:</strong> Relações de confiança e proximidade com as escolas.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Cultura Organizacional</h3>
        <ul>
            <ul><strong>Identidade Cristã:</strong> Clareza nos princípios bíblicos como alicerce institucional.</li>
            <ul><strong>Produtividade:</strong> Entregas eficientes e responsáveis.</li>
            <ul><strong>Flexibilidade:</strong> Capacidade de adaptação em cenários diversos.</li>
            <ul><strong>Horizontalidade:</strong> Comunicação aberta e participação colaborativa.</li>
            <ul><strong>Colaboração:</strong> Trabalho em equipe contínuo e propositivo.</li>
            <ul><strong>Excelência:</strong> Busca constante por qualidade elevada.</li>
            <ul><strong>Liderança Inspiradora:</strong> Líderes que conduzem pelo exemplo e pelo serviço.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
