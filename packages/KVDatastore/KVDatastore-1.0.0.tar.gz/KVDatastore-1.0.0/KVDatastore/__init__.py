
############-----------Imports-----------###############


import threading
import time
import json
import os



class KVDatastore(dict):
    

    def __init__(self):
        self._ttl = 360               # ttl is time to live property for each keys. Default value is 360 sec
        self.lock = threading.Lock() # threading locks are initialised to avoid clashing in storing data while using multiple threading

        
        self.__map = {}              # temporary map dict is used to store keys with time stamp to achieve ttl


        
    def _collect(self,key):
        # private method to delete expired keys from user object on every 1 second
        
        while True:
            now = time.time()
            val = self.__map[key]
            diff = now - val
            if diff>self._ttl:
                # if the ttl is exceeded then the key is deleted from the current object and map dict
                try:
                    
                    del self[key]
                    del self.__map[key]
                    break
                except:
                    break
            time.sleep(1)      

    def _write(self,data):
        # private method to write data to a json file created
        self.lock.acquire()
        with open(self.loc+self.filename, "w") as d:
            
            json.dump(data,d,indent=6)
            d.close()
        self.lock.release()           
        
    def initdatastore(self,location="datastore"):

        #method to initialize datastore with empty json file
        
        try :
            self.loc=location.strip("\/ ")
            self.filename='\keyvaluedatastore'+'.json'
            os.mkdir(self.loc)
            data={}
            with open(self.loc+self.filename,"w") as f:
                json.dump(data,f)
                f.close()
            path = os.getcwd() +"\ "+ self.loc    
            print("The new key-value datastore is created on the path >>>> ",path+ self.filename)       
        except FileExistsError as err:
            print('You are in the default datastore which is already created --->>> '+ self.loc +self.filename +' <<<--- \n')
            
            
    
    
    


    def create(self, key:str, value):
        # Create method to create a key-value pair in json file         
        size = os.path.getsize(self.loc+self.filename)
        if size<=1000000000:                            # this ensures the file should not be more than 1GB
            
            with open(self.loc+self.filename) as f:
                self.lock.acquire()
                data=json.load(f)
                keys=data.keys()
                f.close()
                self.lock.release()
                
                if key in keys:                         # If key already exists, appropriate error message is displayed
                    print("Sorry, key already exists")
                    
                    
                else:
                    self.__map[key] = time.time()       # current time is stamped as a value in map dict
                    dict.__setitem__(self, key, value)

                    self._t = threading.Thread(target=self._collect,args=(key,))
                    self._t.start()
                    
                    data[key]=value
                    self._write(data)
                    
        else:
            print('File size limit exceeded')
             
    def read(self, key):
        # Read method used to read the available key that is not expired
        try:
            
            val = dict.__getitem__(self, key)
            print( val)
        except KeyError as err:
            print('key does not esists ---> ',err)

    
    def delete(self,key):
        # Delete method to delete the available key that is not expired
        try:
            
            if self[key]:
                del self[key]
                self.lock.acquire()
                with open(self.loc+self.filename) as f:
                    data=json.load(f)
                
                    del data[key]
                    f.close()
                self.lock.release()
               
                self._write(data)
        except KeyError:
            print('Key does not exists')
    def close(self):
        # Close method terminates the thread and clear the items in the object 
        self.clear()
        self.__map.clear()
        print("Datastore closed") 




        
        
            
        
    
    


