#
# Imports
#
import odbc

#
# Database instances
#
instances = {}

#
# Configures a database
#
def set(name, str):
	if name in instances:
		return False
	instances[name] = str
		
#
# Gets the database instance
#
def get(name):
	if name in instances:
		return odbc.connect(instances[name])
	return False
