#===========================INÍCIO DAS VARIÁVEIS EDITÁVEIS=======================
adminurl = 't3://localhost:7001'
username = 'weblogic'
password = 'npassaqui'
initialCapacity = 80
maxCapacity = 80
capacityIncrement = 80
driverName = 'com.ibm.db2.jcc.DB2Driver'
driverUsername = 'AOPDB2'
portNumber='446'
dataBaseName='BRDB2P1' 


serverName1='172.17.216.140'
serverName2='172.17.216.141'
driverURL1 = 'jdbc:db2://172.17.216.140:446/BRDB2P1'
driverURL2 = 'jdbc:db2://172.17.216.141:446/BRDB2P1'
dsName1 = 'DB2Pool_1'
dsName2 = 'DB2Pool_2'


#============================FIM DAS VARIÁVEIS EDITÁVEIS=========================

print 'Iniciando a criação dos Pools, certifique-se que o Admin server do dominio na url ===>>> ' + adminurl + ' esteja rodando'

# Conecta com Admin server do domínio
connect(username, password, adminurl)

# Verifica se o DataSource já existe 
try:
	cd('/JDBCSystemResources/' + dsName1)
	print 'O Data Source ' + dsName1 + ' já existe.'
	exit()
except WLSTException:
	pass

print 'Criando um novo Data Source chamado ' + dsName1 + '.'
edit()
startEdit()
cd('/')

# Cria o Data Source
jdbcSystemResource = create(dsName1, 'JDBCSystemResource')
jdbcResource = jdbcSystemResource.getJDBCResource()
jdbcResource.setName(dsName1)

# Coloca o jndi name igual ao nome do Data Source pois vai utilizar o Multipool.
jdbcResourceParameters = jdbcResource.getJDBCDataSourceParams()
jdbcResourceParameters.setJNDINames([dsName1])

# Cria o Connection Pool
connectionPool = jdbcResource.getJDBCConnectionPoolParams()
connectionPool.setInitialCapacity(initialCapacity)
connectionPool.setMaxCapacity(maxCapacity)
connectionPool.setCapacityIncrement(capacityIncrement)
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
driver.setDriverName(driverName)
driver.setUrl(driverURL1)
driverProperties = driver.getProperties()
userProperty = driverProperties.createProperty('user')
userProperty.setValue(driverUsername)
userProperty1 = driverProperties.createProperty('portNumber')
userProperty1.setValue(portNumber)
userProperty2 = driverProperties.createProperty('dataBaseName')
userProperty2.setValue(dataBaseName)
userProperty3 = driverProperties.createProperty('serverName')
userProperty3.setValue(serverName1)




# Ativa as modificações no domínio
save()
activate(block='true')
print 'Data Source criado com sucesso.'

####==============Datasource 2 =============

# Verifica se o DataSource já existe 
try:
	cd('/JDBCSystemResources/' + dsName2)
	print 'O Data Source ' + dsName2 + ' já existe.'
	exit()
except WLSTException:
	pass

print 'Criando um novo Data Source chamado ' + dsName2 + '.'
edit()
startEdit()
cd('/')

# Cria o Data Source
jdbcSystemResource = create(dsName2, 'JDBCSystemResource')
jdbcResource = jdbcSystemResource.getJDBCResource()
jdbcResource.setName(dsName2)

# Coloca o jndi name igual ao nome do Data Source pois vai utilizar o Multipool.
jdbcResourceParameters = jdbcResource.getJDBCDataSourceParams()
jdbcResourceParameters.setJNDINames([dsName2])

# Cria o Connection Pool
connectionPool = jdbcResource.getJDBCConnectionPoolParams()
connectionPool.setInitialCapacity(initialCapacity)
connectionPool.setMaxCapacity(maxCapacity)
connectionPool.setCapacityIncrement(capacityIncrement)
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
driver.setDriverName(driverName)
driver.setUrl(driverURL2)
driverProperties = driver.getProperties()
userProperty = driverProperties.createProperty('user')
userProperty.setValue(driverUsername)
userProperty1 = driverProperties.createProperty('portNumber')
userProperty1.setValue(portNumber)
userProperty2 = driverProperties.createProperty('dataBaseName')
userProperty2.setValue(dataBaseName)
userProperty3 = driverProperties.createProperty('serverName')
userProperty3.setValue(serverName2)


print 'Data Source criado com sucesso.'
# Ativa as modificações no domínio
save()
activate(block='true')
exit()