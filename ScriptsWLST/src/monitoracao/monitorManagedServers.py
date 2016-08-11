from java.util 	import Properties
from java.io 	import FileInputStream
from java.io 	import File
from java.util 	import Enumeration

from string import split
#============CARREGA DADOS ARQUIVO PROPRIEDADES====================================
#arquivo de propriedades a ser carregado
localizacaoArquivoPropriedadesConfiguracao = 'servidores.properties'

myProps = Properties()

#carrega arquivo de propriedades
myProps.load(FileInputStream(File(localizacaoArquivoPropriedadesConfiguracao)))

#========SEPARA ELEMENTOS SERVIDOR DA LISTA DE PROPRIEDADES CARREGADA==============
#array para armazenar as chaves dos servidores definidos no arquivo de propriedades.
servidores = []

propertyNames = myProps.propertyNames()

while propertyNames.hasMoreElements():
    #carrega os nomes de todas as chaves carregadas do arquivo de propriedades
    chave = propertyNames.nextElement()
    #recupera tipo da chave para verificar se � um servidor se for adiciona no array de servidores.
    elemento = split(chave, '_')
    #checa se elemento carregado do arquivo de properties � um servidor e adiciona na lista de servidores
    if elemento[0] == 'SERVIDOR':
        servidores.append(chave)
        
print 'A seguinte lista de servidores será monitorada....'
for a in servidores:
    print 'Nome do servidor ==>> ' + myProps.get(a)
#====FIM SEPARA ELEMENTOS SERVIDOR DA LISTA DE PROPRIEDADES CARREGADA==============
#==========================CRIACAO DE INSTANCIAS===================================
print 'Iniciando monitoracao dos servidores........'


portaHttps = myProps.get('PORTA_HTTPS_SERVIDORES')
usuario = myProps.get('USUARIO_ADMIN')
senha = myProps.get('SENHA_ADMIN')
parametroTDump = myProps.get('PARAMETRO_THREAD_DUMP')

def monitoraServidores() :
    for servidor in servidores:
        nomeServidor = myProps.get(servidor)
        ipServidor = myProps.get('IP_'+servidor)
        print('\n\n\n===============================INICIANDO MONITORAMENTO SERVIDOR ==>> ' + nomeServidor + '==============================')
        print('=============================================================================================================================')
        try:
            connect(usuario, senha, 't3s://' + ipServidor + ':443')
            serverRuntime()
            print('Checando a memoria...')
            cd('serverRuntime:/JVMRuntime/' + nomeServidor)
            jvmDescription = cmo.getJVMDescription()
            memAlocada = cmo.getHeapSizeCurrent() / 1048576
            porcentagemMemDisponivel = cmo.getHeapFreePercent()
            memDisponivel = cmo.getHeapFreeCurrent()/1048576
            print ('=======INFORMACOES DE JVM==========')
            print('Descricao da  JVM :' + jvmDescription)
            print('Memoria alocada em MB: ' + str(memAlocada))
            print('Percentual de memoria disponivel: ' + str(porcentagemMemDisponivel))
            print('Total de memoria disponivel em MB: ' + str(memDisponivel))
            print('\n')
            
            cd('serverRuntime:/')
            quantidadeSocketsAbertos = cmo.getOpenSocketsCurrentCount();
            print('Quantidade de sockets abertos: ' + str(quantidadeSocketsAbertos));
        
            cd('serverRuntime:/ThreadPoolRuntime/ThreadPoolRuntime/')
            quantidadeRequisicoesAtendidas = cmo.getCompletedRequestCount()
            statusServidor = cmo.getHealthState()
            hoggingThreads = cmo.getHoggingThreadCount()
            totalThreads = cmo.getExecuteThreadTotalCount()
            threadsLivres = cmo.getExecuteThreadIdleCount()
            requisicoesPendentes = cmo.getPendingUserRequestCount()
            tamanhoFila = cmo.getQueueLength()
            requisicoesPorSegundo = cmo.getThroughput()
            if(hoggingThreads > int(parametroTDump)) :
                threadDump(writeToFile='true', fileName='ThreadDump_' + nomeServidor + '.txt')
            print('========INFORMACOES DE THREADS======')
            print('Status do servidor: ' + str(statusServidor))
            print('Total de requisicoes de usuarios atendidas: ' + str(quantidadeRequisicoesAtendidas))
            print('Total de threads no servidor: ' + str(totalThreads))
            print('Total de threads livres: ' + str(threadsLivres))
            print('Total de threads com delay na resposta: ' + str(hoggingThreads))
            print('Total de requisicoes de usuarios pendentes: ' + str(requisicoesPendentes))
            print('Tamanho da fila aguardando por threads: ' + str(tamanhoFila))
            print('Media de requisicoes por segundo(Throughput): ' +str(requisicoesPorSegundo))
            disconnect()
            print('\n\n\n===============================TERMINANDO MONITORAMENTO SERVIDOR ==>> ' + nomeServidor + '==============================')
            print('==============================================================================================================================')
            print('==============================================================================================================================')
        except:
            print('Erro ao tirar estat�sticas do servidor + ' + nomeServidor + ' ignorando este servidor, indo para o pr�ximo!!!!');

monitoraServidores()
exit()
