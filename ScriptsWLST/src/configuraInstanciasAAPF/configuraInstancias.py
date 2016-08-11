from java.util 	import Properties
from java.io 	import FileInputStream
from java.io 	import File
from java.util 	import Enumeration

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


myProps = carregaArquivoPropriedades('servidores.properties')

admin = myProps.get('USUARIO_ADMIN')
senha = myProps.get('SENHA_ADMIN')
adminurl = 't3://' + myProps.get('IP_ADMIN_SERVER') + ':' + myProps.get('PORTA_HTTP_ADMIN_SERVER')
print 'conectando no admin server...'
print 'URL Admin server ==>> ' + adminurl
# Conecta com Admin server do domínio
connect(admin, senha, adminurl)

servidores = getServidoresDominio()

#inicia configuração do domínio
edit()
startEdit()

#=======CONFIGURA JAVA_OPTIONS DOS SEVIDORES=======================================
args = myProps.get('JAVA_ARGS')
beaHome = myProps.get('BEA_HOME')
classpath = myProps.get('CLASSPATH')
javaHome = myProps.get('JAVA_HOME')
javaVendor = myProps.get('JAVA_VENDOR')

for servidor in servidores:
    nomeServidor = servidor.getName()
    if nomeServidor != 'AdminServer' :
        cd('/')
        cd('Servers/' + nomeServidor + '/ServerStart/' + nomeServidor)
        cmo.setBeaHome(beaHome)
        cmo.setClassPath(classpath)
        cmo.setJavaHome(javaHome)
        cmo.setJavaVendor(javaVendor)
        cmo.setUsername(admin)
        cmo.setPassword(senha)
#=====FIM CONFIGURA JAVA_OPTIONS DOS SERVIDORES====================================

#ativa configurações e sai
activate()