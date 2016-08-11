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

def criaConnectionFactory(propriedades):
    nomeCluster=propriedades.get('NOME_CLUSTER')
    nomeSystemModule=propriedades.get('NOME_SYSTEM_MODULE')
    nomeSystemModule=nomeSystemModule + '-pooling'
    nomeSubDeployment=propriedades.get('NOME_SUBDEPLOYMENT')
    nomeSubDeployment=nomeSubDeployment + '-pooling'
    nomeFactory=propriedades.get('NOME_JMS_CONNECTION_FACTORY')
    nomeJndiFactory=propriedades.get('NOME_JNDI_CONNECTION_FACTORY')
    cd('/JMSSystemResources/' + nomeSystemModule + '/JMSResource/' + nomeSystemModule)
    cmo.createConnectionFactory(nomeFactory)
    cd('/JMSSystemResources/' + nomeSystemModule + '/JMSResource/' + nomeSystemModule + '/ConnectionFactories/' + nomeFactory)
    cmo.setJNDIName(nomeJndiFactory)
    cd('/JMSSystemResources/' + nomeSystemModule + '/JMSResource/' + nomeSystemModule + '/ConnectionFactories/' + nomeFactory + '/SecurityParams/' + nomeFactory)
    cmo.setAttachJMSXUserId(false)
    cd('/JMSSystemResources/' + nomeSystemModule + '/JMSResource/' + nomeSystemModule + '/ConnectionFactories/' + nomeFactory)
    cmo.setSubDeploymentName(nomeSubDeployment)
    cd('/JMSSystemResources/' + nomeSystemModule + '/JMSResource/' + nomeSystemModule + '/ConnectionFactories/' + nomeFactory + '/TransactionParams/' + nomeFactory)
    cmo.setTransactionTimeout(180)
    cmo.setXAConnectionFactoryEnabled(true)
    print ''


#le e carrega arquivo de propriedades
propriedades = carregaArquivoPropriedades('config.properties')

#conecta no AdminServer
conectaAdmin(propriedades)

#carrega lista de servidores
servidores = listaServidores(propriedades)

domainConfig()
edit()
startEdit()

criaConnectionFactory(propriedades)

#Finaliza execucao do script
activate()
disconnect()
exit()
