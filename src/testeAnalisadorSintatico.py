from token import Token
from syParser import SyParser
import os.path

arquivo_entrada = "output/example.json"
arquivo_entrada_invalido = "output/exampleInvalido.json"

# Verifica se o arquivo de entrada existe no diretorio
if not os.path.exists(arquivo_entrada):
    print("Arquivo de entrada não existe")

if not os.path.exists(arquivo_entrada_invalido):
    print("Arquivo de entrada não existe")

# Abre o arquivo de entrada (resposta do analisador lexico)
f = open(arquivo_entrada, "r")
conteudo_arquivo = Token.from_json( f.read() )
f.close()

p = SyParser(entrada=conteudo_arquivo)
p.parse()
