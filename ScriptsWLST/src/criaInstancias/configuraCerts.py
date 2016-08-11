from java.util     import Properties
from java.io     import FileInputStream
from java.io     import File
from java.util     import Enumeration
from string import split
#funcao que carrega dados de arquivo de propriedades
def carregaArquivoPropriedades(nomeArquivo) :
    print 'carregando propriedades do arquivo: ' + nomeArquivo
    #arquivo de propriedades a ser carregado
    localizacaoArquivoPropriedadesConfiguracao = nomeArquivo    
    myProps = Properties()
    #carrega arquivo de propriedades
    myProps.load(FileInputStream(File(localizacaoArquivoPropriedadesConfiguracao)))
    return myProps

#conecta no admin server e iniciliza editor do dominio para possibilitar as alteracoes.        
def conectaAdminIniciaEditor(myProps):
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
    
#varre todos os elementos do properties e separa os que tem prefixo SERVIDOR
def recuperaServidores (propriedades):
    propertyNames = propriedades.propertyNames()
    #armazena os servidores
    servidores = []
    while propertyNames.hasMoreElements():
        #carrega os nomes de todas as chaves carregadas do arquivo de propriedades
        chave = propertyNames.nextElement()
        #recupera tipo da chave para verificar se é um servidor se for adiciona no array de servidores.
        elemento = split(chave, '_')
        #checa se elemento carregado do arquivo de properties é um servidor 
        #e adiciona na lista de servidores ja no grupo especifico
        if elemento[0] == 'SERVIDOR':
            servidores.append(chave)
    print 'A seguinte lista de servidores será configurada aguarde....'
    for srv in servidores:
        print 'Nome do servidor ==>> ' + propriedades.get(srv)
    return servidores

#funcao que efetivamente configura todos os servidores da lista para utilizarem o certificado desejado.
def configuraCertificados(servidores, props):
    for servidor in servidores:
        nomeServidor = props.get(servidor)
        cd('/')
        cd('Servers/' + nomeServidor)
        cmo.setKeyStores('CustomIdentityAndJavaStandardTrust')
        cmo.setCustomIdentityKeyStoreFileName('/var/weblogic/domains/aapf/www2.p12')
        cmo.setCustomIdentityKeyStoreType('PKCS12')
        setEncrypted('CustomIdentityKeyStorePassPhrase', 'CustomIdentityKeyStorePassPhrase_1258638606062', 'Script1258638545621Config', 'Script1258638545621Secret')
        setEncrypted('JavaStandardTrustKeyStorePassPhrase', 'JavaStandardTrustKeyStorePassPhrase_1258638606118', 'Script1258638545621Config', 'Script1258638545621Secret')
        cd('/Servers/' +nomeServidor+ '/SSL/' + nomeServidor)
        cmo.setExportKeyLifespan(500)
        cmo.setUseServerCerts(false)
        cmo.setSSLRejectionLoggingEnabled(true)
        cmo.setAllowUnencryptedNullCipher(false)
        cmo.setInboundCertificateValidation('BuiltinSSLValidationOnly')
        cmo.setOutboundCertificateValidation('BuiltinSSLValidationOnly')
        cmo.setHostnameVerificationIgnored(true)
        cmo.setHostnameVerifier(None)
        cmo.setTwoWaySSLEnabled(false)
        cmo.setClientCertificateEnforced(false)
        cmo.setServerPrivateKeyAlias('server-cert')
        setEncrypted('ServerPrivateKeyPassPhrase', 'ServerPrivateKeyPassPhrase_1258638648555', 'Script1258638545621Config', 'Script1258638545621Secret')


#fim funcoes início execucao script
props=carregaArquivoPropriedades('servidores.properties')
conectaAdminIniciaEditor(props)
servidores=recuperaServidores(props)
configuraCertificados(servidores, props)
activate()

