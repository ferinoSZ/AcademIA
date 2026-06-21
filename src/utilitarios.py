PALAVRAS_IGNORADAS = {
    "como", "funciona", "qual", "quais", "sobre",
    "para", "com", "que", "uma", "um",
    "dos", "das", "do", "da", "de",
    "os", "as", "ao", "aos", "em", "por",
}


def pegar_palavras_importantes(texto):

    texto_limpo = ""

    for caractere in texto.lower():

        if caractere.isalnum():
            texto_limpo += caractere

        else:
            texto_limpo += " "

    return {
        palavra
        for palavra in texto_limpo.split()
        if len(palavra) >= 3
        and palavra not in PALAVRAS_IGNORADAS
    }