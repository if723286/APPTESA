import streamlit as st
from datetime import datetime, timedelta

def calcular_diferencia_tiempo(vueltas):
    # Convertir los horarios a objetos datetime
    horarios_inicio = [datetime.strptime(vuelta["inicio"], '%H:%M') for vuelta in vueltas]
    horarios_fin = [datetime.strptime(vuelta["fin"], '%H:%M') for vuelta in vueltas]

    # Calcular la diferencia total de tiempo para todas las vueltas
    diferencia_tiempo_total = timedelta()

    for i in range(len(horarios_inicio)):
        vuelta = vueltas[i]
        vuelta_redonda = vuelta["redonda"]
        veces_en_semana = vuelta["veces_en_semana"]

        # Calcular la diferencia de tiempo para la vuelta actual y multiplicar por el número de veces
        if vuelta_redonda:
            tiempo_espera_minutos = vuelta["tiempo_espera"]
            diferencia_tiempo_total += ((horarios_fin[i] - horarios_inicio[i])* 2 + timedelta(minutes=tiempo_espera_minutos)) * veces_en_semana
        else:
            diferencia_tiempo_total += (horarios_fin[i] - horarios_inicio[i]) * veces_en_semana

    return diferencia_tiempo_total

def main():
    st.title("Calculadora de Diferencia de Tiempo para Vueltas")

    # Obtener los horarios de vuelta del usuario con el formato HH:MM
    num_vueltas = st.slider("Número de vueltas:", min_value=1, max_value=5, value=3)

    vueltas = []
    for i in range(num_vueltas):
        hora_inicio_str = st.time_input(f"Ingrese la hora de inicio para la vuelta {i + 1}:", value=datetime(1900, 1, 1, 0, 0))
        hora_fin_str = st.time_input(f"Ingrese la hora de fin para la vuelta {i + 1}:", value=datetime(1900, 1, 1, 23, 59))
        vuelta_redonda = st.checkbox(f"¿Es vuelta redonda para la vuelta {i + 1}?")

        veces_en_semana = st.number_input(f"¿Cuántas veces hizo esta vuelta en la semana para la vuelta {i + 1}?", min_value=1, value=1)

        tiempo_espera_minutos = 0
        if vuelta_redonda:
            tiempo_espera_minutos = st.slider(f"Seleccione el tiempo de espera (en minutos) para la vuelta {i + 1}:", min_value=1, max_value=60, value=30)

        vuelta = {"inicio": hora_inicio_str.strftime('%H:%M'), "fin": hora_fin_str.strftime('%H:%M'), "redonda": vuelta_redonda, "tiempo_espera": tiempo_espera_minutos, "veces_en_semana": veces_en_semana}
        vueltas.append(vuelta)

    # Calcular la diferencia de tiempo
    if st.button("Calcular"):
        try:
            diferencia_tiempo = calcular_diferencia_tiempo(vueltas)
            horas = diferencia_tiempo.total_seconds() // 3600
            minutos = (diferencia_tiempo.total_seconds() % 3600) // 60
            st.success(f"La diferencia total de tiempo para {num_vueltas} vueltas es: {int(horas)} horas y {int(minutos)} minutos.")
        except ValueError:
            st.error("Por favor, ingrese las horas en el formato correcto (HH:MM).")

if __name__ == "__main__":
    main()

