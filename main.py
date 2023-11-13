# This project is to automate the PG Trend Analysis.
# Inputs: 'List of Part No'
# Output: PG_Trend_Output_Month.xlxs
import logger
import hgpdFileProcessor
import pdFileProcessor
import time

if __name__ == "__main__":
    #calling the Logger class present in logger.py file.
    logger.Logger.logSetup()
    logger.Logger.clockTime('START')
    print("#######################################################")
    print("########## PD or HGPD MONTHLY FILE PROCESSOR ##########")
    print("#######################################################\n")
    print("Enter 1 for PD file process \nEnter 2 for HGPD file process")
    process_type = input("Please enter 1 or 2 : ")

    if (process_type == '1'):
        file = input("Please enter the PD AWPR filename with Path: ")
        print("Beginning to PD process file : ", file)
        pdFileProcessor.Pd.pdFileProcessor(file)
        print("Done processing PD file...")
    else:
        file = input("Please enter the HGPD AWPR filename with Path: ")
        print("Beginning to HGPD process file : ", file)
        hgpdFileProcessor.Hgpd.hgpdFileProcessor(file)
        print("Done processing HGPD file...")
    logger.Logger.clockTime('END')
    time.sleep(30000)