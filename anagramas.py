def limpiar_texto(texto):
    texto = texto.lower()
    texto = texto.replace(" ", "")
    texto = ''.join(c for c in texto if c.isalpha())
    return texto


def son_anagramas(palabra1, palabra2):
    palabra1_limpia = limpiar_texto(palabra1)
    palabra2_limpia = limpiar_texto(palabra2)

    if len(palabra1_limpia) != len(palabra2_limpia):
        return False, None

    if palabra1_limpia == palabra2_limpia:
        return False, "son_iguales"

    return sorted(palabra1_limpia) == sorted(palabra2_limpia), None


def mostrar_letras(palabra):
    palabra_limpia = limpiar_texto(palabra)
    letras = {}
    for letra in palabra_limpia:
        letras[letra] = letras.get(letra, 0) + 1
    return letras


def detector_anagramas():
    print("\n" + "=" * 60)
    print("              DETECTOR DE ANAGRAMAS")
    print("=" * 60 + "\n")

    palabra1 = input("Ingrese la primera palabra: ").strip()
    palabra2 = input("Ingrese la segunda palabra: ").strip()

    if not palabra1 or not palabra2:
        print("\n❌ Debe ingresar ambas palabras\n")
        return

    es_anagrama, tipo = son_anagramas(palabra1, palabra2)

    print("\n" + "-" * 60)
    print("📝 ANÁLISIS:")
    print("-" * 60)
    print(f"   Palabra 1: {palabra1}")
    print(f"   Palabra 2: {palabra2}")
    print("-" * 60)

    letras1 = mostrar_letras(palabra1)
    letras2 = mostrar_letras(palabra2)

    print(f"   Letras de '{palabra1}': {dict(sorted(letras1.items()))}")
    print(f"   Letras de '{palabra2}': {dict(sorted(letras2.items()))}")
    print("-" * 60)

    if tipo == "son_iguales":
        print("   ⚠️  Las palabras son IDÉNTICAS (no son anagramas)")
    elif es_anagrama:
        print("   ✅ ¡SÍ son ANAGRAMAS!")
    else:
        print("   ❌ NO son anagramas")

    print("-" * 60 + "\n")

    print("💡 Ejemplos de anagramas:")
    print("   • amor ↔ roma")
    print("   • teatro ↔ atroté")
    print("   • listen ↔ silent\n")


if __name__ == "__main__":
    detector_anagramas()