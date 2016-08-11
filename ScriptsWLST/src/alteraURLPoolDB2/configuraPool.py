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

def atualizaParametrosPool(nomePool, dataBaseName, portNumber, nomeServidor) :
    try:
        cd('domainConfig:/JDBCSystemResources/'+nomePool+'/Targets')
        ls()
        cd('domainConfig:/JDBCSystemResources/'+nomePool+'/JDBCResource/'+nomePool+'/JDBCDriverParams/'+nomePool)
        print('URL atual do pool: ' + get('Url'))
        
        print '... Iniciando alteracao da configuracao para'
        print('Nova URL: jdbc:db2://' +nomeServidor+':'+portNumber+'/'+dataBaseName)
        #inicia configuração do domínio
        edit()
        startEdit()
        cd('edit:/JDBCSystemResources/'+nomePool)
        jdbcResource = cmo.getJDBCResource()
        # Configura parâmetros do Driver
        driver = jdbcResource.getJDBCDriverParams()
        driver.setUrl('jdbc:db2://' +nomeServidor+':'+portNumber+'/'+dataBaseName)
        cd('edit:/JDBCSystemResources/'+nomePool+'/JDBCResource/'+nomePool+'/JDBCDriverParams/'+nomePool+'/Properties/'+nomePool+'/Properties/dataBaseName')
        print set('Value',dataBaseName)
        cd('edit:/JDBCSystemResources/'+nomePool+'/JDBCResource/'+nomePool+'/JDBCDriverParams/'+nomePool+'/Properties/'+nomePool+'/Properties/portNumber')
        print set('Value',portNumber)
        cd('edit:/JDBCSystemResources/'+nomePool+'/JDBCResource/'+nomePool+'/JDBCDriverParams/'+nomePool+'/Properties/'+nomePool+'/Properties/serverName')
        print set('Value',nomeServidor)
        #ativa configurações e sai
        activate()
    except WLSTException,e:
        print(e)
        print('ALERTA == ALERTA == ALERTA == ALERTA == ALERTA == ALERTA ')
        print 'Erro ao acessar o pool para modificar configuração, favor checar o nome do Pool se esta correto no arquivo de configuracao deste script' 
        
#=============FIM DEFINIÇAO DE FUNCOES==============
propriedades = carregaArquivoPropriedades('config.properties')

username = propriedades.get('username')
password = propriedades.get('password')
url = propriedades.get('url')
nomePool = propriedades.get('nomePool')
dataBaseName = propriedades.get('dataBaseName')
portNumber = propriedades.get('portNumber')
nomeServidor = propriedades.get('nomeServidor')

connect(username, password, url)

atualizaParametrosPool(nomePool, dataBaseName, portNumber, nomeServidor)
       