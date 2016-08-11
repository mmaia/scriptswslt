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



def ajustaRotacaoLogs(quantidadeArquivos):
    for servidor in servidores:
        cd('/')
        cd('Servers/' + servidor.getName() + '/Log/' + servidor.getName())
        cmo.setNumberOfFilesLimited(true)
        cmo.setFileCount(int(quantidadeArquivos))
        cd('/')
        cd('Servers/' + servidor.getName() + '/WebServer/' + servidor.getName() + '/WebServerLog/' + servidor.getName())
        cmo.setNumberOfFilesLimited(true)
        cmo.setFileCount(int(quantidadeArquivos))
    print 'Log dos servidores configurados com sucesso nos servidores deste dominio [OK]'

#configura todos os servidores do domínio para deployment:nostage
#no admin console server>Configuration>deployment>Staging Mode
def configuraDeploymentsNoStage():
    for servidor in servidores:
        cd('/')
        cd('Servers/' + servidor.getName())
        cmo.setStagingMode('nostage')
    print 'Staging mode configurado para nostage com sucesso nos servidores deste domínio [OK]'

#=================FIM DEFINICAO DE FUNCOES======================
propriedades = carregaArquivoPropriedades('config.properties')

username = propriedades.get('username')
password = propriedades.get('password')
url = propriedades.get('url')
quantidadeArquivos = propriedades.get('quantidadeArquivos')

connect(username, password, url)

servidores = getServidoresDominio()

#inicia configuração do domínio
edit()
startEdit()

ajustaRotacaoLogs(quantidadeArquivos)
configuraDeploymentsNoStage()

#ativa configurações e sai
activate()
disconnect()

exit()
