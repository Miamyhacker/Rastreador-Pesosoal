import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Segurança Ativa", layout="centered")

st.markdown("""
<style>
body { background:#0b0f14; color:white; font-family:Arial; }
.box { max-width:420px; margin:auto; text-align:center; }
.circle {
    width:180px; height:180px; border-radius:50%;
    border:4px solid #2ecc71;
    display:flex; align-items:center; justify-content:center;
    font-size:48px; margin:auto;
}
.btn {
    width:100%; padding:14px; font-size:18px;
    border-radius:12px; border:none;
    background:#1f2937; color:white;
}
.card {
    background:#1f2937;
    padding:20px;
    border-radius:16px;
    margin-top:20px;
    text-align:left;
}
</style>
""", unsafe_allow_html=True)

components.html("""
<div class="box">
    <h2>Verificar segurança</h2>

    <div class="circle" id="pct">4%</div>

    <p>✅ Ambiente de pagamentos<br>
       ✅ Privacidade e segurança<br>
       ✅ Vírus</p>

    <button class="btn" onclick="getLocation()">● ATIVAR PROTEÇÃO</button>

    <div id="result"></div>
</div>

<script>
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            let p = document.getElementById("pct");
            let i = 4;
            let timer = setInterval(()=>{
                i+=6; p.innerText=i+"%";
                if(i>=100) clearInterval(timer);
            },80);

            document.getElementById("result").innerHTML =
            "<div class='card'><b>Proteção ativada ✅</b><br><br>"
            + "Latitude: "+pos.coords.latitude+"<br>"
            + "Longitude: "+pos.coords.longitude+"</div>";
        },
        function() {
            document.getElementById("result").innerHTML =
            "<div class='card'><h3>Para uma experiência melhor</h3>"
            + "<ul>"
            + "<li>Ative a localização do dispositivo</li>"
            + "<li>Permita localização precisa no navegador</li>"
            + "</ul>"
            + "<small>Configurações → Localização → Precisão de Local</small>"
            + "</div>";
        }
    );
}
</script>
""", height=600)
