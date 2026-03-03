import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

tam_fuentes=12

@np.vectorize
def func_f(x: int):
  return ((-1)**x)*(1/x)

def Draw_Sucesion_1D(n , intervalo_x = [-0.05,1.05], intervalo_y = [-0.125,0.125],solo_ultimo = False, Plot_dark = True, ocultar_etiquetas = False):
  indices_suc= np.arange(1,n+1)

  #! iniciar figura
  fig , ax = plt.subplots(figsize=(12,1))
  aux1=min(0,intervalo_x[0])
  aux2=max(1,intervalo_x[1])
  dif = aux2-aux1
  ax.set_xlim(aux1-0.05*dif,aux2+0.05*dif)
  ax.set_ylim(*intervalo_y)

  #* dibujar ejes coordenados
  ax.spines[["bottom"]].set_position(("data", 0))
  ax.spines[["left", "top", "right"]].set_visible(False)
  ax.plot(1, 0, ">", transform=ax.get_yaxis_transform(), clip_on=False, color = 'white' if Plot_dark else 'black')

  # Graficar la función
  if solo_ultimo:
    sucesion = func_f(n)
  else:
    sucesion = func_f(indices_suc)

  ax.scatter(sucesion,np.zeros_like(sucesion) , color='cyan' if Plot_dark else 'blue', s=30)

  # etiquetas de los puntos
  if not ocultar_etiquetas:
    if solo_ultimo:
      ax.text(sucesion, 0.025 , f'a {n}', fontsize=tam_fuentes, ha='center', va='bottom')
    else:
      for i in range(n):
        ax.text(sucesion[i], 0.025 , f'a {i+1}', fontsize=tam_fuentes, ha='center', va='bottom')

  # etiquetas de los valores en los ejes
  etiquetas_x = np.arange(aux1, aux2+0.1*(aux2-aux1), 0.1*(aux2-aux1))
  ax.set_xticks(etiquetas_x)
  ax.set_yticks([])

  # tamaño de fuentes en los ejes
  ax.tick_params(axis='both', which='major', labelsize=tam_fuentes)

  return fig


def main():
  #! parametros para grafico
  Plot_dark = True

  # intervalos x e y
  intervalo_x = [-1.5,1.5]

  # cantidad numero de elementos de la sucesion
  n=6

  #! Configuración de la página de Streamlit
  st.set_page_config(page_title="Visualización 1D de una sucesión", layout="wide", initial_sidebar_state='expanded', page_icon=':material/line_axis:')#, menu_items={'Get Help': 'https://www.extremelycoolapp.com/help','Report a bug': "https://www.extremelycoolapp.com/bug",'About': "# This is a header. This is an *extremely* cool app!"})

  #! Titulo
  st.title('Visualización 1D de una sucesión')

  #! Checkboxes para opciones de visualización
  # n = st.sidebar.slider('indique el valor de $n$', 1, 100, 6, 1)
  n = st.sidebar.number_input('indique el valor de n', min_value=1, value=n, step=1)
  # solo_ultimo = st.sidebar.checkbox('Mostrar solo el último término', value=False)
  ocultar_etiquetas = st.sidebar.toggle('Ocultar etiquetas sucesión', value=False)
  solo_ultimo = st.sidebar.toggle('Mostrar solo el término actual', value=False)
  # Plot_dark = st.sidebar.checkbox('Tema oscuro en el gráfico', value=Plot_dark)
  Plot_dark = st.sidebar.toggle(label='Gráfico modo oscuro', value=True, key='toggle_dark_mode')
  if Plot_dark:
    plt.style.use('dark_background')
  else:
    plt.style.use('default')

  #! Generar gráfico con spinner
  with st.spinner('Generando gráfico...'):
    fig = Draw_Sucesion_1D(n , intervalo_x, solo_ultimo=solo_ultimo, Plot_dark=Plot_dark, ocultar_etiquetas=ocultar_etiquetas)
  st.pyplot(fig)
  # st.markdown(f'$a_n = \\dfrac{{(-1)^{{n}}}}{{n}}$')

if __name__ == "__main__":
  main()
