import logging
import time
import timeit

#Logging Setup by defining logging pattern, filename and level
logging.basicConfig(format='%(asctime)s  %(lineno)d %(message)s',
                    filename='pg_trend_log.log', encoding='utf-8',
                    level=logging.DEBUG)

class Logger():
    global start 
    start = timeit.default_timer()
    def logSetup():
        #Open the log file in write mode and trucate the data in the file while opening
        with open("pg_trend_log.log", 'w') as logfile:
            logfile.truncate(0)
        
    def clockTime(state):
        if (state == 'START'):
            #Starting Time
            start_time = time.time()
            logging.info("##########################################")
            logging.info("Process Started... ")
            logging.info("##########################################")
        elif (state == 'END'):
            #Ending Time
            end_time = time.time()
            stop = timeit.default_timer()
            execution_time = stop - start
            logging.info("##########################################")
            logging.info("Process Ended in %s mins", execution_time/60)
            logging.info("##########################################")
            print("Total time taken by the process in minutes is: ", execution_time /60)