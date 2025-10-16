def calcular_propina():
    print("\n--- Calculadora de Propinas ---\n")

    # pedir cuenta total
    cuenta = float(input("Cuanto fue la cuenta? $"))

    # pedir porcentaje
    print("\nCuanto quieres dejar?")
    print("1. 10%")
    print("2. 15%")
    print("3. 20%")
    print("4. Otro porcentaje")

    opcion = input("\nElige una opcion (1-4): ")

    if opcion == "1":
        porcentaje = 10
    elif opcion == "2":
        porcentaje = 15
    elif opcion == "3":
        porcentaje = 20
    elif opcion == "4":
        porcentaje = float(input("Que porcentaje? "))
    else:
        print("Opcion no valida")
        return

    # calculos
    propina = cuenta * (porcentaje / 100)
    total = cuenta + propina

    # mostrar resultados
    print(f"\nCuenta: ${cuenta:.2f}")
    print(f"Propina ({porcentaje}%): ${propina:.2f}")
    print(f"Total a pagar: ${total:.2f}")

    # si son varias personas
    personas = input("\nCuantas personas dividen la cuenta? (Enter para omitir): ")
    if personas:
        personas = int(personas)
        por_persona = total / personas
        print(f"Cada persona paga: ${por_persona:.2f}")


calcular_propina()