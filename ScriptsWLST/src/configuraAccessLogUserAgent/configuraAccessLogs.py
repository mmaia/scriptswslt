from java.util     import Properties
from java.io     import FileInputStream
from java.io     import File
from java.util     import Enumeration

#=======================DEFINICAO DE FUNCOES ============================================================================================

#funcao que carrega dados de arquivo de propriedades
def carregaArquivoPropriedades(nomeArquivo) :
    print 'carregando propriedades do arquivo: ' + nomeArquivo
    #arquivo de propriedades a ser carregado
    localizacaoArquivoPropriedadesConfiguracao = nomeArquivo    
    myProps = Properties()
    #carrega arquivo de propriedades
    myProps.load(FileInputStream(File(localizacaoArquivoPropriedadesConfiguracao)))
    return myProps

#conecta no admin server e inicializa editor do dominio para possibilitar as alteracoes.        
def conectaAdminIniciaEditor(myProps):
    admin = myProps.get('username')
    senha = myProps.get('password')
    adminurl = myProps.get('url')
    print 'conectando no admin server...'
    print 'URL Admin server ==>> ' + adminurl
    # Conecta com Admin server do dominio
    connect(admin, senha, adminurl)
    #inicia configuracao do dominio
    edit()
    startEdit()
    
#funcao que retorna lista de todos os servidores configurados para este dominio.
def getServidoresDominio():
    print 'executando funcao getServidoresDominio'
    domainConfig()
    servidores = cmo.getServers()
    return servidores

#faz a configuração do log de acesso dos servidores do dominio omitindo o AdminServer.
def configuraLogAcessoServidores(servidores) :
    for servidor in servidores:
        cd('/')
        cd('edit:/Servers/' + servidor.getName() + '/WebServer/' + servidor.getName() + '/WebServerLog/' + servidor.getName())
        set('LogFileFormat','extended')
        set('ELFFields','c-ip RFC931  auth_user  x-br.com.bb.aapf.accesslog.AAPFCustomAccessLogFormatter')
    print 'Log dos servidores configurados com sucesso nos servidores deste dominio [OK]'
        

#=================fim definicao de funcoes=========================================================
#==================================================================================================
propriedades = carregaArquivoPropriedades('config.properties')
conectaAdminIniciaEditor(propriedades)
servidores = getServidoresDominio()

configuraLogAcessoServidores(servidores)

#ativa configuracoes e sai
activate()
disconnect()

exit()
