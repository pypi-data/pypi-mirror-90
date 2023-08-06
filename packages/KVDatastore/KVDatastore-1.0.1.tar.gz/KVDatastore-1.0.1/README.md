=================  File based Key Value Datastore   =======================



This is a simple Key value datastore that supports CRD operations(Create, Read, Delete). 
This datastore creates a datastore in your local machine.
Since it is a package, you can initialize by following steps.

	=> open your terminal, run pip install KVDatastore
	=> now open your python, run following code.
	
>>> from KVDatastore import *
>>> object=KVDatastore()
	
	This imports all methods to your code and creates instance of the class

	=> The methods available are,
		--> initdatastore(location)
		--> create(key,value)	
		--> read(key)
		--> delete(key)