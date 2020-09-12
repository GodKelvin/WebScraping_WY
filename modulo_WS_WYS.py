#Autor: Kelvin Lehrback
#Site base: --Site removido por questao de sigilo--

import urllib.request
from bs4 import BeautifulSoup
#from requests import get

#importe o pandas para converter a lista em uma planilha
import pandas as pd

#Apenas para fim de debugger
import time


def main(args):
	inicioTempo = time.time()
	
	#Criando o dataframe para guardar os dados das cartas
	#Definindo as colunas
	colunasDF = ["Nome", "Edicao", "Preco"]
	dfCartas = pd.DataFrame(columns = colunasDF)
	
	#Variavel para andar pela linha do DataFrame
	linhaDF = 0
	
	
	#Lista/Num de paginas p/ extrair os dados
	listaUrl = []
	for i in range(1,5):
		#Atencao ao padrao de numeracao do respectivo site
		url = "--site removido por questao de sigilo--" + str(i)
		listaUrl.append(url)
	
	#Especificando a URL
	#Atencao ao final da URL, 1 eh o numero da pag
	#url = ""
	
	#Para cada URL na lista de URL[...]
	for url in listaUrl:
		#consultando o site e retornando o html para a variavel Page
		page = urllib.request.urlopen(url)
		
		#Armazenando o HTML no formato BeautifulSoup
		htmlSoup = BeautifulSoup(page, "html5lib")

		#Contem um container com os dados das cartas
		containerCard = htmlSoup.find_all("div", class_ = "pProdItens")
		
		#Variaveis utilizadas
		nomeCartaGeral = ""
		edicaoGeral = ""
		nomeCarta = ""
		edicaoCarta = ""
		preco = 0.0
		
		#Variaveis para andar nas linhas do DataFrame
		#Mesmo nome das colunas setadas la em cima
		nomeColDF = "Nome"
		edicaoColDF = "Edicao"
		precoColDF = "Preco"
		
		#Para cada carta dentro do container, pegamos os seus dados
		for carta in containerCard:
			#Extraindo o preço da respectiva carta do site
			preco = carta.find("td", class_ = "pPrecoP")
			preco = preco.text
			preco = preco.strip("R$ ")
			if(preco == ""):
				preco = "N.D"
			
			#Tag e Classe que contem o nome da carta
			#"Encontra na tag 'a' com nome "itemNameP"[...]
			nomeCarta = carta.find("a", class_ = "itemNameP").text
			edicao = nomeCarta.split()
			edicao = edicao[len(edicao) - 1]
			
			#Removo do nome a sigla da primeira edicao encontrada
			nomeCarta = nomeCarta.strip(edicao)
			
			#ATENCAO ISSO AQUI EH IMPORTANTE
			#Armazeno o primeiro nome encontrado(PT ou EN) da carta/edicao nas variaveis
			nomeCartaGeral = nomeCarta
			edicaoGeral = edicao
			
			#Atencao que nessa chamada nao tem texto no "nomeCarta"
			nomeCarta = carta.find("a", class_ = "itemNamePI")
			
			#Se a carta possuir outro idioma (nome e edicao em PT/EN)
			if(nomeCarta != None):
				#Agora sim o "nomeCarta" tem texto
				nomeCarta = nomeCarta.text
				
				#Concateno o nome em portugues e ingles
				nomeCartaGeral = nomeCartaGeral + '/ ' + nomeCarta
				
				#Pegando a segunda sigla da edicao
				edicao = nomeCartaGeral.split()
				edicao = edicao[len(edicao) - 1]
				
				#Removo do nome a sigla da segunda edicao encontrada
				nomeCartaGeral = nomeCartaGeral.strip(edicao)
				
				#Concatenando ambas as siglas de edicoes (portugues e ingles)
				edicaoGeral = edicaoGeral + ' / ' + edicao
			
			#Colocando os valores encontrados no DataFrame
			#Jeito antigo no Pandas
			'''
			dfCartas.set_value(linhaDF, nomeColDF, nomeCartaGeral)
			dfCartas.set_value(linhaDF, edicaoColDF, edicaoGeral)
			dfCartas.set_value(linhaDF, precoColDF, preco)
			'''
			
			#Jeito novo no Pandas
			#Linha tal na coluna tal recebe tal valor
			dfCartas.at[linhaDF, nomeColDF] = nomeCartaGeral
			dfCartas.at[linhaDF, edicaoColDF] = edicaoGeral
			dfCartas.at[linhaDF, precoColDF] = preco
			
			#Apos o preenchimento dos dados da carta, desce uma linha
			linhaDF += 1
			
			
			'''
			print("Nome: %s\n" %nomeCartaGeral)
			print("Edicao: %s\n" %edicaoGeral)
			print("Preco: %s\n" %preco)
			print("-----------------------------------\n")
			'''

			
	#print(dfCartas)
	#Gerando o arquivo .CSV
	dfCartas.to_csv ("preco.csv", index = None, header=True)
	print("Arquivo criado com sucesso!")
	
	fimTempo = time.time()
	print(fimTempo - inicioTempo)
	return 0
	
    
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
