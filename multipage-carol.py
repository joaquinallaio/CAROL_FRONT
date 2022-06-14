#from tkinter import Button
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import requests
from streamlit_lottie import st_lottie
import pandas as pd

# image = Image.open("../marcacarol.png", "rb")

# st.image(image, caption='Sunrise by the mountains')

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

st.markdown(
        """
       ## 1️⃣ Carga tu receta?
        """
        )

price = None
df = None
spin = False
@st.cache(show_spinner=False)
def get_drugs():
    print('get drugs')
    print("ahi vamos")
    params = {"img_file": image.getvalue()}
    api_url = "https://carol-be-image-s44yr7rzkq-ew.a.run.app/medicines"
    res = requests.post(api_url,files=params)
    drugs = res.json()
    spin = True
    return pd.DataFrame(drugs)


image = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"])
if image is not None:
    if not spin:
        with st.spinner('Interpretando receta...'):
            df = get_drugs()
            print(df.keys())
            options_builder = GridOptionsBuilder.from_dataframe(df)
            options_builder.configure_selection("single", use_checkbox=True)
            grid_options = options_builder.build()
            grid_return = AgGrid(df, grid_options)
            st.markdown("#" + grid_return)
            # option = st.selectbox('Seleccioná tus medicamentos', df)
            # st.markdown(f'Seleccionaste: {option}')
            # st.markdown(df[df.description == option]['prices'].iloc[0])
    else:
        st.stop()

else:
    print("no hay nada")



# with st.spinner('Wait for it...'):
#     time = time.sleep(5)

# if st.button(" 📸 Sacá una foto de tu receta"):
#     camera = st.camera_input(" 📸 Sacá una foto de tu receta")

def confirmar_medicamento():
    import streamlit as st
    st.button("Confirmar medicamento")

# # page_names_to_funcs = {
#      " 🏠 Home": home,
#      " 💻 Cargá tu receta desde tu dispositivo": " 💻 Cargá tu receta desde tu dispositivo",
#      " 📸 Sacá una foto de tu receta": sacar_foto,
#      " ✅ Confirmar tu medicamento": confirmar_medicamento,
#         }


# barra_azul = st.sidebar.selectbox("Qué te gustaría hacer?", page_names_to_funcs.keys())
# page_names_to_funcs[barra_azul]()

st.write("#")
st.write("#")
components.html("""<hr style="height:6px;border:none;color:#333;background-color:#FFFFFF;" /> """)
'''
## 2️⃣Confirmá tus medicamentos acá 👇🏽
'''
