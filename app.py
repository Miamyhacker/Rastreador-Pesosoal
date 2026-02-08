import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Segurança Ativa",
    layout="centered"
)

st.markdown("""
<style>
body {
    background-color:#0b0f14;
    color:white;
    font-family:Arial;
}
.container {
    text-align:center;
}
.circle {
    width:200px;
    height:200px;
    border-radius:50%;
    border:4px solid #2ecc71;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:48px;
    margin:auto;
    box-shadow:0 0 30px rgba(46,204,113,.6);
}
.btn {
    margin-top:20px;
    padding:16px;
    width:100%;
    font-size:18px;
    border-radius:12px;
    background:#1f2937;
    color:white;
    border:none;
}
.alert {
    margin-top:30px;
    background:#1f2937;
    padding:20px;
    border-radius:16px;
    text-align:left;
}
</style>
""", unsafe_allow_html=True)

components.html("""
<div class="container">
    <h2>Verificar segurança</h2>

    <div class="circle" id="progress">4%</div>

    <p>✅ Ambiente de pagamentos<br>
       ✅ Privacidade e segurança<br>
       ✅ Vírus</p>

    <button class="btn" onclick="pedirLocalizacao()">● ATIVAR PROTEÇÃO</button>

    <div id="msg"></div>
</div>

<script>
function pedirLocalizacao() {
    if (!navigator.geolocation) {
        document.getElementById("msg").innerHTML =
        "<div class='alert'>Geolocalização não suportada.</div>";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(pos) {
            let p = document.getElementById("progress");
            let i = 4;
            let interval = setInterval(() => {
                i += 5;
                p.innerText = i + "%";
                if (i >= 100) clearInterval(interval);
            }, 80);

            document.getElementById("msg").innerHTML =
            "<div class='alert'><b>Proteção ativada com sucesso ✅</b><br><br>"
            + "Latitude: " + pos.coords.latitude + "<br>"
            + "Longitude: " + pos.coords.longitude + "</div>";
        },
        function(err) {
            document.getElementById("msg").innerHTML =
            "<div class='alert'><h3>Para uma experiência melhor</h3>"
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
""", height=650)
