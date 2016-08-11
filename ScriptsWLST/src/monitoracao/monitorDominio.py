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


#funcao que retorna lista de todos os servidores configurados para este dom�nio.
def getServidoresDominio():
    print 'executando funcao getServidoresDominio'
    domainConfig()
    servidores = cmo.getServers()
#    print '===============================LISTA SERVIDORES DESTES DOM�NIO==============='
#    for servidor in servidores:
#        print servidor.getName()
#    print '===============================FIM LISTA SERVIDORES===========\n\n'
    return servidores

#funcao que pega lista de servidores como parametro e verifica o status de cada um deles.
def mostraStatusServidores(servidores): 
    print '=======================STATUS dos servidores do domínio==============='
    domainRuntime()
    for servidor in servidores:
        try:
            cd('/ServerRuntimes/' + servidor.getName())
            #ls()
            print servidor.getName() + ': ' + get('State')
        except WLSTException,e:
            servidoresNaoAcessiveis.append(servidor)
    
    servidoresAlerta = []
    #testa novamente servidores que n�o estava acess�veis para ter certeza
    for servidor in servidoresNaoAcessiveis : 
        try:
            cd('/ServerRuntimes/' + servidor.getName())
            #ls()
            print servidor.getName() + ': ' + get('State')
        except WLSTException,e:
            servidoresAlerta.append(servidor)
    if len(servidoresAlerta) > 0 :
        print 'ALERTA == ALERTA == ALERTA == ALERTA == ALERTA == ALERTA =='
        print 'Os seguintes servidores estão inacessíveis para monitoração, favor checar!'
        for servidor in servidoresAlerta :
            print servidor.getName()
            
#faz checagem de mem�ria nos servidores do dom�nio especificado.
def listaConfiguracoesMemoriaServidoresDomino():
    servidoresComBaixoHeapMemoria = []
    for servidor in servidores:
        try:
            cd("domainRuntime:/ServerRuntimes/" + servidor.getName() + "/JVMRuntime/" +servidor.getName())
            heapSizeMax = cmo.getHeapSizeMax()/1048576
            heapMemoriaLivre = cmo.getHeapFreeCurrent()/1048576
            heapMemoriaLivrePercentagem = cmo.getHeapFreePercent()
            #adiciona na lista de servidores com pouca memoria se servidor tiver menos de 2% de mem�ria livre
            if heapMemoriaLivrePercentagem < 2 :
                servidoresComBaixoHeapMemoria.append(servidor)
            #memoriaMB = memoria/1048576 #transforma os bytes em MB para mostrar
            print '\n================================================================='
            print "O servidor " + servidor.getName() + " esta com :"
            print 'Memoria total alocada(MB): ' + str(heapSizeMax)
            print 'Memoria total disponivel(MB): ' + str(heapMemoriaLivre)
            print 'Memoria livre(%): ' + str(heapMemoriaLivrePercentagem)
        except WLSTException,e:
            print 'AVISO: O servidor ' + servidor.getName() + ' nao esta acessivel atraves do admin server'
    #faz novo teste de heap de mem�ria e caso continuem com pouca mem�ria dispon�vel, mostra ALERTA para observa��o do servidor.
    for servidor in servidoresComBaixoHeapMemoria :
        try:
            cd("domainRuntime:/ServerRuntimes/" + servidor.getName() + "/JVMRuntime/" +servidor.getName())
        except WLSTException,e:
            print 'AVISO: O servidor ' + servidor.getName() + ' nao esta acessivel atraves do admin server'
            heapMemoriaLivrePercentagem = cmo.getHeapFreePercent()
            #adiciona na lista de servidores com pouca memoria se servidor tiver menos de 2% de mem�ria livre
            if heapMemoriaLivrePercentagem < 2 :
                print 'ALERTA == ALERTA == ALERTA == ALERTA == ALERTA == ALERTA =='
                print 'O servidor ' + servidor.getName() + ' est� com heap de mem�ria < que 2% e deve ser observado!'

#faz checagem de threads dos servidores do dom�nio
def checaThreadsServidoresDominio() :
    servidoresComThreadsProblematicas = []
    for servidor in servidores :
        try:
            cd("domainRuntime:/ServerRuntimes/" + servidor.getName() + "/ServerChannelRuntimes/DefaultSecure[https]")
            numeroConexoes = cmo.getConnectionsCount()
            print '==============================================='
            print 'Dados do servidor ' + servidor.getName() + ': '
            print 'Conexoes https: ' + str(numeroConexoes)
            
            cd('domainRuntime:/ServerRuntimes/' + servidor.getName() + '/ExecuteQueueRuntimes/weblogic.socket.Muxer')
            fila = cmo.getPendingRequestCurrentCount()
            print 'Requisicoes de usuarios pendentes: ' + str(fila)
            
            cd('domainRuntime:/ServerRuntimes/' + servidor.getName() + '/ThreadPoolRuntime/ThreadPoolRuntime')
            hoggingThread = cmo.getHoggingThreadCount()
            print 'Quantidade de threads com status hogging: ' + str(hoggingThread)
            print '===============================================\n'
            
        except WLSTException,e:
           print 'Erro servidor nao acessivel para ServerRuntimes ==>> ' + servidor.getName()

#faz health check nos pools de conexao do ambiente.
def checaPoolsConexoes() :
    domainConfig()
    #recupera lista de pools de conexões configuradas no domínio.
    connectionPools = cmo.getJDBCSystemResources()
    for pool in connectionPools : 
        print pool.getName()
        cd('domainConfig:/JDBCSystemResources/' +pool.getName()+ '/JDBCResource/' +pool.getName()+ '/JDBCConnectionPoolParams/' + pool.getName())
        print '==============================================='
        print 'Dados do pool: ' + pool.getName()
        capacidadeInicialPool = cmo.getInitialCapacity()
        capacidadeMaximaPool = cmo.getMaxCapacity()
        print 'Capacidade maxima do pool: ' + str(capacidadeMaximaPool)
        cd('domainConfig:/JDBCSystemResources/' + pool.getName())
        targetServers = cmo.getTargets()
        print 'targets do pool'
        for targetServer in targetServers :
            print targetServer.getName()
        
#        cd('domainRuntime:/ServerRuntimes/server-aapj/JDBCServiceRuntime/server-aapj/JDBCDataSourceRuntimeMBeans/AAPJ')

#=================FIM DEFINICAO DE FUNCOES======================
propriedades = carregaArquivoPropriedades('config.properties')

username = propriedades.get('username')
password = propriedades.get('password')
url = propriedades.get('url')

connect(username, password, url)

#lista para armazenar servidores n�o acess�veis atrav�s do admin server.
servidoresNaoAcessiveis = []

servidores = getServidoresDominio()

mostraStatusServidores(servidores)

listaConfiguracoesMemoriaServidoresDomino()

checaThreadsServidoresDominio()

checaPoolsConexoes()

disconnect()

exit()
