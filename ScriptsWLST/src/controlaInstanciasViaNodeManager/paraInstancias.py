from java.util     import Properties
from java.io     import FileInputStream
from java.io     import File

#import thread
from string import split

#============DEFINICAO DE FUNCOES============
#funcao que carrega dados de arquivo de propriedades
def carregaArquivoPropriedades(nomeArquivo) :
    print 'carregando propriedades do arquivo: ' + nomeArquivo
    #arquivo de propriedades a ser carregado 
    myProps = Properties()
    #carrega arquivo de propriedades
    myProps.load(FileInputStream(File(nomeArquivo)))
    return myProps


def listaServidores(arquivoPropriedades):
    print 'selecionando servidores da lista de propriedades'
    servidores = []
    propriedades = arquivoPropriedades.propertyNames()
    while propriedades.hasMoreElements():
        #carrega os nomes de todas as chaves carregadas do arquivo de propriedades
        chave = propriedades.nextElement()
        #recupera tipo da chave para verificar se um servidor se for adiciona no array de servidores.
        elemento = split(chave, '_')
        #checa se elemento carregado do arquivo de properties  um servidor e adiciona na lista de servidores
        if elemento[0] == 'SERVIDOR':
            servidores.append(chave)
    #while que imprime lista de servidores recuperada
    print '=======================AVISO================================================================'
    print'LISTA DOS SERVIDORES A SEREM PARADOS'
    for servidor in servidores:
        print 'Servidor ==>> ' + arquivoPropriedades.get(servidor)
    print '=======================AVISO================================================================'
    return servidores
            
    
def paraInstancias():
    usuario = arquivoPropriedades.get('USUARIO_ADM')
    senha = arquivoPropriedades.get('USUARIO_ADM_SENHA')
    ipNodeManager = arquivoPropriedades.get('NODEMANAGER_IP')
    portaNodeManager = arquivoPropriedades.get('NODEMANAGER_PORT')
    nomeDominio = arquivoPropriedades.get('DOMINIO_NOME')
    diretorioDominio = arquivoPropriedades.get('DOMINIO_DIRETORIO')
    print '\n================================================================================================'
    print 'tentando conexao com o nodemanager...'
    print 'usuario: ' + usuario
    print 'ip Node Manager: ' + ipNodeManager
    print 'porta Node Manager: ' + portaNodeManager
    print 'Nome do dominio: ' + nomeDominio
    print 'Diretorio do dominio no servidor: ' + diretorioDominio
    print '================================================================================================'
    nmConnect(usuario,senha, ipNodeManager, portaNodeManager, nomeDominio, diretorioDominio, 'plain', 'true')
    for servidor in servidores:
        try:
            nmKill(arquivoPropriedades.get(servidor))
        except:
            print 'Erro ao tentar parar o servidor ' + arquivoPropriedades.get(servidor) + 'provavelmente este servidor já encontra-se parado'
#==========execucao (Main)========

arquivoPropriedades = carregaArquivoPropriedades('servidores.properties')

servidores = listaServidores(arquivoPropriedades)

paraInstancias()