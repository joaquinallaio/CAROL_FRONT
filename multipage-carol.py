#from tkinter import Button
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import requests
from streamlit_lottie import st_lottie
import pandas as pd


def load_lottieurl(url:str):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_hello = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_otmfyizb.json")

st.title("Bienvenid@ a Carol 👋")
st.markdown(
        """
       #### Desde ahora, comprar tus medicamentos será más fácil y rápido.
        """
        )


st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="high",#medium;high
    height=None,
    width=None,
    key=None,
)
components.html("""<hr style="height:6px;border:none;color:#333;background-color:#FFFFFF;" /> """)

st.markdown(" ## 1️⃣ Carga tu receta!")

price = None
df = None
spin = False
@st.cache(show_spinner=False)
def get_drugs():
    print('get drugs')
    print("ahi vamos")
    params = {"img_file": image.getvalue()}
    #api_url = "https://carol-be-image-s44yr7rzkq-ew.a.run.app/medicines"
    api_url = "http://127.0.0.1:8000/medicines"
    res = requests.post(api_url,files=params)
    drugs = res.json()
    spin = True
    return pd.DataFrame(drugs)

option = None
image = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"])
if image is not None:
    if not spin:
        with st.spinner('Interpretando receta...'):
            df = get_drugs()
            print(df.keys())
            # options_builder = GridOptionsBuilder.from_dataframe(df)
            # options_builder.configure_selection("single", use_checkbox=True)
            # grid_options = options_builder.build()
            # grid_return = AgGrid(df, grid_options)
            # st.markdown(grid_return)
            option = st.selectbox('Seleccioná tus medicamentos', df)

    else:
        st.stop()

else:
    print("no hay nada")

# components.html("""<hr style="height:6px;border:none;color:#333;background-color:#FFFFFF;" /> """)

if not option == None:
    st.markdown("## 2️⃣Confirmá tus medicamentos acá 👇🏽")
    st.markdown(f'## Seleccionaste: {option}')
    st.markdown(f"## Precio: $ {df[df.description == option]['prices'].iloc[0]}")
    st.markdown(f"## Principio activo: {df[df.description == option]['formula'].iloc[0]}")
    st.button("Comprar")
