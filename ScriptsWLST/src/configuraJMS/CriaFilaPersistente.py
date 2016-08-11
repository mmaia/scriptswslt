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


#funcao que cria um system module, subdeployment e fila jms distribuída e add no cluster.
def criaRecursosJMS(propriedades, servidores):
    nomeCluster=propriedades.get('NOME_CLUSTER')
    nomeSystemModule=propriedades.get('NOME_SYSTEM_MODULE')
    nomeSystemModule=nomeSystemModule + '-log'
    nomeSubDeployment=propriedades.get('NOME_SUBDEPLOYMENT')
    nomeSubDeployment=nomeSubDeployment + '-log'
    nomeFila=propriedades.get('NOME_FILA')
    nomeFila=nomeFila + '-persistent-log'
    jndiNameFila=propriedades.get('NOME_JNDI_FILA_LOG')
    
    #cria system module persistente e atribui ao cluster.
    cmo.createJMSSystemResource(nomeSystemModule)
    cd('/SystemResources/' + nomeSystemModule)
    set('Targets',jarray.array([ObjectName('com.bea:Name='+nomeCluster+',Type=Cluster')], ObjectName))

    tmpNomeSubDeployment=nomeSubDeployment
    #cria um subdeployment para cada servidor e add nos jms servers
    for server in servidores:
        cd('/SystemResources/' + nomeSystemModule)
        nomeSubDeployment=tmpNomeSubDeployment + '-' + propriedades.get(server)
        cmo.createSubDeployment(nomeSubDeployment)
        cd('/JMSSystemResources/'+nomeSystemModule+'/JMSResource/'+nomeSystemModule)
        fila=nomeFila + '-' + propriedades.get(server)
        cmo.createQueue(fila)
        cd('/JMSSystemResources/'+nomeSystemModule+'/JMSResource/'+ nomeSystemModule +'/Queues/'+fila)
        cmo.setJNDIName(jndiNameFila)
        cmo.setSubDeploymentName(nomeSubDeployment)
        cd('/SystemResources/'+nomeSystemModule+'/SubDeployments/'+nomeSubDeployment)
        set('Targets',jarray.array([ObjectName('com.bea:Name=JMSServer-'+propriedades.get(server)+',Type=JMSServer')], ObjectName))
    print 'Module com fila persistente e subdeployments criados'






#le e carrega arquivo de propriedades
propriedades = carregaArquivoPropriedades('config.properties')

#conecta no AdminServer
conectaAdmin(propriedades)

#carrega lista de servidores
servidores = listaServidores(propriedades)

domainConfig()
edit()
startEdit()

criaRecursosJMS(propriedades,servidores)

#Finaliza execucao do script
activate()
disconnect()
exit()
