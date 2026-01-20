"""
Dashboard CRM Seguro JA - Interface Profissional
Estética inspirada em Evolution API
"""
import os
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Seguro JA | CRM Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS CUSTOMIZADO ====================
st.markdown("""
<style>
    /* Importa fonte Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações globais */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Remove padding padrão do Streamlit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Esconde elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background principal */
    .main {
        background-color: #f8fafc;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #334155 0%, #1e293b 50%, #0f172a 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* Inputs na sidebar */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #475569 !important;
        color: white !important;
        border: 1px solid #64748b !important;
    }
    
    [data-testid="stSidebar"] .stDateInput > div > div {
        background-color: #475569 !important;
        border: 1px solid #64748b !important;
    }
    
    [data-testid="stSidebar"] .stDateInput input {
        color: white !important;
        background-color: #475569 !important;
    }
    
    [data-testid="stSidebar"] .stDateInput button {
        color: white !important;
    }
    
    [data-testid="stSidebar"] input {
        color: white !important;
        background-color: #475569 !important;
    }
    
    /* Calendar popup */
    .stDateInput [data-baseweb="calendar"] {
        background-color: #334155 !important;
    }
    
    .stDateInput [data-baseweb="calendar"] * {
        color: white !important;
    }
    
    /* Botão na sidebar */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
    }
    
    /* Cards principais */
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .metric-delta.positive {
        color: #10b981;
    }
    
    .metric-delta.negative {
        color: #ef4444;
    }
    
    /* Lead Cards */
    .lead-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .lead-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        border-color: #3b82f6;
    }
    
    .lead-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .lead-name {
        font-size: 1rem;
        font-weight: 600;
        color: #0f172a;
    }
    
    .lead-phone {
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    .lead-score {
        font-size: 0.875rem;
        font-weight: 600;
        color: #3b82f6;
    }
    
    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-novo {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .badge-qualificado {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-em_negociacao {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-convertido {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-perdido {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .badge-aguardando {
        background: #fef3c7;
        color: #92400e;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        height: 600px;
        overflow-y: auto;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .chat-message {
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .chat-message.user {
        align-items: flex-end;
    }
    
    .chat-message.bot {
        align-items: flex-start;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 0.875rem 1.125rem;
        border-radius: 16px;
        font-size: 0.9375rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .message-bubble.user {
        background: #3b82f6;
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .message-bubble.bot {
        background: #f1f5f9;
        color: #0f172a;
        border-bottom-left-radius: 4px;
    }
    
    .message-time {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }
    
    /* Header */
    .dashboard-header {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .dashboard-title {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .dashboard-subtitle {
        font-size: 0.9375rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    /* Tabela customizada */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Botões */
    .stButton>button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background: #2563eb;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Tabs customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
    }
    
    /* Inputs */
    .stSelectbox, .stDateInput {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ==================== FUNÇÕES DE API ====================

def get_api_health():
    """Verifica se a API está online"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_leads_stats():
    """Obtém estatísticas de leads via API"""
    try:
        response = requests.get(f"{API_URL}/api/leads/stats", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_leads(status=None, limit=50):
    """Obtém lista de leads via API"""
    try:
        params = {"limit": limit}
        if status:
            params["status"] = status
        response = requests.get(f"{API_URL}/api/leads", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_messages(lead_id):
    """Obtém mensagens de um lead via API"""
    try:
        response = requests.get(f"{API_URL}/api/leads/{lead_id}/messages", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

# ==================== FUNÇÕES DE RENDERIZAÇÃO ====================

def render_status_badge(status, aguardando_atendimento=False):
    """Renderiza badge de status"""
    if aguardando_atendimento:
        return '<span class="badge badge-aguardando">⏳ AGUARDANDO ATENDIMENTO</span>'
    
    status_map = {
        "novo": "Novo",
        "qualificado": "Qualificado",
        "em_negociacao": "Em Negociação",
        "convertido": "Convertido",
        "perdido": "Perdido"
    }
    label = status_map.get(status, status)
    return f'<span class="badge badge-{status}">{label}</span>'

def render_metric_card(label, value, delta=None, delta_positive=True):
    """Renderiza card de métrica"""
    delta_html = ""
    if delta:
        delta_class = "positive" if delta_positive else "negative"
        delta_symbol = "↑" if delta_positive else "↓"
        delta_html = f'<div class="metric-delta {delta_class}">{delta_symbol} {delta}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def render_chat_message(message, sender, timestamp=None):
    """Renderiza mensagem de chat"""
    message_class = "user" if sender == "user" else "bot"
    time_str = ""
    if timestamp:
        time_str = f'<div class="message-time">{timestamp}</div>'
    
    return f"""
    <div class="chat-message {message_class}">
        <div class="message-bubble {message_class}">{message}</div>
        {time_str}
    </div>
    """

def render_lead_card(lead, index):
    """Renderiza card de lead"""
    # Verifica se está aguardando atendimento humano
    aguardando = lead.get('status') == 'qualificado'
    status_badge = render_status_badge(lead.get('status', 'novo'), aguardando)
    
    # Extrai informações do lead
    name = lead.get('name', 'Aguardando qualificação')
    phone = lead.get('whatsapp_number', 'N/A')
    score = lead.get('qualification_score', 0) or 0
    email = lead.get('email', '')
    
    # Adiciona email se existir
    email_line = f'<div class="lead-phone">📧 {email}</div>' if email else ''
    
    return f"""
    <div class="lead-card" id="lead-{index}">
        <div class="lead-header">
            <div>
                <div class="lead-name">👤 {name}</div>
                <div class="lead-phone">📱 {phone}</div>
                {email_line}
            </div>
            <div>
                <div class="lead-score">⭐ {score}/100</div>
            </div>
        </div>
        <div style="margin-top: 0.75rem;">
            {status_badge}
        </div>
    </div>
    """

# ==================== INTERFACE PRINCIPAL ====================

# Header principal
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">🛡️ Seguro JA | CRM Dashboard</div>
    <div class="dashboard-subtitle">Sistema Inteligente de Gestão de Leads com IA</div>
</div>
""", unsafe_allow_html=True)

# Verifica conexão com API
api_status = get_api_health()

if not api_status:
    st.error(f"⚠️ **Não foi possível conectar ao backend**")
    st.info(f"Verifique se o servidor está rodando em: `{API_URL}`")
    
    # Mock data para demonstração
    st.warning("🔄 Usando dados de demonstração")
    
    stats = {
        "total_leads": 127,
        "novos_hoje": 8,
        "qualificados": 45,
        "em_negociacao": 23,
        "convertidos": 34,
        "taxa_qualificacao": 35.4,
        "taxa_conversao": 26.8
    }
    
    leads = [
        {
            "id": 1,
            "name": "João Silva",
            "whatsapp_number": "11999887766",
            "status": "novo",
            "qualification_score": 75,
            "created_at": "2026-01-19T10:30:00"
        },
        {
            "id": 2,
            "name": "Maria Santos",
            "whatsapp_number": "11988776655",
            "status": "qualificado",
            "qualification_score": 92,
            "created_at": "2026-01-19T09:15:00"
        },
        {
            "id": 3,
            "name": "Carlos Oliveira",
            "whatsapp_number": "11977665544",
            "status": "em_negociacao",
            "qualification_score": 88,
            "created_at": "2026-01-18T16:45:00"
        }
    ]
else:
    st.success("✅ **Conectado ao backend**")
    stats = get_leads_stats()
    leads = get_leads()

# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    
    status_filter = st.selectbox(
        "Status do Lead",
        ["Todos", "novo", "qualificado", "em_negociacao", "convertido", "perdido"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    date_range = st.date_input(
        "Período de Análise",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📞 Suporte")
    st.markdown("**Seguro JA**")
    st.markdown("📧 contato@seguroja.com.br")
    st.markdown("📱 (11) 99999-9999")
    st.markdown("⏰ Seg-Sex: 8h às 18h")
    
    st.markdown("---")
    if st.button("🔄 Atualizar Dados"):
        st.rerun()

# ==================== MÉTRICAS PRINCIPAIS ====================

if stats:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            render_metric_card(
                "Total de Leads",
                stats.get("total_leads", 0),
                f"+{stats.get('novos_hoje', 0)} hoje",
                True
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            render_metric_card(
                "Qualificados",
                stats.get("qualificados", 0),
                f"{stats.get('taxa_qualificacao', 0):.1f}%",
                True
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            render_metric_card(
                "Em Negociação",
                stats.get("em_negociacao", 0)
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            render_metric_card(
                "Convertidos",
                stats.get("convertidos", 0),
                f"{stats.get('taxa_conversao', 0):.1f}%",
                True
            ),
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ==================== ÁREA DE LEADS E CHAT ====================

col_leads, col_chat = st.columns([1, 1])

with col_leads:
    st.markdown("### 👥 Leads Capturados")
    
    # Filtra leads por status
    if status_filter != "Todos":
        filtered_leads = [l for l in leads if l.get('status') == status_filter]
    else:
        filtered_leads = leads
    
    # Renderiza leads
    if filtered_leads:
        for idx, lead in enumerate(filtered_leads[:10]):  # Mostra até 10 leads
            # Extrai dados
            name = lead.get('name', 'Aguardando qualificação')
            phone = lead.get('whatsapp_number', 'N/A')
            email = lead.get('email', '')
            score = lead.get('qualification_score', 0) or 0
            status = lead.get('status', 'novo')
            aguardando = status == 'qualificado'
            
            # Container com borda
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**👤 {name}**")
                    st.caption(f"📱 {phone}")
                    if email:
                        st.caption(f"📧 {email}")
                
                with col2:
                    st.markdown(f"**⭐ {score}**/100")
                
                # Badge de status
                if aguardando:
                    st.warning("⏳ AGUARDANDO ATENDIMENTO")
                else:
                    status_labels = {
                        "novo": ("🆕 NOVO", "info"),
                        "qualificado": ("✅ QUALIFICADO", "success"),
                        "em_negociacao": ("💬 EM NEGOCIAÇÃO", "warning"),
                        "convertido": ("🎯 CONVERTIDO", "success"),
                        "perdido": ("❌ PERDIDO", "error")
                    }
                    label, badge_type = status_labels.get(status, ("DESCONHECIDO", "info"))
                    if badge_type == "info":
                        st.info(label)
                    elif badge_type == "success":
                        st.success(label)
                    elif badge_type == "warning":
                        st.warning(label)
                    elif badge_type == "error":
                        st.error(label)
                
                # Botão para seleção
                if st.button("📋 Ver Conversas", key=f"btn_lead_{idx}", use_container_width=True):
                    st.session_state.selected_lead = lead
                    st.rerun()
                
                st.markdown("---")  # Separador
    else:
        st.info("Nenhum lead encontrado com os filtros aplicados")

with col_chat:
    st.markdown("### 💬 Histórico de Conversas")
    
    if 'selected_lead' in st.session_state:
        lead = st.session_state.selected_lead
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <strong style="font-size: 1.125rem; color: #0f172a;">{lead.get('name', 'Lead')}</strong><br>
            <span style="color: #64748b; font-size: 0.875rem;">{lead.get('whatsapp_number', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Busca mensagens
        messages = get_messages(lead.get('id')) if api_status else [
            {"sender": "user", "message": "Olá, gostaria de informações sobre seguro auto", "created_at": "2026-01-19T10:30:00"},
            {"sender": "bot", "message": "Olá! Fico feliz em ajudar com informações sobre seguro auto. Para oferecer a melhor cotação, preciso de algumas informações. Qual é a marca e modelo do seu veículo?", "created_at": "2026-01-19T10:30:15"},
            {"sender": "user", "message": "É um Honda Civic 2022", "created_at": "2026-01-19T10:31:00"},
            {"sender": "bot", "message": "Excelente! O Honda Civic é um ótimo veículo. Você é o proprietário do veículo?", "created_at": "2026-01-19T10:31:10"}
        ]
        
        # Container de chat
        chat_html = '<div class="chat-container">'
        
        if messages:
            for msg in messages:
                sender_type = "user" if msg.get('sender') == 'user' else "bot"
                timestamp = msg.get('created_at', '')[:16] if msg.get('created_at') else ''
                chat_html += render_chat_message(
                    msg.get('message', ''),
                    sender_type,
                    timestamp
                )
        else:
            chat_html += '<div style="text-align: center; color: #94a3b8; padding: 2rem;">Nenhuma mensagem ainda</div>'
        
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="chat-container">
            <div style="text-align: center; color: #94a3b8; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <div style="font-size: 1.125rem; font-weight: 600;">Selecione um lead</div>
                <div style="font-size: 0.875rem; margin-top: 0.5rem;">Clique em um lead à esquerda para ver o histórico de conversas</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== FOOTER ====================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: #94a3b8; font-size: 0.875rem; padding: 2rem 0;">
    <strong>Seguro JA CRM</strong> • Powered by Evolution API + OpenAI • Atualizado em {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
</div>
""", unsafe_allow_html=True)
