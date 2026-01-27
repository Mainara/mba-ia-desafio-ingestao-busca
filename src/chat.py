from search import search_prompt

def main():
    print("Bem-vindo ao Chat de Busca Semântica!")
    print("Digite 'sair' para encerrar.")
    print("-" * 50)

    while True:
        try:
            pergunta = input("\nFaça sua pergunta: ")
            
            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando o chat.")
                break
            
            if not pergunta.strip():
                continue

            print(f"\nPERGUNTA: {pergunta}")
            print("Processando...")
            
            resposta = search_prompt(pergunta)
            
            print(f"RESPOSTA: {resposta}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nEncerrando o chat.")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()