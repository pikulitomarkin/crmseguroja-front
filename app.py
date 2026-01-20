"""
Dashboard CRM com Streamlit - Frontend Isolado
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

# Configuração da página
st.set_page_config(
    page_title="CRM Dashboard - Seguro JA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .lead-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

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

# Header
st.title("📊 CRM Dashboard - Seguro JA")
st.markdown("---")

# Verifica conexão com API
api_status = get_api_health()

if not api_status:
    st.error(f"⚠️ Não foi possível conectar ao backend: {API_URL}")
    st.info("Verifique se o servidor está rodando e a variável API_URL está configurada corretamente.")
    st.stop()

st.success("✅ Conectado ao backend")

# Sidebar
with st.sidebar:
    st.header("⚙️ Filtros")
    
    status_filter = st.selectbox(
        "Status do Lead",
        ["Todos", "novo", "qualificado", "em_negociacao", "convertido", "perdido"]
    )
    
    date_range = st.date_input(
        "Período",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )
    
    st.markdown("---")
    st.markdown("### 📞 Contato")
    st.markdown("**Seguro JA**")
    st.markdown("WhatsApp: (11) 99999-9999")

# Métricas principais
st.header("📈 Métricas Gerais")

stats = get_leads_stats()

if stats:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Leads",
            value=stats.get("total_leads", 0),
            delta=f"+{stats.get('novos_hoje', 0)} hoje"
        )
    
    with col2:
        st.metric(
            label="Qualificados",
            value=stats.get("qualificados", 0),
            delta=f"{stats.get('taxa_qualificacao', 0):.1f}%"
        )
    
    with col3:
        st.metric(
            label="Em Negociação",
            value=stats.get("em_negociacao", 0)
        )
    
    with col4:
        st.metric(
            label="Convertidos",
            value=stats.get("convertidos", 0),
            delta=f"{stats.get('taxa_conversao', 0):.1f}%"
        )
else:
    st.warning("Não foi possível carregar as estatísticas")

st.markdown("---")

# Lista de Leads
st.header("👥 Leads Recentes")

# Aplica filtro de status
status_param = None if status_filter == "Todos" else status_filter
leads = get_leads(status=status_param)

if leads:
    # Tabs por status
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"🆕 Novos ({len([l for l in leads if l.get('status') == 'novo'])})",
        f"✅ Qualificados ({len([l for l in leads if l.get('status') == 'qualificado'])})",
        f"💬 Em Negociação ({len([l for l in leads if l.get('status') == 'em_negociacao'])})",
        f"🎉 Convertidos ({len([l for l in leads if l.get('status') == 'convertido'])})",
        f"❌ Perdidos ({len([l for l in leads if l.get('status') == 'perdido'])})"
    ])
    
    def render_leads(status):
        filtered_leads = [l for l in leads if l.get('status') == status]
        
        if not filtered_leads:
            st.info(f"Nenhum lead com status '{status}'")
            return
        
        for lead in filtered_leads:
            with st.expander(f"📱 {lead.get('name', 'Sem nome')} - {lead.get('whatsapp_number', '')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Nome:** {lead.get('name', 'N/A')}")
                    st.markdown(f"**Telefone:** {lead.get('whatsapp_number', 'N/A')}")
                    st.markdown(f"**Status:** {lead.get('status', 'N/A')}")
                    st.markdown(f"**Score:** {lead.get('qualification_score', 0)}/100")
                    
                    if lead.get('email'):
                        st.markdown(f"**Email:** {lead.get('email')}")
                    
                    if lead.get('qualification_data'):
                        st.markdown("**Dados de Qualificação:**")
                        qual_data = lead.get('qualification_data')
                        if isinstance(qual_data, dict):
                            for key, value in qual_data.items():
                                st.markdown(f"- {key}: {value}")
                
                with col2:
                    created_at = lead.get('created_at', '')
                    if created_at:
                        st.markdown(f"**Criado:** {created_at[:10]}")
                    
                    updated_at = lead.get('updated_at', '')
                    if updated_at:
                        st.markdown(f"**Atualizado:** {updated_at[:10]}")
                
                # Mostrar mensagens
                if st.button(f"Ver Conversas", key=f"msg_{lead.get('id')}"):
                    messages = get_messages(lead.get('id'))
                    if messages:
                        st.markdown("**💬 Histórico de Conversas:**")
                        for msg in messages[-10:]:  # Últimas 10 mensagens
                            sender = "🤖 Bot" if msg.get('sender') == 'bot' else "👤 Cliente"
                            st.markdown(f"{sender}: {msg.get('message', '')}")
                    else:
                        st.info("Nenhuma mensagem ainda")
    
    with tab1:
        render_leads("novo")
    
    with tab2:
        render_leads("qualificado")
    
    with tab3:
        render_leads("em_negociacao")
    
    with tab4:
        render_leads("convertido")
    
    with tab5:
        render_leads("perdido")

else:
    st.warning("Nenhum lead encontrado")

# Footer
st.markdown("---")
st.markdown("### 🔄 Atualização Automática")
if st.button("🔄 Atualizar Dados"):
    st.rerun()

st.markdown("*Dashboard atualizado em: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "*")
