BEA_HOME="/home/mmaia/bea"
export BEA_HOME

DOMAIN_HOME=/var/weblogic10/domains/extranet
export DOMAIN_HOME

${BEA_HOME}/jrockit_160_05/bin/java -cp ${BEA_HOME}/wlserver_10.3/server/lib/weblogic.jar weblogic.WLST paraInstancias.py

${BEA_HOME}/jrockit_160_05/bin/java -cp ${BEA_HOME}/wlserver_10.3/server/lib/weblogic.jar weblogic.WLST inicializaInstancias.py