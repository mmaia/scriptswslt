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


#funcao que retorna lista de todos os servidores configurados para este domínio.
def getServidoresDominio():
    print 'executando funcao getServidoresDominio'
    domainConfig()
    servidores = cmo.getServers()
    return servidores
    
def habilitaPorta80(listenPortEnabled, listenPort):
    for servidor in servidores:
        if servidor.getName() != 'AdminServer' : 
            cd('/')
            cd('Servers/' + servidor.getName())
            cmo.setListenPort(int(listenPort))
            if listenPortEnabled == 'true' :
                cmo.setListenPortEnabled(true)
            else :
                cmo.setListenPortEnabled(false)
    print 'Porta 80 habilitada nos servidores'

#=================FIM DEFINICAO DE FUNCOES======================
propriedades = carregaArquivoPropriedades('config.properties')

username = propriedades.get('username')
password = propriedades.get('password')
url = propriedades.get('url')

listenPort = propriedades.get('listenPort')
listenPortEnabled = propriedades.get('listenPortEnabled')

connect(username, password, url)

servidores = getServidoresDominio()

#inicia configuração do domínio
edit()
startEdit()

habilitaPorta80(listenPortEnabled, listenPort)

#ativa configurações e sai
activate()
disconnect()

exit()
