import os
from bson.json_util import dumps
from main.config import mongo
import shutil
class Database:
    ''' 
        3 folders are created in memory to capture the db and to be used as a backup
        A = Contains the latest backup
        B = Contains the 1st stale backup
        C = contains the 2nd stale backup

        Each folder containes N files 1 for each collection, where N = number of collections
    '''

    ''' Creates Backup of DB '''
    def copy_db():
        ## get all collections
        db = mongo.get_database('db')
        collections = db.collection_names()
        ## get to /var/www/html/
        dirname = os.path.dirname(os.getcwd())
        os.chdir(dirname)
        ## if DB_Backup does not exist make it
        print("24",os.getcwd())
        if not os.path.isdir('DB_Backup'):
            os.mkdir('DB_Backup')
        ## go to DB_Backup
        print("28",os.getcwd())
        os.chdir(os.getcwd() + '/DB_Backup')
        print("30",os.getcwd())
        ## if dirs A,B,C do not exist make them
        if not os.path.isdir('A'):
            os.mkdir('A')
        if not os.path.isdir('B'):
            os.mkdir('B')
        if not os.path.isdir('C'):
            os.mkdir('C')
        ## delete C
        shutil.rmtree('C')
        ## rename B to C
        os.rename('B','C')
        ## rename A to B
        os.rename('A','B')
        ## Remove A if exists and make A
        if os.path.isdir('A'):
            shutil.rmtree('A')
        os.mkdir('A')
        
        ## go into A
        os.chdir(os.getcwd() + '/A')
        ## for each collection
        for collection in collections:
            filename = collection+'.json'
            print("collection = ",collection)
            cursor = db[collection].find({})
            ## create a json file with collection name
            ## write the collection in that file
            with open(filename, 'w') as file:
                file.write('[')
                for document in cursor:
                    file.write(dumps(document))
                    file.write(',')
                file.write(']')
        os.chdir(os.path.dirname(os.getcwd()))
        print("64",os.getcwd())
        return
            