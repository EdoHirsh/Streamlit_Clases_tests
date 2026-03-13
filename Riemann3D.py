import matplotlib.pyplot as plt
import streamlit as st

def func_f(x, y):
  return x ** 2 + y ** 2

def draw_riemann(m, n, intervalo_x=(0, 5), intervalo_y=(0, 5), intervalo_x_graf=(0,5), intervalo_y_graf=(0,5), intervalo_z_graf=(0, 50),alpha=1, beta=1):
  largo_x = intervalo_x[1] - intervalo_x[0]
  largo_y = intervalo_y[1] - intervalo_y[0]

  fig = plt.figure(figsize=(8, 6))
  ax = fig.add_subplot(111, projection='3d')
  ax.set_xlim(intervalo_x_graf)
  ax.set_ylim(intervalo_y_graf)
  ax.set_zlim(intervalo_z_graf)

  dx = largo_x / m
  dy = largo_y / n

  vol_aprox = 0.0
  zmin = intervalo_z_graf[0]
  zmax = intervalo_z_graf[1]

  for i in range(m):
    for j in range(n):
      x_i = intervalo_x[0] + i * dx
      y_j = intervalo_y[0] + j * dy
      z0 = 0
      dz = func_f(x_i + alpha*dx, y_j + beta*dy)
      color = plt.cm.gnuplot((dz - zmin) / (zmax - zmin) if zmax > zmin else 0)
      ax.bar3d(x_i, y_j, z0, dx, dy, dz, color=color, alpha=0.9, shade=True)
      vol_aprox += dz * dx * dy

  ax.set_xlabel('$x$')
  ax.set_ylabel('$y$')
  ax.set_zlabel('$z$')
  ax.set_title(f'$f(x,y)=x^2+y^2$')

  return fig, vol_aprox

def main():
  rango_m = (1, 16)
  rango_n = (1, 16)

  st.title('Suma de Riemann 3D — Interactivo')

  #* Deslizadores para m y n en la barra lateral
  m = st.sidebar.slider('Particiones en eje $x$ ($m$)', min_value=rango_m[0], max_value=rango_m[1], value=8, step=1)
  n = st.sidebar.slider('Particiones en eje $y$ ($n$)', min_value=rango_n[0], max_value=rango_n[1], value=8, step=1)

  #* Deslizadores para alpha y beta (punto de evaluación dentro de cada subrectángulo)
  Punto_muestra = st.sidebar.selectbox("Punto de muestra:",["extremo inferior izquierdo","extremo superior derecho","punto medio"], index=1)
  match Punto_muestra:
    case "extremo inferior izquierdo":
      alpha, beta = 0.0, 0.0
    case "extremo superior derecho":
      alpha, beta = 1.0, 1.0
    case "punto medio":
      alpha, beta = 0.5, 0.5

  vol_real = 1250/3

  with st.spinner('Generando gráfico...'):
    fig, vol = draw_riemann(m, n,alpha=alpha, beta=beta)
    st.pyplot(fig)
    st.markdown(f'**Volumen aproximado:** {vol:.2f}')
    st.markdown(f'**Volumen real:** {vol_real:.2f}')

if __name__ == '__main__':
  main()