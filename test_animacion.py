import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import pathlib as Path

def func_f(x):
    return x ** 2

def draw_ani(N_base =1, N_Max =15,intervalo_x=(0, 1), intervalo_y=(0, 1), Mult = 10, tol = 1e-10, SumaDerecha=True, SumaIzquierda=True):
    N_add = N_Max - N_base
    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(5,5))

    # Crear los ejes
    ax.set_xlim(intervalo_x[0],1.1*intervalo_x[1])
    ax.set_ylim(intervalo_y[0],1.1*intervalo_y[1])
    ax.set_aspect('equal')
    # Move the left and bottom spines to x = 0 and y = 0, respectively.
    ax.spines[["left", "bottom"]].set_position(("data", 0))
    # Hide the top and right spines.
    ax.spines[["top", "right"]].set_visible(False)
    # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
    # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
    # respectively) and the other one (1) is an axes coordinate (i.e., at the very
    # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
    # actually spills out of the axes.
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    def update(frame):
        # limpiar cuadro anterior
        ax.clear()

        # Crear los ejes
        ax.set_xlim(intervalo_x[0],1.1*intervalo_x[1])
        ax.set_ylim(intervalo_y[0],1.1*intervalo_y[1])
        ax.set_aspect('equal')
        # Move the left and bottom spines to x = 0 and y = 0, respectively.
        ax.spines[["left", "bottom"]].set_position(("data", 0))
        # Hide the top and right spines.
        ax.spines[["top", "right"]].set_visible(False)
        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        # Graficar la función
        x = np.linspace(intervalo_x[0], intervalo_x[1], 100)
        y = func_f(x)
        ax.plot(x, y, color='black')

        n=np.floor(frame/Mult)
        dx=(intervalo_x[1]-intervalo_x[0])/(n-tol)
        PuntosSubintervalos=np.arange(intervalo_x[0],intervalo_x[1]+dx,dx)
        ax.text(intervalo_x[0],1.1*intervalo_y[1],f'  n = {int(n)}', fontsize=12, color='black',horizontalalignment='left',verticalalignment='center')

        # Graficar los rectangulos derecha
        if SumaDerecha:
            for i in range(np.size(PuntosSubintervalos)-1):
                ax.plot([PuntosSubintervalos[i],PuntosSubintervalos[i+1],PuntosSubintervalos[i+1],PuntosSubintervalos[i],PuntosSubintervalos[i]],[0,0,func_f(PuntosSubintervalos[i+1]),func_f(PuntosSubintervalos[i+1]),0],color='brown')
                ax.fill_between([PuntosSubintervalos[i],PuntosSubintervalos[i+1]],[func_f(PuntosSubintervalos[i+1]),func_f(PuntosSubintervalos[i+1])],color='orange')

        # Graficar los rectangulos izquierda
        if SumaIzquierda:
            for i in range(np.size(PuntosSubintervalos)-1):
                ax.plot([PuntosSubintervalos[i],PuntosSubintervalos[i+1],PuntosSubintervalos[i+1],PuntosSubintervalos[i],PuntosSubintervalos[i]],[0,0,func_f(PuntosSubintervalos[i]),func_f(PuntosSubintervalos[i]),0],color='blue')
                ax.fill_between([PuntosSubintervalos[i],PuntosSubintervalos[i+1]],[func_f(PuntosSubintervalos[i]),func_f(PuntosSubintervalos[i])],color='lightblue')

        ax.plot([intervalo_x[0],intervalo_x[0]],[0,func_f(intervalo_x[0])],color='black',linestyle='--')
        ax.plot([intervalo_x[1],intervalo_x[1]],[0,func_f(intervalo_x[1])],color='black',linestyle='--')

    ani=FuncAnimation(fig, update, frames=np.linspace(N_base*Mult,N_base*Mult+N_add*Mult,Mult*N_add), blit=False, repeat=False)

    return fig, ax, ani

def main():
    st.title('Suma de Riemann — Interactivo')

    #* opciones
    SumaDerecha = st.sidebar.toggle('Mostrar suma derecha', value=True)
    SumaIzquierda = st.sidebar.toggle('Mostrar suma izquierda', value=True)

    lado=('_izquierda' if SumaIzquierda else '')+('_derecha' if SumaDerecha else '')
    filename = f'./videos/Animacion_Riemann{lado}.mp4'


    with st.spinner('Generando gráfico...'):
        if not Path.Path(filename).exists() or not Path.Path('./videos/').exists():
            if not Path.Path('./videos/').exists():
                Path.Path('./videos/').mkdir(parents=True, exist_ok=True)
            # crea la animacion y guardala
            _, _, ani = draw_ani(SumaDerecha=SumaDerecha, SumaIzquierda=SumaIzquierda)
            ani.save(filename, writer='ffmpeg', fps=30)
        st.video(filename, autoplay=True, loop=True)
        # st.video(ani.to_html5_video())

if __name__ == '__main__':
    main()