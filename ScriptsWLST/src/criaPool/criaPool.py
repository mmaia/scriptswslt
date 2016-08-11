from java.util 	import Properties
from java.io 	import FileInputStream
from java.io 	import File
from java.util 	import Enumeration

from string import split
#============CARREGA DADOS ARQUIVO PROPRIEDADES====================================
#arquivo de propriedades a ser carregado
localizacaoArquivoPropriedadesConfiguracao = 'pool.properties'

myProps = Properties()

#carrega arquivo de propriedades
myProps.load(FileInputStream(File(localizacaoArquivoPropriedadesConfiguracao)))


admin = myProps.get('USUARIO_ADMIN')
senha = myProps.get('SENHA_ADMIN')
adminurl = 't3://' + myProps.get('IP_ADMIN_SERVER') + ':' + myProps.get('PORTA_HTTP_ADMIN_SERVER')

nomePool=myProps.get('NOME_POOL')
senhaPool=myProps.get('SENHA_POOL')
nomeJNDI=myProps.get('NOME_JNDI')
capacidadeInicial=myProps.get('CAPACIDADE_INICIAL_POOL')
capacidadeMaxima=myProps.get('CAPACIDADE_MAXIMA_POOL')
capacidadeIncremento=myProps.get('CAPACIDADE_INCREMENTO_POOL')
nomeDriver=myProps.get('NOME_DRIVER')
urlDB=myProps.get('URL_DB')
usuarioDB=myProps.get('USUARIO_DB')
portaDB=myProps.get('PORTA_DB')
nomeDB=myProps.get('NOME_DB')
urlServidorDB=myProps.get('URL_SERVIDOR_DB')

#========FIM CARREGA DADOS ARQUIVO PROPRIEDADES====================================

print 'conectando no admin server...'
print 'URL Admin server ==>> ' + adminurl
# Conecta com Admin server do domínio
connect(admin, senha, adminurl)

# Verifica se o DataSource já existe 
try:
	cd('/JDBCSystemResources/' + nomePool)
	print 'O Data Source ' + nomePool + ' já existe.'
	exit()
except WLSTException:
	pass

print 'Criando um novo Data Source chamado ' + nomePool + '.'



#inicia configuração do domínio
edit()
startEdit()
cd('/')

# Cria o Data Source
jdbcSystemResource = create(nomePool, 'JDBCSystemResource')
jdbcResource = jdbcSystemResource.getJDBCResource()
jdbcResource.setName(nomePool)

# Coloca o jndi name igual ao nome do Data Source pois vai utilizar o Multipool.
jdbcResourceParameters = jdbcResource.getJDBCDataSourceParams()
jdbcResourceParameters.setJNDINames([nomeJNDI])

# Cria o Connection Pool
connectionPool = jdbcResource.getJDBCConnectionPoolParams()
connectionPool.setInitialCapacity(int(capacidadeInicial))
connectionPool.setMaxCapacity(int(capacidadeMaxima))
connectionPool.setCapacityIncrement(int(capacidadeIncremento))
connectionPool.setTestConnectionsOnReserve(true)
connectionPool.setTestFrequencySeconds(300)
connectionPool.setStatementCacheSize(500)
connectionPool.setStatementCacheType('LRU')
connectionPool.setTestTableName('SQL select 1+1 from SYSIBM.SYSDUMMY1')
connectionPool.setSecondsToTrustAnIdlePoolConnection(300)
connectionPool.setInactiveConnectionTimeoutSeconds(300)
connectionPool.setHighestNumWaiters(5000)
connectionPool.setConnectionReserveTimeoutSeconds(30)
connectionPool.setStatementTimeout(120)


# Configura parâmetros do Driver
driver = jdbcResource.getJDBCDriverParams()
driver.setDriverName(nomeDriver)
driver.setUrl(urlDB)
driverProperties = driver.getProperties()
userProperty = driverProperties.createProperty('user')
userProperty.setValue(usuarioDB)
userProperty1 = driverProperties.createProperty('portNumber')
userProperty1.setValue(portaDB)
userProperty2 = driverProperties.createProperty('dataBaseName')
userProperty2.setValue(nomeDB)
userProperty3 = driverProperties.createProperty('serverName')
userProperty3.setValue(urlServidorDB)




# Ativa as modificações no domínio
save()
activate(block='true')
print 'Data Source criado com sucesso.'