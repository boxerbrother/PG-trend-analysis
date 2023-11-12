import logging
import pandas as pd
import os
import time
import datetime

class Hgpd():
    logging.info("Begin to process the HGPD File...")
    def hgpdFileProcessor(filename):
        #Check if the input file exists or not, if file doesn't exists in the provided path then exit
        if not (os.path.isfile(filename)):
            print("The entered file doesn't exists")
            logging.info("Then entered file doesn't exist. Please re-run with correct file.")
            time.sleep(300)
            exit()
        else:
            logging.info("HGPD File provided is valid %s", filename)     

        logging.info("Begin reading the PD file...")       

        #Sheet_name=None is to read all the remaining sheets as dictionary. 
        #The dictionary's key is Sheet Name and Value is data for that sheet as dataframe
        sheets = pd.read_excel(filename, engine="openpyxl", usecols="A,B,C,E,H,O,P",sheet_name=None)

        #Create empty Dataframe
        hgpd_df = pd.DataFrame()
        
        #Iterate over each sheet's data and keep on appending data of all sheet to one dataframe
        for sheet in sheets:
            hgpd_df = hgpd_df._append(sheets[sheet],ignore_index=True)
            logging.info("Reading Sheet '%s' from excel", sheet)

        #Extract Month Name from Column 'N' of input spreadsheet and read only 1 row
        month_name = pd.read_excel(filename, engine="openpyxl", usecols="N",nrows=1,)

        #Create list of two column name which needs to be updated in final output header
        columnlist_with_month_name = [month_name.to_string(header=False,index=False)+' Final Invoice Value',
                                    month_name.to_string(header=False,index=False)+' Final Invoice Qty']
        
        #Create dictionary of 'Original Column' with 'New/Updated Column'
        columndict = {'Final Invoice Value' : month_name.to_string(header=False,index=False)+' Final Invoice Value',
                    'Final Invoice Qty' : month_name.to_string(header=False,index=False)+' Final Invoice Qty'}
        
        #pg_list_master file is a static file which usually doesn't change monthly, hence hardcoding the filepath
        pg_list_master  = r'C:\Users\sonikar\Documents\ProcessAutomation\PG_Trend_Project\PG_List.xlsx'

        #Read input pg_list_master in READONLY mode
        pg_list_df = pd.read_excel(open(pg_list_master,'rb'))

        logging.info("Vlookup has begun...")

        #Vlookup on 'Part Number' and whereever 'Part Number' matches append 'PG' & 'OldNew' columns for that row
        merged_data = pd.merge( hgpd_df, pg_list_df, on='Part Number',how='left')
        
        #Update the column names to have Date
        merged_data.rename(columns=columndict,inplace=True)

        #Code below in tripple quote is commented as it is for testing/debugging purpose
        #This code writes all the data to text file (if row count is > 8,00,000)
        # if (len(merged_data.index) > 800000):
        #     #specify path for export
        #     path = r'C:\Users\sonikar\Documents\ProcessAutomation\PG_Trend_Project\merged_df.txt'
        #     #export rows of all the sheets together to text file
        #     with open(path, 'a') as f:
        #         df_string = merged_data.to_string(index=False)
        #         f.write(df_string)
        # else:
        #     #Below Step writes all the columns after applying VLOOKUP based on 'Part Number'
        #     merged_data.to_excel('AWPR_PGList_Vlookup_output.xlsx',index=False)
        
        logging.info("Pivoting has begun...")        
        #Apply the pivot on 'Part Number' and consider 'Final Invoice Value' and 'Final Invoice Qty' columns for filter
        pivoted_data = merged_data.pivot_table(index=['Part Number','PG','OldNew'],
                                           values=columnlist_with_month_name,
                                           aggfunc="sum"
                                          )



        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        #Write the pivoted data in a excel file 'output.xlsx'
        filename = 'HGPD_output_pivot'+month_name.to_string(header=False,index=False) + ts +'.xlsx'
        output_file = r'C:\Users\sonikar\Documents\Scheme Formulation\Process_automation_output\PG_trend_analysis'+ '\\' + filename
        logging.info("Writing to output file %s", output_file)
        print("Writing to output file :", output_file)
        pivoted_data.to_excel(output_file)
    