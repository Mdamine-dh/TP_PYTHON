import streamlit as st
import requests

st.title("Network Tool")

network = st.text_input("Adresse réseau ")
mask = st.text_input("Masque")

if st.button("Calculer"):
    full_network = network.strip() + mask.strip()
    
    # API
    try:
        res = requests.get(f"http://127.0.0.1:8000/network_info?network={full_network}")
        if res.status_code == 200:
            info = res.json()
            st.write(f"Network: {info['network']}")
            st.write(f"Broadcast: {info['broadcast']}")
            st.write(f"Netmask: {info['netmask']}")
            st.write(f"Nombre d'hôtes utilisables: {info['usable_hosts']}")
            st.write("Liste des hôtes:")
            st.write(info['hosts'])
        else:
            st.error("Erreur lors de l'appel de l'API")
    except Exception as e:
        st.error(f"Erreur: {e}")