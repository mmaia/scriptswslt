from java.util     import Properties
from java.io     import FileInputStream
from java.io     import File
from java.util     import Enumeration

from string import split

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
    username = propriedades.get('USUARIO_ADMIN')
    password = propriedades.get('SENHA_ADMIN')
    url = propriedades.get('ADMIN_URL')
    connect(username, password, url)

#funcao que carrega lista de servidores
def listaServidores(propriedades):
    #========SEPARA ELEMENTOS SERVIDOR DA LISTA DE PROPRIEDADES CARREGADA==============
    #array para armazenar as chaves dos servidores definidos no arquivo de propriedades.
    servidores = []
    propertyNames = propriedades.propertyNames()
    while propertyNames.hasMoreElements():
        #carrega os nomes de todas as chaves carregadas do arquivo de propriedades
        chave = propertyNames.nextElement()
        #recupera tipo da chave para verificar se e um servidor se for adiciona no array de servidores.
        elemento = split(chave, '_')
        #checa se elemento carregado do arquivo de properties e um servidor e adiciona na lista de servidores
        if elemento[0] == 'SERVIDOR':
            servidores.append(chave)
            
    print 'A seguinte lista de servidores sera configurada aguarde....'
    for a in servidores:
        print 'Nome do servidor ==>> ' + propriedades.get(a)
    return servidores


def addServidoresCluster(propriedades, servidores):
    nomeCluster = propriedades.get('NOME_CLUSTER')
    for server in servidores:
        nomeServidor = propriedades.get(server)
        print 'Nome do servidor sendo removido do cluster==>> ' + nomeServidor 
        cd('/Servers/' + nomeServidor)
        print 'caminho ==>> ' + pwd()
        cmo.setCluster(getMBean('/Clusters/' + nomeCluster))
#=================FIM DEFINICAO DE FUNCOES======================

#funcao que cria o canal em todos os servidores no ip do proprio servior e na porta do cluster definida
def criaChannelCluster(propriedades, servidores):
    portaCluster = propriedades.get('PORTA_CLUSTER')
    nomeChannel=propriedades.get('NOME_CHANNEL_CLUSTER')
    for server in servidores:
        nomeServidor = propriedades.get(server)
        ipServidor = propriedades.get('IP_' + server)
        cd('/Servers/' + nomeServidor)
        cmo.createNetworkAccessPoint(nomeChannel)
        cd('/Servers/' + nomeServidor + '/NetworkAccessPoints/' + nomeChannel)
        cmo.setProtocol('cluster-broadcast')
        cmo.setListenAddress(ipServidor)
        cmo.setListenPort(int(portaCluster))
        cmo.setEnabled(true)
        cmo.setHttpEnabledForThisProtocol(true)
        cmo.setTunnelingEnabled(false)
        cmo.setOutboundEnabled(false)
        cmo.setTwoWaySSLEnabled(false)
        cmo.setClientCertificateEnforced(false)
        
    
def criaCluster(propriedades):
    nomeChannel=propriedades.get('NOME_CHANNEL_CLUSTER')
    nomeCluster=propriedades.get('NOME_CLUSTER')
    cd('/')
    cmo.createCluster(nomeCluster)
    cd('/Clusters/' + nomeCluster)
    cmo.setClusterMessagingMode('unicast')
    cmo.setClusterBroadcastChannel(nomeChannel)

#le e carrega arquivo de propriedades
propriedades = carregaArquivoPropriedades('config.properties')

#conecta no AdminServer
conectaAdmin(propriedades)

#carrega lista de servidores
servidores = listaServidores(propriedades)

domainConfig()
edit()
startEdit()

criaChannelCluster(propriedades, servidores)

criaCluster(propriedades)

#Finaliza execucao do script
activate()
disconnect()
exit()
