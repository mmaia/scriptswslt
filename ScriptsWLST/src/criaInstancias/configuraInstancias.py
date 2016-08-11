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

#========FIM CARREGA DADOS ARQUIVO PROPRIEDADES====================================
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
        
print 'A seguinte lista de servidores será configurada aguarde....'
for a in servidores:
    print 'Nome do servidor ==>> ' + myProps.get(a)
#====FIM SEPARA ELEMENTOS SERVIDOR DA LISTA DE PROPRIEDADES CARREGADA==============

admin = myProps.get('USUARIO_ADMIN')
senha = myProps.get('SENHA_ADMIN')
adminurl = 't3://' + myProps.get('IP_ADMIN_SERVER') + ':' + myProps.get('PORTA_HTTP_ADMIN_SERVER')
print 'conectando no admin server...'
print 'URL Admin server ==>> ' + adminurl
# Conecta com Admin server do domínio
connect(admin, senha, adminurl)
#inicia configuração do domínio
edit()
startEdit()
#=======CONFIGURA LOGS DOS SERVIDORES==============================================

dirLogs=myProps.get('DIRETORIO_LOG')
for servidor in servidores:
    nomeServidor = myProps.get(servidor)
    cd('/')
    cd('Servers/' + nomeServidor + '/Log/' + nomeServidor)
    cmo.setFileName(dirLogs + '/' + nomeServidor + '/server.log')
    cmo.setRotationType('byTime')
    cmo.setFileTimeSpan(6)
    cd('/')
    cd('Servers/' + nomeServidor + '/WebServer/' + nomeServidor + '/WebServerLog/' + nomeServidor)
    cmo.setFileName(dirLogs + '/' + nomeServidor + '/access.log')
    cmo.setRotationType('byTime')
    cmo.setFileTimeSpan(6)
    print 'LOG DO SERVIDOR '+nomeServidor+' CONFIGURADO\n\n'
#=====FIM CONFIGURA LOGS DOS SERVIDORES============================================

#=======CONFIGURA JAVA_OPTIONS DOS SEVIDORES=======================================
args = myProps.get('JAVA_ARGS')
beaHome = myProps.get('BEA_HOME')
classpath = myProps.get('CLASSPATH')
javaHome = myProps.get('JAVA_HOME')
javaVendor = myProps.get('JAVA_VENDOR')

for servidor in servidores:
    nomeServidor = myProps.get(servidor)
    cd('/')
    cd('Servers/' + nomeServidor + '/ServerStart/' + nomeServidor)
    cmo.setArguments(args)
    cmo.setBeaHome(beaHome)
    cmo.setClassPath(classpath)
    cmo.setJavaHome(javaHome)
    cmo.setJavaVendor(javaVendor)
    cmo.setUsername(admin)
    cmo.setPassword(senha)
#=====FIM CONFIGURA JAVA_OPTIONS DOS SERVIDORES====================================

#ativa configurações e sai
activate()