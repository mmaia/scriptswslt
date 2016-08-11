from java.util 	import Properties

from java.io 	import FileInputStream

from java.io 	import File

from java.util 	import Enumeration

#arquivo de propriedades a ser carregado
propFileLocation = 'C:\\bea\\scripts_WLST\\configuracao.properties'

myProps = Properties()

myProps.load(FileInputStream(File(propFileLocation)))

propertyNames = myProps.propertyNames()

while propertyNames.hasMoreElements():
    #imprime on nomes de todas as chaves carregadas de um arquivo de propriedades
    chave = propertyNames.nextElement()
    print str(chave)
    print '' + myProps.getProperty(chave)