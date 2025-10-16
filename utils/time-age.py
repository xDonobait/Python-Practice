from datetime import datetime, timedelta


def calcular_edad(fecha_nacimiento):
    hoy = datetime.now()

    años = hoy.year - fecha_nacimiento.year
    meses = hoy.month - fecha_nacimiento.month
    dias = hoy.day - fecha_nacimiento.day

    if dias < 0:
        meses -= 1
        dias_mes_anterior = (hoy.replace(day=1) - timedelta(days=1)).day
        dias += dias_mes_anterior

    if meses < 0:
        años -= 1
        meses += 12

    return años, meses, dias


def validar_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        if fecha > datetime.now():
            print("❌ La fecha no puede ser futura")
            return None
        return fecha
    except ValueError:
        print("❌ Formato de fecha inválido. Use DD/MM/AAAA")
        return None


def calculadora_edad():
    print("\n" + "=" * 50)
    print("           CALCULADORA DE EDAD")
    print("=" * 50 + "\n")

    while True:
        fecha_str = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ")
        fecha_nacimiento = validar_fecha(fecha_str)

        if fecha_nacimiento:
            break

    años, meses, dias = calcular_edad(fecha_nacimiento)

    print("\n" + "-" * 50)
    print("📅 RESULTADO:")
    print("-" * 50)
    print(f"   Edad: {años} años, {meses} meses y {dias} días")
    print("-" * 50)

    dias_totales = (datetime.now() - fecha_nacimiento).days
    print(f"   Total de días vividos: {dias_totales:,} días")
    print(f"   Total de horas: {dias_totales * 24:,} horas")
    print("-" * 50 + "\n")


if __name__ == "__main__":
    calculadora_edad()