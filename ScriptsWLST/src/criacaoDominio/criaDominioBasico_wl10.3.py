#============CARREGA DADOS ARQUIVO PROPRIEDADES====================================
from java.util 	import Properties

from java.io 	import FileInputStream

from java.io 	import File

from java.util 	import Enumeration

#arquivo de propriedades a ser carregado
localizacaoArquivoPropriedadesConfiguracao = 'dominio.properties'

myProps = Properties()

#carrega arquivo de propriedades
myProps.load(FileInputStream(File(localizacaoArquivoPropriedadesConfiguracao)))    

#carrega os valores do arquivo de propriedades para variaveis locais para fazer o codigo mais legivel
porta_http=myProps.getProperty('PORTA_HTTP_ADMIN_SERVER')
root_dominio=myProps.getProperty('ROOT_DOMINIO')
nome_dominio=myProps.getProperty('NOME_DOMINIO')
senha=myProps.getProperty('SENHA_ADMIN')
ip=myProps.getProperty('IP_ADMIN_SERVER')
senhaDeployer=myProps.getProperty('SENHA_DEPLOYER')
#=========FIM CARREGA DADOS ARQUIVO PROPRIEDADES====================================


#=================CONFIGURA DOMÍNIO================================================

#Utiliza um template padrão do weblogic 10 como base para criação do domínio.
readTemplate("dominioBB_WL10.3.jar")

#Configura o Admin Server para o domínio.
cd('Servers/AdminServer')
set('ListenAddress',ip)
set('ListenPort', int(porta_http))

#Define a senha para usuário default do weblogic(usuario=wladmin) e usuário deployer(usuario=usrdeploy).
#este usuario é temporário e será apagado o usuário utilizado para este domínio como
#default administrador será o passado no arquivo de propriedades de configuração.
cd('/')
cd('Security/templateDominioBB/User/wladmin')
cmo.setPassword(senha)

cd('/')
cd('Security/templateDominioBB/User/deployer')
cmo.setPassword(senhaDeployer)


#configura o domínio com os valores passados e cria o domínio
setOption('OverwriteDomain', 'true')
writeDomain(root_dominio + '/' + nome_dominio)

#==============FIM CONFIGURA DOMINIO================================================


print('Dominio chamado: ' + nome_dominio + '  criado com sucesso')

#fecha o template e sai do WLST
closeTemplate()
exit()
