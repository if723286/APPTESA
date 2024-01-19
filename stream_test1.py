import streamlit as st

def calcular_salario(tipo_unidad, vueltas, descanso_dia, descansa_domingo, bono_productividad, rendimiento_combustible, horas_trabajo):
    # Sueldo base según el tipo de unidad
    sueldo_base = {
        "Carro": 1760,
        'Camioneta': 1980,
        'Sprinter': 2200,
        'Camion': 2420
    }[tipo_unidad]

    # Restar 18 vueltas y aplicar costo por vueltas extra
    vueltas_extra = max(vueltas - 18, 0)
    pago_vuelta_extra = {
        "Carro": 73,
        'Camioneta': 85,
        'Sprinter': 97,
        'Camion': 124
    }[tipo_unidad] * vueltas_extra

    # Pago por descanso en día de descanso
    pago_descanso_laborado = sueldo_base / 7 * 2 if not descanso_dia else 0
    descanso = 220 if descanso_dia else 0

    # Pago por trabajar el domingo
    pago_domingo = sueldo_base / 7 * 0.25 if not descansa_domingo else 0

    # Pago por bono de productividad
    pago_bono_productividad = 200 if bono_productividad else 0

    # Pago por rendimiento de combustible
    pago_rendimiento_combustible = {
        'Bajo': 100,
        'Medio': 150,
        'Bueno': 200
    }[rendimiento_combustible]

    # Pago por horas de trabajo
    if 45 < horas_trabajo <= 54:
        pago_horas_trabajo = sueldo_base / 7 / 7.5 * 2 * (horas_trabajo - 45)
    elif horas_trabajo > 54:
        horas_extra_doble = min(9, horas_trabajo - 45)  # Máximo 9 horas dobles
        horas_extra_triple = max(horas_trabajo - 54, 0)  # Resto son triples
        pago_horas_trabajo = sueldo_base / 7 / 7.5 * (2 * horas_extra_doble + 3 * horas_extra_triple)
    else:
        pago_horas_trabajo = 0

    # Pago por tiempo laborando en TESA
    bono_lealtad = 0
    if vueltas > 11:
        bono_lealtad= 435
    else:
        pago_horas_trabajo = 200

    #Mondero electronico
        
    monedero = 100

    # Total del salario
    salario_total = (
        sueldo_base +
        pago_vuelta_extra +
        pago_descanso_laborado +
        descanso +
        pago_domingo +
        pago_bono_productividad +
        pago_rendimiento_combustible +
        pago_horas_trabajo +
        bono_lealtad +
        monedero
    )

    # Detalles del salario para la tabla
    detalles_salario = {
        "Concepto": ["Sueldo base", "Tiempo extra", "Vueltas extra", "Descanso laborado", "Prima dominical (si trabajo en domingo)",
                     "Bono lealtad", "Bono descanso (si descanso el día de su descanso)", "Bono productividad",
                     "Bono rendimiento", "Monedero electrónico"],
        "Cantidad $": [f"${'{:,.2f}'.format(sueldo_base)}", f"${'{:,.2f}'.format(pago_horas_trabajo)}",
                       f"${'{:,.2f}'.format(pago_vuelta_extra)}", f"${'{:,.2f}'.format(pago_descanso_laborado)}",
                       f"${'{:,.2f}'.format(pago_domingo)}", f"${'{:,.2f}'.format(bono_lealtad)}",
                       f"${'{:,.2f}'.format(descanso)}", f"${'{:,.2f}'.format(pago_bono_productividad)}",
                       f"${'{:,.2f}'.format(pago_rendimiento_combustible)}", f"${'{:,.2f}'.format(monedero)}"]
    }

    return salario_total, detalles_salario

def main():
    st.title("Calculadora de Salario para Choferes de TESA")

    tipo_unidad = st.selectbox("Selecciona el tipo de unidad que manejas", ["Camioneta", "Sprinter", "Camion", "Carro"])

    vueltas_extra = st.number_input("¿Cuántas vueltas hiciste?", min_value=0, value=18)

    horas_trabajo = st.number_input("¿Cuántas horas trabajaste?", min_value=0, value=45)

    descanso_dia = st.selectbox("¿Descansaste en tu día de descanso?", options=["Sí", "No"])

    descansa_domingo = st.selectbox("¿Descansaste el domingo?", options=["Sí", "No"])

    bono_productividad = st.selectbox("¿Ganaste bono de productividad?", options=["Sí", "No"])



    rendimiento_combustible = st.selectbox("Selecciona tu rendimiento de combustible", ["Bueno", "Bajo", "Medio"])



    if st.button("Calcular Salario"):
        salario_calculado, detalles_salario = calcular_salario(tipo_unidad, vueltas_extra, descanso_dia, descansa_domingo, bono_productividad, rendimiento_combustible, horas_trabajo)
        
        

        # Mostrar tabla con detalles del salario
        st.subheader("Detalles del Salario")
        st.table(detalles_salario)
        st.success(f"Tu salario calculado es: ${'{:,.2f}'.format(salario_calculado)}")

        # Nota sobre reducciones de ISR e IMSS
        st.warning("Recuerda que este es tu salario nominal. Aquí no están calculadas las reducciones de ISR e IMSS.")

        # Mensaje adicional con número de comunicación y horarios
        st.markdown("""
        ## ¿Tienes dudas?
        Si tienes alguna pregunta, no dudes en comunicarte con nosotros al número de atención:
        - 📞 3337320671 o 3337322424 ext 106

        Horarios de atención:
        - Viernes, sábado y lunes siguientes al depósito: 8:30 - 14:00 y 17:30 - 20:00 0
        """)

        

if __name__ == "__main__":
    main()

