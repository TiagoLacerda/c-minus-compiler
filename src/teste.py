from token import Token
from tokenList import TokenList

arquivo_entrada = "output/example.json"

# Abre o arquivo de entrada (resposta do analisador lexico)
f = open(arquivo_entrada, "r")
conteudo_arquivo = Token.from_json( f.read() )
f.close()

print(len(conteudo_arquivo))
lista = TokenList()
lista.insert_all_tokens(conteudo_arquivo)
print(lista.ponteiro.token.value)
lista.ponteiro = lista.cabeca
print(lista.ponteiro.token.value)
print(lista.ponteiro.posicao)
lista.next_node()
lista.next_node()
print(lista.ponteiro.posicao)