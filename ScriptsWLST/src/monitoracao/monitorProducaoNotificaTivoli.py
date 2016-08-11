from java.util     import Properties
from java.io     import FileInputStream
from java.io     import File
from java.util     import Enumeration

from string import split
import os
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
    #recupera tipo da chave para verificar se é um servidor se for adiciona no array de servidores.
    elemento = split(chave, '_')
    #checa se elemento carregado do arquivo de properties é um servidor e adiciona na lista de servidores
    if elemento[0] == 'SERVIDOR':
        servidores.append(chave)
        
print 'A seguinte lista de servidores será monitorada....'
for a in servidores:
    print 'Nome do servidor ==>> ' + myProps.get(a)
#====FIM SEPARA ELEMENTOS SERVIDOR DA LISTA DE PROPRIEDADES CARREGADA==============
#==========================CRIACAO DE INSTANCIAS===================================
print 'Iniciando monitoracao dos servidores........'


portaHttp = myProps.get('PORTA_HTTP_SERVIDORES')
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
            connect(usuario, senha, 't3://' + ipServidor + ':' + portaHttp)
            serverRuntime()
            
            #chama funcao de monitoramento do pool de conexoes deste servidor.
            monitoraPoolsConexao(nomeServidor)
            
            print ('Conectou com sucesso no servidor ==>> ' + nomeServidor + ' O channel http deste servidor está ok, o check CheckWeblogicHealthError do Tivoli está ok')
            disconnect()
            print('\n\n\n===============================TERMINANDO MONITORAMENTO SERVIDOR ==>> ' + nomeServidor + '==============================')
            print('=====================================VOU ENVIAR MENSAGEM HARMLESS PARA O TIVOLI==============================')
            os.system("./chamadaTivoli.sh " + "HARMLESS " + "ACESSO_SERVIDOR_OK " + nomeServidor + " CheckWeblogicHealthError" )
        except:
            print('Erro ao tentar conectar com o servidor ' + nomeServidor + ' erro 1 vou tentar novamente...')
            try:
                connect(usuario, senha, 't3://' + ipServidor + ':' + portaHttp)
                serverRuntime()
                print ('Conectou com sucesso no servidor ==>> ' + nomeServidor + ' O channel http deste servidor está ok, o check CheckWeblogicHealthError do Tivoli está ok')
                os.system("./chamadaTivoli.sh " + "HARMLESS " + "ACESSO_SERVIDOR_OK " + nomeServidor + " CheckWeblogicHealthError" )
                disconnect()
            except:
                print('Segundo erro ao tentar conectar com o servidor ==>> ' + nomeServidor + ' erro 2 vou tentar mais uma vez...')
                try:
                    connect(usuario, senha, 't3://' + ipServidor + ':' + portaHttp)
                    serverRuntime()
                    print ('Conectou com sucesso no servidor ==>> ' + nomeServidor + ' O channel http deste servidor está ok, o check CheckWeblogicHealthError do Tivoli está ok')
                    os.system("./chamadaTivoli.sh " + "HARMLESS " + "ACESSO_SERVIDOR_OK " + nomeServidor + " CheckWeblogicHealthError" )
                    disconnect()
                except:
                    print('Terceiro erro ao tentar conectar com o servidor ==>> ' + nomeServidor + ' erro 3 vou notificar o tivoli...')
                    os.system("./chamadaTivoli.sh " + "CRITICAL " + "ERRO_ACESSO_SERVIDOR " + nomeServidor + " CheckWeblogicHealthError" )


def monitoraPoolsConexao(nomeServidor) :
    try:
        print('Iniciando monitoracao de pool de conexoes...')
        cd('serverRuntime:/JDBCServiceRuntime/' + nomeServidor + '/JDBCDataSourceRuntimeMBeans/')
        poolsConexao = ls();
        for jdbcname in poolsConexao.split():
            if jdbcname != 'dr--':
                cd('serverRuntime:/JDBCServiceRuntime/' + nomeServidor + '/JDBCDataSourceRuntimeMBeans/' + jdbcname)
                statusPool = cmo.getState()
                print 'Connection pool ' + jdbcname + ' is ' + statusPool
                if statusPool != 'Running' :
                    print('Enviando critical de pool de conexoes')
                    os.system("./chamadaTivoli.sh " + "CRITICAL " + "POOL_CONEXOES_ERROR " + nomeServidor + " CheckWeblogicDatabaseConnectionError" )
                else:
                    print('Enviando HARMLESS de pool de conexoes')
                    os.system("./chamadaTivoli.sh " + "HARMLESS " + "POOL_CONEXOES_ERROR " + nomeServidor + " CheckWeblogicDatabaseConnectionError" )
    except:
        print('Erro no monitoramento de pool de conexoes')

monitoraServidores()
exit()
