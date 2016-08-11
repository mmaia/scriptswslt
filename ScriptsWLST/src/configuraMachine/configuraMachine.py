from java.util     import Properties
from java.io     import FileInputStream
from java.io     import File
from java.util     import Enumeration

from string import split


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
    print 'A seguinte lista de servidores sera configurada aguarde....'
    for srv in servidores:
        print 'Nome do servidor ==>> ' + propriedades.get(srv)
    return servidores

#funcao que efetivamente configura os servidores setando a machine
def configuraServidores(servidores, propriedades):
    machine = propriedades.get('MACHINE')
    print 'nome da machine ' + machine
    
    for servidor in servidores:
        nomeServidor = propriedades.get(servidor)
        cd('/')
        cd('/Servers/' + nomeServidor)
        cmo.setMachine(getMBean('/Machines/' + machine))

#ativa configurações e sai
def ativaConfiguracoesTerminaEditor ():
    activate()
    exit()
    
#======================= FIM DEFINICAO DE FUNCOES ============================================================================================


propriedades = carregaArquivoPropriedades('servidores.properties')
conectaAdminIniciaEditor(propriedades)
servidores = recuperaServidores(propriedades)
configuraServidores(servidores, propriedades)
ativaConfiguracoesTerminaEditor()



