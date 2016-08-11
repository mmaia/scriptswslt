from java.util 	import Properties
from java.io 	import FileInputStream
from java.io 	import File
from java.util 	import Enumeration

myProps = Properties()

def carregaPropriedades(nomeArquivo):
    #carrega arquivo de propriedades
    myProps.load(FileInputStream(File(nomeArquivo)))

#chama a função definida acima
carregaPropriedades('exemplo.properties')

propertyNames = myProps.propertyNames()
while propertyNames.hasMoreElements():
    #imprime on nomes de todas as chaves carregadas do arquivo de propriedades
    chave = propertyNames.nextElement()
    print str(chave)
    print '' + myProps.getProperty(chave)