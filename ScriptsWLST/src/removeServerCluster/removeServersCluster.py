from java.util 	import Properties
from java.io 	import FileInputStream
from java.io 	import File

#============DEFINICAO DE FUNCOES============
#funcao que carrega dados de arquivo de propriedades
def carregaArquivoPropriedades(nomeArquivo) :
    print 'carregando propriedades do arquivo: ' + nomeArquivo
    #arquivo de propriedades a ser carregado
    localizacaoArquivoPropriedadesConfiguracao = nomeArquivo    
    myProps = Properties()
    #carrega arquivo de propriedades
    myProps.load(FileInputStream(File(localizacaoArquivoPropriedadesConfiguracao)))
    return myProps

#funcao que conecta no admin server utilizando dados definidos em arquivo de propriedades
def conectaAdmin(propriedades):
    username = propriedades.get('username')
    password = propriedades.get('password')
    url = propriedades.get('url')
    connect(username, password, url)

#funcao que carrega lista de servidores
def listaServidores(propriedades):
    print 'nao implementado'


#=================FIM DEFINICAO DE FUNCOES======================

#le e carrega arquivo de propriedades.
propriedades = carregaArquivoPropriedades('config.properties')

#conecta no AdminServer
conectaAdmin(propriedades)






#lista para armazenar servidores n�o acess�veis atrav�s do admin server.
servidoresNaoAcessiveis = []

servidores = getServidoresDominio()

mostraStatusServidores(servidores)

listaConfiguracoesMemoriaServidoresDomino()

checaThreadsServidoresDominio()

checaPoolsConexoes()

disconnect()

exit()
