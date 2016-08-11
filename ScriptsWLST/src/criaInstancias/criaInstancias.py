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

readDomain(myProps.get('DIRETORIO_DOMINIO'))

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
        
print 'A seguinte lista de servidores será criada e configurada aguarde....'
for a in servidores:
    print 'Nome do servidor ==>> ' + myProps.get(a)
#====FIM SEPARA ELEMENTOS SERVIDOR DA LISTA DE PROPRIEDADES CARREGADA==============
#==========================CRIACAO DE INSTANCIAS===================================
print 'Iniciando configuração dos servidores, criando os servidores........'

portaHttp = myProps.get('PORTA_HTTP_SERVIDORES')
portaHttps = myProps.get('PORTA_HTTPS_SERVIDORES')
portaHttpHabilitada = myProps.get('PORTA_HTTP_HABILITADA')
portaHttpsHabilitada = myProps.get('PORTA_HTTPS_HABILITADA')
print 'porta http habilitada? ' + portaHttpHabilitada + ' porta https habilitada? ' + portaHttpsHabilitada
cd('/')
#garante que os servidores estarão em modo de produção neste domínio!
set('ProductionModeEnabled', 'true')

for servidor in servidores:
    nomeServidor = myProps.get(servidor)
    ipServidor = myProps.get('IP_'+servidor)
    cd('/')
    create(nomeServidor, 'Server')
    cd('Server/' + nomeServidor)
    set('ListenPort', int(portaHttp))
    set('ListenAddress', ipServidor)
    set('ListenPortEnabled', portaHttpHabilitada)
    if portaHttpsHabilitada == 'true':
        print 'porta ssl deve ser habilitada, configurando... porta ssl ' + portaHttps
        create(nomeServidor,'SSL')
        cd('SSL/' + nomeServidor)
        set('Enabled', 'True')
        set('ListenPort', int(portaHttps))
    print 'Servidor ==>> ' + nomeServidor + ' criado com sucesso!\n'


print 'Servidores criados com sucesso!'
#========================FIM CRIACAO DE INSTANCIAS=================================
#=======================
# Atualiza domínio e sai
#=======================
updateDomain()
closeDomain()
exit()
