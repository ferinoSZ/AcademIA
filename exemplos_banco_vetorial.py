"""
Exemplos de uso avançado do banco vetorial AcademIA
Execute cada função independentemente para testar
"""

import sys
sys.path.insert(0, './src')

from banco_vetorial import *
from embeddings import gerar_embedding_pergunta
from ingestao import carregar_chunks

# ============================================================================
# EXEMPLO 1: Reset completo do banco
# ============================================================================
def exemplo_resetar_banco():
    print("\n📌 EXEMPLO 1: Resetar banco")
    print("-" * 40)
    
    if verificar_banco_existe():
        resposta = input("Banco existe. Deseja limpar? (s/n): ")
        if resposta.lower() == 's':
            limpar_banco()
            print("Banco limpo")
    else:
        print("Banco não existe ainda")

# ============================================================================
# EXEMPLO 2: Verificar stats do banco
# ============================================================================
def exemplo_stats():
    print("\n EXEMPLO 2: Ver estatísticas do banco")
    print("-" * 40)
    
    if not verificar_banco_existe():
        print(" Banco não existe. Execute main.py primeiro")
        return
    
    colecao = inicializar_banco()
    stats = obter_stats_banco(colecao)
    
    print(" Estatísticas do Banco Vetorial:")
    print(f"  • Nome: {stats['nome_colecao']}")
    print(f"  • Chunks armazenados: {stats['total_chunks']}")
    print(f"  • Localização: {stats['caminho']}")

# ============================================================================
# EXEMPLO 3: Buscar manualmente com diferentes perguntas
# ============================================================================
def exemplo_buscar_manual():
    print("\n EXEMPLO 3: Buscar com perguntas diferentes")
    print("-" * 40)
    
    if not verificar_banco_existe():
        print(" Banco não existe. Execute main.py primeiro")
        return
    
    perguntas = [
        "O que é perda de funcionário?",
        "Como solicitar um documento?",
        "Qual é o horário de funcionamento?"
    ]
    
    colecao = inicializar_banco()
    chunks = carregar_chunks()
    
    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n  Pergunta {i}: '{pergunta}'")
        
        vetor = gerar_embedding_pergunta(pergunta)
        indices = buscar_no_banco_vetorial(vetor, colecao, num_resultados=3)
        
        for j, indice in enumerate(indices, 1):
            chunk = chunks[indice]
            print(f"    {j}. [{chunk['titulo']}] - Pág {chunk['pagina']}")

# ============================================================================
# EXEMPLO 4: Inspecionar um chunk específico
# ============================================================================
def exemplo_inspecionar_chunk():
    print("\n EXEMPLO 4: Inspecionar chunk específico")
    print("-" * 40)
    
    colecao = inicializar_banco()
    chunks = carregar_chunks()
    
    if not chunks:
        print("Nenhum chunk encontrado")
        return
    
    indice = 0  # Primeiro chunk
    chunk = chunks[indice]
    
    print(f"\nChunk #{chunk['id']}:")
    print(f"  • ID: {chunk['id']}")
    print(f"  • Grupo: {chunk['grupo']}")
    print(f"  • Ordem no grupo: {chunk['ordem']}")
    print(f"  • Título: {chunk['titulo']}")
    print(f"  • Página: {chunk['pagina']}")
    print(f"  • Tamanho texto: {len(chunk['texto'])} caracteres")
    print(f"\n  Texto (primeiros 200 chars):")
    print(f"  {chunk['texto'][:200]}...")

# ============================================================================
# EXEMPLO 5: Busca com top-k variável
# ============================================================================
def exemplo_top_k_variavel():
    print("\n EXEMPLO 5: Comparar resultados com diferentes top-k")
    print("-" * 40)
    
    colecao = inicializar_banco()
    pergunta = "achados e perdidos"
    
    for k in [3, 5, 10]:
        print(f"\n  Top-{k} resultados:")
        
        vetor = gerar_embedding_pergunta(pergunta)
        indices = buscar_no_banco_vetorial(vetor, colecao, num_resultados=k)
        
        print(f"  Retornou {len(indices)} resultados: {list(indices)}")

# ============================================================================
# EXEMPLO 6: Exportar chunks para análise
# ============================================================================
def exemplo_exportar_chunks():
    print("\n EXEMPLO 6: Exportar chunks para arquivo")
    print("-" * 40)
    
    import json
    from datetime import datetime
    
    colecao = inicializar_banco()
    chunks = carregar_chunks()
    
    # Prepara dados para exportar
    dados_export = {
        "timestamp": datetime.now().isoformat(),
        "total_chunks": len(chunks),
        "chunks": []
    }
    
    for chunk in chunks[:5]:  # Apenas 5 primeiros para exemplo
        dados_export["chunks"].append({
            "id": chunk["id"],
            "titulo": chunk["titulo"],
            "pagina": chunk["pagina"],
            "grupo": chunk["grupo"],
            "tamanho_texto": len(chunk["texto"])
        })
    
    # Salva em arquivo
    caminho = "chunks_export.json"
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados_export, f, ensure_ascii=False, indent=2)
    
    print(f" Dados exportados para {caminho}")
    print(f"  Total de chunks: {dados_export['total_chunks']}")
    print(f"  Amostra de 5 chunks salva")

# ============================================================================
# EXEMPLO 7: Validar integridade do banco
# ============================================================================
def exemplo_validar_banco():
    print("\n EXEMPLO 7: Validar integridade do banco")
    print("-" * 40)
    
    if not verificar_banco_existe():
        print(" Banco não existe")
        return
    
    colecao = inicializar_banco()
    stats = obter_stats_banco(colecao)
    
    print("Validações:")
    print(f"Arquivo existe: {verificar_banco_existe()}")
    print(f"Coleção carregável: {colecao is not None}")
    print(f"Contém chunks: {stats['total_chunks'] > 0}")
    print(f"Banco válido: OK")

# ============================================================================
# Menu principal
# ============================================================================
def menu():
    exemplos = {
        '1': ('Resetar banco completamente', exemplo_resetar_banco),
        '2': ('Ver estatísticas do banco', exemplo_stats),
        '3': ('Buscar com perguntas diferentes', exemplo_buscar_manual),
        '4': ('Inspecionar um chunk', exemplo_inspecionar_chunk),
        '5': ('Comparar top-k variável', exemplo_top_k_variavel),
        '6': ('Exportar chunks para JSON', exemplo_exportar_chunks),
        '7': ('Validar integridade', exemplo_validar_banco),
    }
    
    print("\n" + "=" * 60)
    print("EXEMPLOS AVANÇADOS - BANCO VETORIAL ACADEMIA")
    print("=" * 60)
    
    for chave, (descricao, _) in exemplos.items():
        print(f"  [{chave}] {descricao}")
    
    print(f"  [0] Sair")
    print("=" * 60)
    
    escolha = input("\nEscolha uma opção: ")
    
    if escolha in exemplos:
        try:
            exemplos[escolha][1]()
        except Exception as e:
            print(f"\n Erro: {e}")
            import traceback
            traceback.print_exc()
    elif escolha != '0':
        print(" Opção inválida")

if __name__ == "__main__":
    try:
        while True:
            menu()
            continuar = input("\nExecutar outro exemplo? (s/n): ")
            if continuar.lower() != 's':
                print("\nAté logo!")
                break
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário")
