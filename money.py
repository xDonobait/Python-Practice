def desglosar_dinero(monto):
    denominaciones = [
        (100000, "Billete de $100,000"),
        (50000, "Billete de $50,000"),
        (20000, "Billete de $20,000"),
        (10000, "Billete de $10,000"),
        (5000, "Billete de $5,000"),
        (2000, "Billete de $2,000"),
        (1000, "Billete de $1,000"),
        (500, "Moneda de $500"),
        (200, "Moneda de $200"),
        (100, "Moneda de $100"),
        (50, "Moneda de $50")
    ]

    desglose = []
    monto_restante = int(monto)

    for valor, nombre in denominaciones:
        if monto_restante >= valor:
            cantidad = monto_restante // valor
            monto_restante = monto_restante % valor
            desglose.append((nombre, cantidad, valor * cantidad))

    return desglose, monto_restante


def validar_monto(monto_str):
    try:
        monto = float(monto_str.replace(",", ""))
        if monto <= 0:
            print("❌ El monto debe ser mayor a cero")
            return None
        if monto > 10000000:
            print("❌ El monto es demasiado grande")
            return None
        return monto
    except ValueError:
        print("❌ Ingrese un monto válido")
        return None


def calculadora_billetes():
    print("\n" + "=" * 60)
    print("        DESGLOSE DE BILLETES Y MONEDAS (COP)")
    print("=" * 60 + "\n")

    while True:
        monto_str = input("Ingrese el monto en pesos: $")
        monto = validar_monto(monto_str)

        if monto:
            break

    desglose, sobrante = desglosar_dinero(monto)

    print("\n" + "-" * 60)
    print("💵 DESGLOSE ÓPTIMO:")
    print("-" * 60)

    total_piezas = 0
    for nombre, cantidad, subtotal in desglose:
        print(f"   {nombre:25} x {cantidad:3} = ${subtotal:>12,}")
        total_piezas += cantidad

    print("-" * 60)
    print(f"   Total de piezas: {total_piezas}")
    print(f"   Monto total: ${int(monto):,}")

    if sobrante > 0:
        print(f"   ⚠️  Sobrante (no se puede dar): ${sobrante}")

    print("-" * 60 + "\n")


if __name__ == "__main__":
    calculadora_billetes()