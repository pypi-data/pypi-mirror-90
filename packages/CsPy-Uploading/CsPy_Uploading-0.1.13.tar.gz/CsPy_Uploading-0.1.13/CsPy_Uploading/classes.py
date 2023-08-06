import pandas as pd
import numpy as np
import datetime as dt
import os as os
import openpyxl as xl
import pyodbc as odbc
import humanfriendly as hf
import platform as pl
import win32com.client as win32
import sys
from google.cloud.bigquery import Client, LoadJobConfig, DatasetReference
from google.cloud.bigquery import SchemaField as sf
from google.oauth2 import service_account
from CsPy_Uploading.functions import read_query_from_file
from CsPy_Uploading.functions import left
from CsPy_Uploading.functions import right
from CsPy_Uploading.functions import mid
from CsPy_Uploading.functions import insert_line
from CsPy_Uploading.functions import thg_log
from CsPy_Uploading.functions import log
from CsPy_Uploading.functions import copy_excel
from CsPy_Uploading.functions import save_excel_sheets_to_csv
from CsPy_Uploading.functions import delete_folder_contents
from CsPy_Uploading.functions import date_convert
from CsPy_Uploading.functions import sql_to_workbook
from CsPy_Uploading.functions import date_selection


# TODO: Add better error exceptions
# TODO: Add function/variable descriptions
# TODO: Add error handling for miss matched column names
# TODO: Add Read Functionality
# TODO: Deletion infrastructure
# TODO: Handle Bug when no account is set on VM for uploading (Probably just disable logging)


class DownloadJob:
    """
    WORK IN PROGRESS
    """
    def __init__(self, query, save_file_path, file_name=None, bq_project_read=None, bq_key=None, dsn=None,
                 set_logging=None, set_open_csv=None,
                 first_name=None, surname=None):
        self.start_time = dt.datetime.now()
        self.thg_log()
        self.job_progress = "Initialising Job"
        self.query = query
        self.save_file_path = save_file_path
        self.file_name = file_name
        self.bq_project_read = bq_project_read
        self.bq_key = bq_key
        self.dsn = dsn
        self.set_logging = set_logging
        self.set_open_csv = set_open_csv
        self.first_name = first_name
        self.surname = surname
        self.connection_test = False
        self.end_script = False
        self.variable_check()
        self.job_progress = "Searching For Accounts"
        self.account = Account(first_name, surname)
        self.job_progress = "Initialising Settings"
        self.download_setting = DownloadSettings(set_logging, set_open_csv)
        self.update_download_setting()
        self.save_file_path = self.get_save_file_path(save_file_path)
        self.data_from = self.get_download_type()
        self.credentials = self.get_credentials()
        self.get_dsn()
        self.get_bq_project()
        self.df = self.get_data_frame()
        pass

    def thg_log(self):
        """
        INTERNAL FUNCTION
        DONE
        """
        self.job_progress = "Producing Job Logo"
        print("""
===================================================================================================                                                                                                                                                                                                 
     @&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.              &&&&&&&&&&&@&&.        
     &&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.          @@&&&&&&&&&&&&&&&&&&&&/    
     ,.......&&&&&&&&........       &&&&&&&%           &&&&&&&.        @&&&&&&&&&&/..*&&&&&&&@      
             &&&&&&&@               &&&&&&&%           &&&&&&&.      ,&&&&&&&@             @        
             &&&&&&&@               &&&&&&&%           &&&&&&&.      &&&&&&&&                       
             &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.     .&&&&&&&             ,,,,,,.    
             &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.      &&&&&&&.            &&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.      @&&&&&&@/           &&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.       &&&&&&&&&@        /@&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.         &&&&&&&&&&&&&&&&&&&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.            &&&&&&&&&&&&&&&&@&.       
===================================================================================================
            """)

    def insert_line(self):
        """
        INTERNAL FUNCTION
        DONE
        """
        if self.download_setting.logging:
            print('===================================================================================================')

    def log(self, string):
        """
        INTERNAL FUNCTION
        """
        if self.download_setting.logging:
            print(dt.datetime.now(), ': ', string)

    def variable_check(self):
        """
        INTERNAL FUNCTION
        """
        if not isinstance(self.query, str):
            raise InputTypeError(
                job_progress=self.job_progress,
                variable="\'query\'",
                accepted_data_types="STR",
                input_data_type=type(self.query).__name__.capitalize()
            )

        if not isinstance(self.save_file_path, str):
            raise InputTypeError(
                job_progress=self.job_progress,
                variable="\'save_file_path\'",
                accepted_data_types="STR",
                input_data_type=type(self.save_file_path).__name__.capitalize()
            )

        if self.file_name is not None:
            if not isinstance(self.file_name, str):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'file_name\'",
                    accepted_data_types="STR",
                    input_data_type=type(self.file_name).__name__.capitalize()
                )

        if self.bq_project_read is not None:
            if not isinstance(self.bq_project_read, str):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'bq_project_read\'",
                    accepted_data_types="STR",
                    input_data_type=type(self.bq_project_read).__name__.capitalize()
                )

        if self.dsn is not None:
            if not isinstance(self.dsn, str):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'dsn\'",
                    accepted_data_types="STR",
                    input_data_type=type(self.dsn).__name__.capitalize()
                )

        if self.set_logging is not None:
            if not isinstance(self.set_logging, bool):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'set_logging\'",
                    accepted_data_types="BOOL",
                    input_data_type=type(self.set_logging).__name__.capitalize()
                )

        if self.set_open_csv is not None:
            if not isinstance(self.set_open_csv, bool):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'set_open_csv\'",
                    accepted_data_types="BOOL",
                    input_data_type=type(self.set_open_csv).__name__.capitalize()
                )

        if self.first_name is not None:
            if not isinstance(self.first_name, str):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'first_name\'",
                    accepted_data_types="STR",
                    input_data_type=type(self.first_name).__name__.capitalize()
                )

        if self.surname is not None:
            if not isinstance(self.surname, str):
                raise InputTypeError(
                    job_progress=self.job_progress,
                    variable="\'surname\'",
                    accepted_data_types="STR",
                    input_data_type=type(self.surname).__name__.capitalize()
                )

        pass

    def data_frame_info(self, start, end, df):
        """
        INTERNAL FUNCTION
        """
        if self.download_setting.logging:
            print('')
            self.insert_line()
            print('DataFrame Info:')
            print("""   Read from: """, self.data_from)
            print("""   Runtime: """, hf.format_timespan((end - start).total_seconds()))
            print("""   Row Count: """, len(df))
            print("""   Byte Size: """, df.memory_usage(index=True).sum())
            self.insert_line()
            print('')

    def update_download_setting(self):
        self.job_progress = "Updating Settings"
        if self.account.use_account:
            self.download_setting.use_account = True

    def get_save_file_path(self, save_file_path):
        self.job_progress = "Setting Save File Path"
        save_file_path = str(save_file_path).replace("\\", "/")
        if right(save_file_path, 1) != "/":
            save_file_path = save_file_path + "/"

        return save_file_path

    def get_download_type(self):
        self.job_progress = "Defining Download Type"
        if self.query is not None:
            sql_flags = ['set ansi_nulls off', 'set nocount on', 'set ansi_warnings off', 'datawarehouse',
                         'if object_id', 'declare', '(nolock)', 'marketing.cos']
            bq_flags = ['from `', 'with', 'ditto', 'lower', '_table_suffix', 'eu_data','1,2']
            sql_count = 0
            bq_count = 0
            for i in sql_flags:
                if i in self.query.lower():
                    sql_count += 1
            for i in bq_flags:
                if i in self.query.lower():
                    bq_count += 1
            if sql_count > bq_count:
                return 'SQL'
            elif sql_count < bq_count:
                return 'BQ'
            elif sql_count == bq_count:
                self.log('Cant classify query ending script.')
                self.end_script = True

    def get_credentials(self):
        """
        INTERNAL FUNCTION
        """
        credentials = ""
        if self.end_script:
            pass
        else:
            self.job_progress = "Getting Big Query Credentials"
            try:
                file = sys.modules['__main__'].__file__
                directory_name, file_name = os.path.split(os.path.abspath(file))
                vm_os = 'Windows-2008ServerR2-6.1.7601-SP1'
                user_os = pl.platform()
                scopes = ['https://www.googleapis.com/auth/bigquery', 'https://www.googleapis.com/auth/drive.readonly']
                if self.download_setting.vm_status:
                    self.log('Searching for credentials on VM')
                    if self.bq_key is not None:
                        self.log('Searching for credentials within current directory')
                        directory_name, file_name = os.path.split(os.path.abspath(file))
                        directory_name = str(directory_name).replace("\\", "/")
                        key_path = directory_name + '/' + self.bq_key
                    else:
                        self.log('Searching for credentials within VM Structure')
                        directory_name = 'C:/Users/customersciencevdi.THEHUTGROUP/cos-scripts/VM Structure/BQ Keys'
                        key_path = directory_name + '/key.json'
                else:
                    self.log('Searching for credentials on Local Drive')
                    directory_name, file_name = os.path.split(os.path.abspath(file))
                    directory_name = str(directory_name).replace("\\", "/")
                    key_path = directory_name + '/key.json'

                self.log('Key Path: {}'.format(key_path))
                credentials = service_account.Credentials.from_service_account_file(key_path, scopes=scopes)
                key_info = {}
                with open(key_path, 'r') as key_file:
                    text = key_file.read()
                    key_info = eval(text)
            except Exception as e:
                self.log('Failed to get BQ Credentials')
                self.log('Error: {}'.format(e))
                self.end_script = True

        return credentials

    def get_dsn(self):
        if self.end_script:
            pass
        else:
            self.job_progress = "Defining DSN Connection"
            dsn_server = ''
            if self.data_from == "SQL":
                if self.download_setting.use_account and self.dsn is None:
                    if self.account.info['priority_server'] == '1':
                        dsn_server = 'reporting'
                        self.log('Using Account Priority SQL Server: Reporting')
                        self.dsn = self.account.info['reporting_odbc']
                        if self.download_setting.vm_status:
                            self.log('Loading VM Reporting SQL Server ODBC connection.')
                            self.log('Converting SQL ODBC connecting from {} to {}'.format(self.dsn, 'CustomerProfiling'))
                            self.dsn = 'CustomerProfiling'

                    elif self.account.info['priority_server'] == '2':
                        self.log('Using Account Priority SQL Server: ReportingReadOnly')
                        dsn_server = 'readonly'
                        self.dsn = self.account.info['reporting_read_only_odbc']
                        if self.download_setting.vm_status:
                            self.log('Loading VM ReportingReadOnly SQL Server ODBC connection.')
                            self.log('Converting SQL ODBC connecting from {} to {}'.format(
                                self.dsn, 'CustomerProfiling_NewDWH'))
                            self.dsn = 'CustomerProfiling_NewDWH'

                    elif self.account.info['priority_server'] == '3':
                        self.log('Using Account Priority SQL Server: New Infrastructure')
                        dsn_server = 'new infra'
                        self.dsn = self.account.info['New_Infra_odbc']
                        if self.download_setting.vm_status:
                            self.log('Loading VM New Infra SQL Server ODBC connection.')
                            self.log('Converting SQL ODBC connection from {} to {}'.format(
                                self.dsn, 'CustomerProfiling_NewInfra_GB'))
                            self.dsn = 'CustomerProfiling_NewInfra_GB'
                            self.connection_test = True

                if self.download_setting.vm_status:
                    if dsn_server == 'reporting':
                        self.log('Loading VM Reporting SQL Server ODBC connection.')
                        self.log('Converting SQL ODBC connecting from {} to {}'.format(self.dsn, 'CustomerProfiling'))
                        self.dsn = 'CustomerProfiling'

                    elif dsn_server == 'readonly':
                        self.log('Loading VM ReportingReadOnly SQL Server ODBC connection.')
                        self.log('Converting SQL ODBC connecting from {} to {}'.format(
                            self.dsn, 'CustomerProfiling_NewDWH'))
                        self.dsn = 'CustomerProfiling_NewDWH'

                    elif dsn_server == 'new infra':
                        self.log('Loading VM New Infrastructure SQL Server ODBC connection.')
                        self.log('Converting SQL ODBC connecting from {} to {}'.format(
                            self.dsn, 'CustomerProfiling_NewInfra_GB'))
                        self.dsn = 'CustomerProfiling_NewInfra_GB'
                        self.connection_test = True

                elif not self.download_setting.use_account and self.dsn is None:
                    # Raise Input Error Here!
                    self.end_script = True
                    raise InputError(job_progress=self.job_progress,
                                     expression="DSN Value",
                                     message="Failed to provide a DSN connection whilst trying to read SQL",
                                     solution="Enter a DSN connection using the variable \'dsn\' when defining "
                                              "DownloadJob "
                                     )
            else:
                pass

    def get_bq_project(self):
        if self.end_script:
            pass
        else:
            self.job_progress = "Defining Big Query Project Read"
            if self.data_from == "BQ":
                if self.bq_project_read is None:
                    self.end_script = True
                    raise InputError(job_progress=self.job_progress,
                                     expression="BQ Project Read",
                                     message="Failed to provide a BQ Project Read value whilst trying to read BQ",
                                     solution="Enter a BQ Project Read using the variable \'bq_project_read\' "
                                              "when defining DownloadJob")

    def get_data_frame(self):
        if self.end_script:
            pass
        else:
            self.job_progress = "Getting Data Frame"
            start_time = dt.datetime.now()
            df = pd.DataFrame()
            if self.data_from == 'SQL':
                start_time = dt.datetime.now()
                self.log('Reading from SQL')
                self.log('DSN connection: {}'.format(self.dsn))
                self.query = """
                set ansi_nulls off 
                set nocount on 
                set ansi_warnings off
                """ + self.query
                if self.connection_test:
                    try:
                        connection = odbc.connect(dsn=self.dsn)
                        df = pd.read_sql(sql=self.query, con=connection)
                    except:
                        self.log('New Infra GB Node Failed attempting DE Node.')
                        self.log('Converting SQL ODBC connecting from {} to {}'.format(
                            self.dsn, 'CustomerProfiling_NewInfra_DE'))
                        self.dsn = 'CustomerProfiling_NewInfra_DE'
                        connection = odbc.connect(dsn=self.dsn)
                        df = pd.read_sql(sql=self.query, con=connection)
                else:
                    connection = odbc.connect(dsn=self.dsn)
                    df = pd.read_sql(sql=self.query, con=connection)

            elif self.data_from == 'BQ':
                self.log('Reading from Big Query')
                self.log('Project: {}'.format(self.bq_project_read))
                self.log('Collecting Data...')
                df = pd.read_gbq(query=self.query, project_id=self.bq_project_read, dialect='standard',
                                 credentials=self.credentials)
            end_time = dt.datetime.now()
            self.data_frame_info(start_time, end_time, df)
            return df

    def run(self):
        if self.end_script:
            pass
        else:
            self.job_progress = "Outputting Query and Dataset"
            if self.file_name is not None:
                text_location = self.save_file_path + "Query{}".format("_" + self.file_name + ".txt")
            else:
                text_location = self.save_file_path + "Query.txt"
            self.log("Storing Query to {}".format(text_location))
            text_file = open(text_location, "w")
            text_file.write(self.query)
            text_file.close()
            if self.file_name is not None:
                query_location = self.save_file_path + "Data{}".format("_" + self.file_name + ".csv")
            else:
                query_location = self.save_file_path + "Data.csv"
            self.log("Storing Query to {}".format(query_location))
            self.df.to_csv(query_location, index=False, header=True)
            if self.download_setting.open_csv:
                os.system('start "excel" "{}"'.format(query_location))


class DownloadSettings:
    """
    WORK IN PROGRESS
    """
    def __init__(self, logging, open_csv):
        if logging is None:
            self.logging = True
        else:
            self.logging = logging
        if open_csv is None:
            self.open_csv = False
        else:
            self.open_csv = open_csv
        self.vm_status = False
        self.use_account = False
        self.log_download_settings()
        self.get_vm_status()

    def log(self, string):
        if not self.logging:
            print(dt.datetime.now(), ': ', string)

    def log_download_settings(self):
        if self.logging:
            insert_line()
            print('Download Settings:')
            print("""   Logging: {}""".format(self.logging))

            insert_line()
            print('')
        else:
            print('Logging turned off.')

    def get_vm_status(self):
        vm_os = 'Windows-2008ServerR2-6.1.7601-SP1'
        user_os = pl.platform()
        if user_os == vm_os:
            self.vm_status = True
            log('Running on VM.')
        else:
            log('Running locally.')


class UploadJob:

    def __init__(self, bq_project, bq_dataset, table_name,
                 bq_key=None, csv=None, columns=None, query=None, dsn=None, save_file_path=None, schema=None, date_column=None,
                 set_date_conversion=None, set_logging=None, set_clear_csv_cache=None, set_testing=None,
                 first_name=None, surname=None):
        self.start_time = dt.datetime.now()
        self.thg_log()
        self.upload_details = {'Error': ''}
        self.job_progress = "Initialising Job"
        self.bq_project = bq_project
        self.bq_dataset = bq_dataset
        self.table_name = table_name
        self.bq_key = bq_key
        self.csv = csv
        self.columns = columns
        self.query = query
        self.dsn = dsn
        self.save_file_path = save_file_path
        self.schema = schema
        self.date_column = date_column
        self.set_date_conversion = set_date_conversion
        self.set_logging = set_logging
        self.set_clear_csv_cache = set_clear_csv_cache
        self.set_testing = set_testing
        self.first_name = first_name
        self.surname = surname
        self.connection_test = False
        self.variable_check()
        self.account = Account(first_name, surname)
        self.upload_setting = UploadSettings(set_date_conversion, set_logging, set_clear_csv_cache, set_testing)
        self.update_upload_setting()
        self.save_file_path = self.get_save_file_path(save_file_path)
        self.get_schema()
        self.credentials = self.get_credentials()
        self.bq_client = Client(project=self.bq_project, credentials=self.credentials)
        self.dataset_ref = DatasetReference(project=self.bq_project, dataset_id=self.bq_dataset)
        self.job_config = LoadJobConfig()
        self.update_job_config()
        self.data_from = self.get_upload_type()
        self.df = self.get_data_frame()
        self.date_convert()
        self.int_convert()

    def thg_log(self):
        """
        INTERNAL FUNCTION
        DONE
        """
        print("""
===================================================================================================                                                                                                                                                                                                 
     @&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.              &&&&&&&&&&&@&&.        
     &&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.          @@&&&&&&&&&&&&&&&&&&&&/    
     ,.......&&&&&&&&........       &&&&&&&%           &&&&&&&.        @&&&&&&&&&&/..*&&&&&&&@      
             &&&&&&&@               &&&&&&&%           &&&&&&&.      ,&&&&&&&@             @        
             &&&&&&&@               &&&&&&&%           &&&&&&&.      &&&&&&&&                       
             &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.     .&&&&&&&             ,,,,,,.    
             &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.      &&&&&&&.            &&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.      @&&&&&&@/           &&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.       &&&&&&&&&@        /@&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.         &&&&&&&&&&&&&&&&&&&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.            &&&&&&&&&&&&&&&&@&.       
===================================================================================================
            """)

    def insert_line(self):
        """
        INTERNAL FUNCTION
        DONE
        """
        if self.upload_setting.logging:
            print('===================================================================================================')

    def log(self, string):
        """
        INTERNAL FUNCTION
        DONE
        """
        if self.upload_setting.logging:
            print(dt.datetime.now(), ': ', string)

    def delete_folder_contents(self):
        """
        INTERNAL FUNCTION
        DONE
        """
        if self.upload_setting.clear_csv_cache:
            self.log('Deleting files from: {}'.format(self.save_file_path))
            for file in os.listdir(self.save_file_path):
                self.log('Deleting: {}'.format(file))
                os.unlink(self.save_file_path + '/' + file)

    def variable_check(self):
        """
        INTERNAL FUNCTION

        Not finished need to add all variable checks
        """
        # if not isinstance(self.bq_project, str):
        #     raise InputTypeError(
        #         job_progress=self.job_progress,
        #         variable="\'bq_project\'",
        #         accepted_data_types="STR",
        #         input_data_type=type(self.bq_project).__name__.capitalize()
        #     )
        #
        # if not isinstance(self.bq_dataset, str):
        #     raise InputTypeError(
        #         job_progress=self.job_progress,
        #         variable="\'bq_dataset\'",
        #         accepted_data_types="STR",
        #         input_data_type=type(self.bq_dataset).__name__.capitalize()
        #     )
        #
        # if not isinstance(self.table_name, str):
        #     raise InputTypeError(
        #         job_progress=self.job_progress,
        #         variable="\'table_name\'",
        #         accepted_data_types="STR",
        #         input_data_type=type(self.table_name).__name__.capitalize()
        #     )
        #
        # if self.csv is not None:
        #     if not isinstance(self.csv, str):
        #         raise InputTypeError(
        #             job_progress=self.job_progress,
        #             variable="\'csv\'",
        #             accepted_data_types="STR",
        #             input_data_type=type(self.csv).__name__.capitalize()
        #     )
        #
        # if self.columns is not None:
        #     if not isinstance(self.columns, list):
        #         if not isinstance(self.columns, bytearray):
        #             raise InputTypeError(
        #                 job_progress=self.job_progress,
        #                 variable="\'table_name\'",
        #                 accepted_data_types="list or array",
        #                 input_data_type=type(self.table_name).__name__.capitalize()
        #             )
        pass

    def data_frame_info(self, start, end, df):
        """
        INTERNAL FUNCTION
        DONE
        """
        if self.upload_setting.logging:
            print('')
            self.insert_line()
            print('DataFrame Info:')
            print("""   Read from: """, self.data_from)
            print("""   Runtime: """, hf.format_timespan((end - start).total_seconds()))
            print("""   Row Count: """, len(df))
            print("""   Byte Size: """, df.memory_usage(index=True).sum())
            self.upload_details['Bytes Uploaded'] = df.memory_usage(index=True).sum()
            self.insert_line()
            print('')

    def update_job_config(self):
        self.upload_details['Progress'] = 'Creating Job Config'
        self.log("Creating Upload Job Configuration.")
        self.job_config.write_disposition = 'WRITE_TRUNCATE'
        self.job_config.skip_leading_rows = 1
        self.job_config.source_format = 'CSV'
        if self.schema is not None:
            self.log('Schema Detected.')
            self.job_config.schema = self.schema

        else:
            self.log('Schema not detected using autodetect schema.')
            self.job_config.autodetect = True
            self.upload_setting.date_conversion = False

    def update_upload_setting(self):
        if self.account.use_account:
            self.upload_setting.use_account = True

    def date_convert(self):
        self.upload_details['Progress'] = 'Converting date columns to date keys.'
        self.job_progress = 'Converting date columns to date keys.'
        if self.upload_setting.date_conversion:
            convert_columns = []
            new_schema = []
            new_df = self.df
            for i in self.schema:
                if i.field_type in ('DATETIME', 'DATE'):
                    convert_columns.append(i.name)

            if len(convert_columns) != 0:
                log('Date columns to be converted to keys: {}'.format(str(convert_columns)))

            for i in convert_columns:
                try:
                    self.log('Converting date column {}'.format(i))
                    if i not in new_df.columns:
                        raise ColumnMissingError(
                            missing_column=i,
                            job_progress=self.job_progress
                        )
                    new_df[i] = pd.to_datetime(new_df[i])
                    new_df[i] = new_df[i].fillna(dt.datetime(1990, 1, 1))
                    new_df[i] = new_df[i].dt.strftime('%Y%m%d').astype(int)
                    new_df[i] = new_df[i].replace(19900101, np.nan)
                except Exception as e:
                    self.upload_details['Error'] = e
                    self.log('Failed to convert {} column to a date.'.format(i))
                    self.log('Error: {}'.format(e))

            for i in self.schema:
                if i.name in convert_columns:
                    x = sf(name=i.name, field_type='INTEGER', mode=i.mode)
                    new_schema.append(x)
                else:
                    new_schema.append(i)

            self.schema = new_schema
            self.df = new_df
            self.job_config.schema = self.schema

        else:
            pass

    def int_convert(self):
        if self.schema is not None:
            self.upload_details['Progress'] = 'Converting int columns for upload.'
            self.job_progress = 'Converting int columns for upload.'
            convert_columns = []
            new_schema = []
            new_df = self.df
            for i in self.schema:
                if i.field_type == 'INTEGER':
                    convert_columns.append(i.name)

            for i in convert_columns:
                if i not in new_df.columns:
                    raise ColumnMissingError(
                        missing_column=i,
                        job_progress=self.job_progress
                    )
                try:
                    new_df[i] = new_df[i].astype('float')
                    new_df[i] = new_df[i].astype('Int64')
                except Exception as e:
                    self.log('Failed To Convert Column: {} To INT'.format(i))
                    self.upload_details['Error'] = e

    def get_credentials(self):
        """
        INTERNAL FUNCTION
        """
        self.upload_details['Progress'] = 'Getting BQ Credentials'
        try:
            file = sys.modules['__main__'].__file__
            directory_name, file_name = os.path.split(os.path.abspath(file))
            self.upload_details['Location On VM'] = str(directory_name)
            self.upload_details['Script Name'] = right(file, (len(file)-file.rfind('/'))-1)
            vm_os = 'Windows-2008ServerR2-6.1.7601-SP1'
            user_os = pl.platform()
            scopes = ['https://www.googleapis.com/auth/bigquery', 'https://www.googleapis.com/auth/drive.readonly']
            if self.upload_setting.vm_status:
                self.log('Searching for credentials on VM')
                if self.bq_key is not None:
                    self.log('Searching for credentials within current directory')
                    directory_name, file_name = os.path.split(os.path.abspath(file))
                    directory_name = str(directory_name).replace("\\", "/")
                    key_path = directory_name + '/' + self.bq_key
                else:
                    self.log('Searching for credentials within VM Structure')
                    directory_name = 'C:/Users/customersciencevdi.THEHUTGROUP/cos-scripts/VM Structure/BQ Keys'
                    key_path = directory_name + '/key.json'
            else:
                self.log('Searching for credentials on Local Drive')
                directory_name, file_name = os.path.split(os.path.abspath(file))
                directory_name = str(directory_name).replace("\\", "/")
                key_path = directory_name + '/key.json'

            self.log('Key Path: {}'.format(key_path))
            credentials = service_account.Credentials.from_service_account_file(key_path, scopes=scopes)
            key_info = {}
            with open(key_path, 'r') as key_file:
                text = key_file.read()
                key_info = eval(text)
                self.upload_details['BQ Account Used'] = key_info['client_email']
        except Exception as e:
            self.upload_details['Error'] = e
            self.log('Failed to get BQ Credentials')
            self.log('Error: {}'.format(e))

        return credentials

    def get_dsn(self):
        dsn_server = ''
        if self.dsn is None:
            if self.upload_setting.use_account:
                if self.account.info['priority_server'] == '1':
                    dsn_server = 'reporting'
                    self.log('Using Account Priority SQL Server: Reporting')
                    self.dsn = self.account.info['reporting_odbc']
                    if self.upload_setting.vm_status:
                        self.log('Loading VM Reporting SQL Server ODBC connection.')
                        self.log('Converting SQL ODBC connecting from {} to {}'.format(self.dsn, 'CustomerProfiling'))
                        self.dsn = 'CustomerProfiling'

                elif self.account.info['priority_server'] == '2':
                    self.log('Using Account Priority SQL Server: ReportingReadOnly')
                    dsn_server = 'readonly'
                    self.dsn = self.account.info['reporting_read_only_odbc']
                    if self.upload_setting.vm_status:
                        self.log('Loading VM ReportingReadOnly SQL Server ODBC connection.')
                        self.log('Converting SQL ODBC connecting from {} to {}'.format(
                            self.dsn, 'CustomerProfiling_NewDWH'))
                        self.dsn = 'CustomerProfiling_NewDWH'

                elif self.account.info['priority_server'] == '3':
                    self.log('Using Account Priority SQL Server: New Infrastructure')
                    dsn_server = 'new infra'
                    self.dsn = self.account.info['New_Infra_odbc']
                    if self.upload_setting.vm_status:
                        self.log('Loading VM New Infra SQL Server ODBC connection.')
                        self.log('Converting SQL ODBC connection from {} to {}'.format(
                            self.dsn, 'CustomerProfiling_NewInfra_GB'))
                        self.dsn = 'CustomerProfiling_NewInfra_GB'
                        self.connection_test = True

            else:
                self.log('No DSN provided and no account information to create DSN connection.')

        elif self.dsn is not None:
            if self.upload_setting.use_account:
                if self.dsn == self.account.info['reporting_odbc']:
                    dsn_server = 'reporting'
                elif self.dsn == self.account.info['reporting_read_only_odbc']:
                    dsn_server = 'readonly'

        if self.upload_setting.vm_status:
            if dsn_server == 'reporting':
                self.log('Loading VM Reporting SQL Server ODBC connection.')
                self.log('Converting SQL ODBC connecting from {} to {}'.format(self.dsn, 'CustomerProfiling'))
                self.dsn = 'CustomerProfiling'

            elif dsn_server == 'readonly':
                self.log('Loading VM ReportingReadOnly SQL Server ODBC connection.')
                self.log('Converting SQL ODBC connecting from {} to {}'.format(self.dsn, 'CustomerProfiling_NewDWH'))
                self.dsn = 'CustomerProfiling_NewDWH'

            elif dsn_server == 'new infra':
                self.log('Loading VM New Infrastructure SQL Server ODBC connection.')
                self.log('Converting SQL ODBC connecting from {} to {}'.format(self.dsn, 'CustomerProfiling_NewInfra_GB'))
                self.dsn = 'CustomerProfiling_NewInfra_GB'
                self.connection_test = True

    def get_schema(self):
        self.upload_details['Progress'] = 'Getting Schema'
        if self.schema is not None:
            temp_schema = []
            try:
                for i in self.schema:
                    name = i[0]
                    field_type = i[1]
                    temp_schema.append(sf(name=name, field_type=field_type, mode="NULLABLE"))
                self.schema = temp_schema
            except Exception as e:
                self.log('Error: {}'.format(e))
                self.upload_details['Error'] = e
        pass

    def get_data_frame(self):
        self.upload_details['Progress'] = 'Getting dataframe.'
        start_time = dt.datetime.now()
        df = pd.DataFrame()
        if self.data_from == 'CSV':
            self.log('Reading from CSV - '.format(self.csv))
            if self.columns is not None:
                self.log('Using user defined column names')
                df = pd.read_csv(self.csv, names=self.columns, header=0)
            else:
                df = pd.read_csv(self.csv, header=0)

        elif self.data_from == 'SQL':
            start_time = dt.datetime.now()
            self.log('Reading from SQL')
            self.get_dsn()
            self.log('DSN connection: {}'.format(self.dsn))
            self.query = """
            set ansi_nulls off 
            set nocount on 
            set ansi_warnings off
            """ + self.query
            if self.connection_test:
                try:
                    connection = odbc.connect(dsn=self.dsn)
                    df = pd.read_sql(sql=self.query, con=connection)
                except:
                    self.log('New Infra GB Node Failed attempting DE Node.')
                    self.log('Converting SQL ODBC connecting from {} to {}'.format(
                        self.dsn, 'CustomerProfiling_NewInfra_DE'))
                    self.dsn = 'CustomerProfiling_NewInfra_DE'
                    connection = odbc.connect(dsn=self.dsn)
                    df = pd.read_sql(sql=self.query, con=connection)
            else:
                connection = odbc.connect(dsn=self.dsn)
                df = pd.read_sql(sql=self.query, con=connection)
            if self.columns is not None:
                df.columns(self.columns)

        elif self.data_from == 'BQ':
            self.log('Reading from Big Query')
            self.log('Project: {}'.format(self.bq_project))
            self.log('Collecting Data...')
            df = pd.read_gbq(query=self.query, project_id=self.bq_project, dialect='standard',
                             credentials=self.credentials)
            if self.columns is not None:
                df.columns(self.columns)
        end_time = dt.datetime.now()
        self.data_frame_info(start_time, end_time, df)
        return df

    def get_save_file_path(self, save_file_path):
        folder_path = ""
        self.upload_details['Progress'] = 'Getting Save File Path'
        if save_file_path is None:
            self.upload_setting.clear_csv_cache = True
            self.log("save_file_path not provided creating temporary CSV folder.")
            try:
                file = sys.modules['__main__'].__file__
                directory_name, file_name = os.path.split(os.path.abspath(file))
                directory_name = str(directory_name).replace("\\", "/") + "/"
                folder_path = directory_name + "CSV"
                i = 1
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                else:
                    flag = 0
                    while flag == 0:
                        folder_path = directory_name + "CSV"
                        folder_path = folder_path + "_" + str(i)
                        if not os.path.exists(folder_path):
                            os.mkdir(folder_path)
                            flag = 1
                        else:
                            i += 1
                self.log("Created temporary CSV folder: {}".format(folder_path))
                return folder_path
            except Exception as e:
                self.log("Failed to create temporary CSV folder.")
                self.log('Error: {}'.format(e))
                self.upload_details['Error'] = str(e)
        else:
            self.log('Using user defined save path')
            self.upload_setting.use_save_file_path = True
        return save_file_path

    def get_upload_type(self):
        self.upload_details['Progress'] = 'Getting Upload Type'
        if self.csv is not None:
            self.upload_details['Upload Type'] = 'From CSV'
            self.upload_details['SQL Access'] = 'No'
            self.upload_details['BQ Access'] = 'Write'
            return 'CSV'
        elif self.dsn is not None:
            self.upload_details['Upload Type'] = 'From SQL'
            self.upload_details['SQL Access'] = 'Yes'
            self.upload_details['BQ Access'] = 'Write'
            return 'SQL'
        elif self.query is not None:
            sql_flags = ['set ansi_nulls off', 'set nocount on', 'set ansi_warnings off', 'datawarehouse',
                         'if object_id', 'declare', '(nolock)', 'marketing.cos']
            bq_flags = ['from `', 'with', 'ditto', 'lower', '_table_suffix', 'eu_data', '1,2']
            sql_count = 0
            bq_count = 0
            for i in sql_flags:
                if i in self.query.lower():
                    sql_count += 1
            for i in bq_flags:
                if i in self.query.lower():
                    bq_count += 1
            if sql_count > bq_count:
                self.upload_details['Upload Type'] = 'From SQL'
                self.upload_details['SQL Access'] = 'Yes'
                self.upload_details['BQ Access'] = 'Write'
                return 'SQL'
            elif sql_count < bq_count:
                self.upload_details['Upload Type'] = 'From BQ'
                self.upload_details['SQL Access'] = 'No'
                self.upload_details['BQ Access'] = 'Read & Write'
                return 'BQ'
            elif sql_count == bq_count:
                self.log('Cant classify query.')
                self.upload_details['Error'] = 'Could not classify query.'

    def job_status(self):
        """
        WORK IN PROGRESS
        """
        if not self.upload_setting.vm_status:
            pass
        else:
            log('Running Local - Not Storing Job Status.')
            pass

    def run(self):
        self.upload_details['Progress'] = 'Uploading to Big query.'
        self.upload_details['GA Error'] = None
        try:
            delete_folder_contents(self.save_file_path)
            save_path = self.save_file_path + "/{}.csv"
            self.df.to_csv(save_path.format(self.table_name + '_full'), index=False, header=True)
            self.upload_details['Table Partitions'] = 0
            self.upload_details['Job Status'] = 'Ran Successfully'
            if self.date_column is not None:
                self.upload_details['Date Partitioned'] = 'Yes'
                for day, day_df in self.df.groupby(self.date_column):
                    self.upload_details['Table Partitions'] += 1
                    try:
                        day = str(day).replace('-', '')
                        day_new = day[:8]
                        self.log('Converted {0} to format {1}'.format(day, day_new))
                    except Exception as e:
                        self.log('Failed to convert {0} to format YYYYMMDD'.format(day))
                        day_new = day
                        self.log('Error: {}'.format(e))
                    try:
                        self.log('Uploading {0}{1} to {2}'.format(self.table_name, day_new, self.bq_dataset))
                        table_ref = self.dataset_ref.table(self.table_name + day_new)
                        day_df.to_csv(save_path.format(self.table_name + day_new), index=False, header=True)
                        with open(save_path.format(self.table_name + day_new), 'rb') as upload_file:
                            try:
                                upload_job = self.bq_client.load_table_from_file(
                                                    file_obj=upload_file, destination=table_ref,
                                                    job_config=self.job_config)
                                upload_job.result()
                                print(upload_job.state)
                            except Exception as e:
                                self.log("Table {0}{1} failed to upload to {2}".format(
                                    self.table_name, day_new, self.bq_dataset))
                                self.log('Error: {}'.format(e))
                                self.upload_details['Error'] = str(e)
                                if '400' in str(e):
                                    self.log('Error: {}'.format(upload_job.errors[0]['message']))
                                    self.log('Error: {}'.format(upload_job.errors[1]['message']))
                                    self.upload_details['GA Error'] = 'Error: {}'.format(
                                        upload_job.errors[1]['message'])
                    except Exception as e:
                        self.log('Error: {}'.format(e))
                        self.upload_details['Error'] = str(e)
            elif self.date_column is None:
                self.upload_details['Date Partitioned'] = 'No'
                self.log('Uploading {0} to {1}'.format(self.table_name, self.bq_dataset))
                table_ref = self.dataset_ref.table(self.table_name)
                with open(save_path.format(self.table_name + '_full'), 'rb') as upload_file:
                    try:
                        upload_job = self.bq_client.load_table_from_file(
                            file_obj=upload_file, destination=table_ref, job_config=self.job_config)
                        upload_job.result()
                        self.log(upload_job.state)
                    except Exception as e:
                        self.log("Table {0} failed to upload to {1}".format(self.table_name, self.bq_dataset))
                        self.log('Error: {}'.format(e))
                        self.upload_details['Error'] = 'Error: {}'.format(e)
                        if '400' in str(e):
                            self.log('Error: {}'.format(upload_job.errors[0]['message']))
                            self.log('Error: {}'.format(upload_job.errors[1]['message']))
                            self.upload_details['GA Error'] = 'Error: {}'.format(upload_job.errors[1]['message'])
        except Exception as e:
            self.log('Error: {}'.format(e))
            self.upload_details['Error'] = str(e)
            pass

        finally:
            self.get_upload_details()
            if self.upload_details['Error'] != '':
                self.send_email()
            if self.upload_setting.vm_status:
                self.log('Logging Upload to BQ')
                self.run_upload_details()
                self.log('DONE')
            if self.upload_setting.clear_csv_cache:
                if self.upload_setting.use_save_file_path:
                    self.log('Removing files from user defined CSV cache: {}'.format(self.save_file_path))
                    self.delete_folder_contents()
                else:
                    self.log('Removing files temporary CSV cache: {}'.format(self.save_file_path))
                    self.delete_folder_contents()
                    os.rmdir(self.save_file_path)
            pass

    def get_upload_details(self):
        if self.upload_setting.use_account:
            self.upload_details['Owner'] = self.account.info['first_name'] + ' ' + self.account.info['surname']
        else:
            self.upload_details['Owner'] = 'Not Defined'
        self.upload_details['Run Date'] = self.start_time
        self.upload_details['Runtime'] = (dt.datetime.now() - self.start_time).total_seconds()
        self.upload_details['BQ Project'] = self.bq_project
        self.upload_details['BQ Dataset'] = self.bq_dataset
        self.upload_details['BQ Table'] = self.table_name

    def run_upload_details(self):
        upload_details_schema = [
            sf(name="BQ_Project", field_type="STRING", mode="NULLABLE")
            , sf(name="BQ_Dataset", field_type="STRING", mode="NULLABLE")
            , sf(name="BQ_Table", field_type="STRING", mode="NULLABLE")
            , sf(name="Upload_Type", field_type="STRING", mode="NULLABLE")
            , sf(name="Job_Status", field_type="STRING", mode="NULLABLE")
            , sf(name="Owner", field_type="STRING", mode="NULLABLE")
            , sf(name="Run_Date", field_type="DATETIME", mode="NULLABLE")
            , sf(name="Location_On_VM", field_type="STRING", mode="NULLABLE")
            , sf(name="Script_Name", field_type="STRING", mode="NULLABLE")
            , sf(name="SQL_Access", field_type="STRING", mode="NULLABLE")
            , sf(name="BQ_Access", field_type="STRING", mode="NULLABLE")
            , sf(name="BQ_Account_Used", field_type="STRING", mode="NULLABLE")
            , sf(name="Bytes_Uploaded", field_type="INTEGER", mode="NULLABLE")
            , sf(name="Table_Partitions", field_type="INTEGER", mode="NULLABLE")
            , sf(name="Date_Partitioned", field_type="STRING", mode="NULLABLE")
            , sf(name="Runtime", field_type="FLOAT", mode="NULLABLE")
        ]
        upload_details_df = pd.DataFrame(
            data=
            {
                'BQ_Project': [self.upload_details['BQ Project']]
                , 'BQ_Dataset': [self.upload_details['BQ Dataset']]
                , 'BQ_Table': [self.upload_details['BQ Table']]
                , 'Upload_Type': [self.upload_details['Upload Type']]
                , 'Job_Status': [self.upload_details['Job Status']]
                , 'Owner': [self.upload_details['Owner']]
                , 'Run_Date': [self.upload_details['Run Date']]
                , 'Location_On_VM': [self.upload_details['Location On VM']]
                , 'Script_Name': [self.upload_details['Script Name']]
                , 'SQL_Access': [self.upload_details['SQL Access']]
                , 'BQ_Access': [self.upload_details['BQ Access']]
                , 'BQ_Account_Used': [self.upload_details['BQ Account Used']]
                , 'Bytes_Uploaded': [self.upload_details['Bytes Uploaded']]
                , 'Table_Partitions': [self.upload_details['Table Partitions']]
                , 'Date_Partitioned': [self.upload_details['Date Partitioned']]
                , 'Runtime': [self.upload_details['Runtime']]
            }
        )
        upload_details_bq_client = Client(project='agile-bonbon-662', credentials=self.credentials)
        upload_details_dataset_ref = upload_details_bq_client.dataset('VM_Audit')
        upload_details_job_config = LoadJobConfig()
        upload_details_job_config.write_disposition = 'WRITE_APPEND'
        upload_details_job_config.schema = upload_details_schema
        upload_details_job_config.skip_leading_rows = 1
        upload_details_job_config.source_format = 'CSV'
        save_path = self.save_file_path + "{}.csv"
        upload_details_df.to_csv(save_path.format('Upload_Details'), index=False, header=True)
        if not self.upload_setting.testing:
            with open(save_path.format('Upload_Details'), 'rb') as upload_details_file:
                try:
                    upload_job = upload_details_bq_client.load_table_from_file(
                        file_obj=upload_details_file, destination=upload_details_dataset_ref.table('VM_Audit'),
                        job_config=upload_details_job_config)
                    upload_job.result()
                    print(upload_job.state)
                except Exception as e:
                    self.log("Table Upload_Details failed to upload to VM_Audit")
                    self.log('Error: {}'.format(upload_job.errors[0]['message']))
                    self.log('Error: {}'.format(upload_job.errors[1]['message']))
                    self.upload_details['Error'] = e

            self.log('Removing Upload_Details CSV')
            os.unlink(save_path.format('Upload_Details'))
        else:
            self.log('Testing live not storing results in BQ')

    def send_email(self):
        self.get_upload_details()
        self.upload_details['Job Status'] = 'Ran Unsuccessfully'
        if not self.upload_setting.testing:
            if self.upload_setting.vm_status:
                if self.upload_setting.use_account:
                    outlook = win32.Dispatch('outlook.application')
                    email = outlook.CreateItem(0)
                    email.To = self.account.info['email']
                    email.Subject = 'VM Script: {} Failed to Run.'.format(self.upload_details['Script Name'])
                    if self.upload_details['Progress'] == 'Uploading to Big query.':
                        if self.upload_details['GA Error'] is None:
                            self.upload_details['GA Error'] = 'No GA Error'
                        email.HTMLBody = """
                            Time Ran: {3} <br><br>
                            The Script located at: {0}{1} <br><br>
                            The Script failed at: {4} <br><br>
                            Failed to run successfully due to python error message: {2} <br><br>
                            Failed to run successfully due to GA error message: {5}
                            """.format(self.upload_details['Location On VM'], self.upload_details['Script Name'],
                                       self.upload_details['Error'], self.upload_details['Run Date'],
                                       self.upload_details['Progress'], self.upload_details['GA Error'])
                    else:
                        email.HTMLBody = """
                            Time Ran: {3} <br><br>
                            The Script located at: {0}{1} <br><br>
                            The Script failed at: {4} <br><br>
                            Failed to run successfully due to error message: {2}
                            """.format(self.upload_details['Location On VM'], self.upload_details['Script Name'],
                                       self.upload_details['Error'], self.upload_details['Run Date'],
                                       self.upload_details['Progress'])
                    email.Send()


class UploadSettings:

    def __init__(self, date_conversion, logging, clear_csv_cache, testing):
        if date_conversion is None:
            self.date_conversion = False
        else:
            self.date_conversion = date_conversion

        if logging is None:
            self.logging = True
        else:
            self.logging = logging

        if clear_csv_cache is None:
            self.clear_csv_cache = True
        else:
            self.clear_csv_cache = clear_csv_cache

        if testing is None:
            self.testing = False
        else:
            self.testing = testing

        self.use_save_file_path = False
        self.vm_status = False
        self.use_account = False
        self.log_upload_settings()
        self.get_vm_status()

    def log(self, string):
        if not self.logging:
            print(dt.datetime.now(), ': ', string)

    def log_upload_settings(self):
        if self.logging:
            insert_line()
            print('Upload Settings:')
            print("""   Date Conversion: {}""".format(self.date_conversion))
            print("""   Logging: {}""".format(self.logging))
            print("""   Clear CSV cache: {}""".format(self.clear_csv_cache))
            print("""   Testing: {}""".format(self.testing))

            insert_line()
            print('')
        else:
            print('Logging turned off.')

    def get_vm_status(self):
        vm_os = 'Windows-2008ServerR2-6.1.7601-SP1'
        user_os = pl.platform()
        if user_os == vm_os:
            self.vm_status = True
            log('Running on VM.')
        else:
            log('Running locally.')


class Account:

    def __init__(self, first_name=None, surname=None):
        self.first_name = first_name
        self.surname = surname
        self.info = {}
        self.vm_status = False
        self.use_account = False
        self.get_vm_status()
        self.load_account()

    def load_account(self):
        if self.first_name is None and self.surname is None:
            pass
        else:
            insert_line()
            if self.vm_status:
                account_file = 'C:/Users/customersciencevdi.THEHUTGROUP/cos-scripts/VM Structure/Accounts/{}_{}.txt'
                account_path = account_file.format(self.first_name, self.surname)
            else:
                file = sys.modules['__main__'].__file__
                directory_name, file_name = os.path.split(os.path.abspath(file))
                directory_name = str(directory_name).replace("\\", "/") + "/"
                account_path = directory_name + '{}_{}.txt'.format(self.first_name, self.surname)

            try:
                with open(account_path, 'r') as file:
                    text = file.read()
                    self.info = eval(text)
                    self.use_account = True
                    log('Using Account: {} {}'.format(self.info['first_name'], self.info['surname']))

            except Exception as e:
                log('Error: {}'.format(e))
                log('Failed To Load Account.')

    def create_account(self):
        insert_line()
        print('Please provide answers to each request if you do not have the information currently enter: None')
        self.info['first_name'] = input("First Name?\n> ")
        self.info['surname'] = input("Surname?\n> ")
        self.info['email'] = input("Email Address?\n> ")
        self.info['laptop_serial_number'] = input("Laptop Serial Number?\n> ")
        self.info['New_Infra_odbc'] = input("SQL New Infrastructure ODBC Connection Name?\n>")
        self.info['reporting_odbc'] = input("SQL Reporting Server ODBC Connection Name?\n> ")
        self.info['reporting_read_only_odbc'] = input("SQL ReportingReadOnly Server ODBC Connection Name?\n> ")
        self.info['priority_server'] = input(
            "Priority SQL Server? \n 1 = Reporting \n 2 = ReadOnly \n 3 = New Infra \n> ")
        self.writing()

    def writing(self):
        if self.vm_status:
            path = 'C:/Users/customersciencevdi.THEHUTGROUP/cos-scripts/VM Structure/Accounts/{}_{}.txt'.format(
                self.info['first_name'], self.info['surname'])
        else:
            file = sys.modules['__main__'].__file__
            directory_name, file_name = os.path.split(os.path.abspath(file))
            directory_name = str(directory_name).replace("\\", "/") + "/"
            path = directory_name + '{}_{}.txt'.format(self.info['first_name'], self.info['surname'])

        if os.path.exists(path):
            os.remove(path)

        open(path, 'a').close()
        target = open(path, 'a')
        target.write(str(self.info))

    def get_vm_status(self):
        vm_os = 'Windows-2008ServerR2-6.1.7601-SP1'
        user_os = pl.platform()
        if user_os == vm_os:
            self.vm_status = True

    pass


class DownloadScriptFailure(Exception):
    """
    Exception raised for errors in the download script
    """

    def error_feedback(self):
        """
        WORK IN PROGRESS
        """
        pass

    pass


class InputError(Exception):
    """
    DESC: Exception Raised for errors in the input to download job

    VARIABLES:
        job_progress -- progress in the script
        expression -- input expression in which the error occured
        message -- explanation of the error
        solution -- most common way to fix the error
    """

    def __init__(self, job_progress, expression, message, solution):
        self.job_progress = job_progress
        self.expression = expression
        self.message = message
        self.solution = solution
        self.line = '=================================================================================================='
        super().__init__(self)

    def __str__(self):
        return f"""

        INPUT ERROR!
        {self.line}
        FAILED DURING: {self.job_progress}
        INPUT ERROR: {self.message}
        SOLUTION: {self.solution}
        {self.line}
        """


class InputTypeError(Exception):
    """
    DESC: Exception raised for errors with input types

    VARIABLES:
        job_progress -- Progress in the script
        variable -- Variable with incorrect data type
        data_types -- Entered data type & Correct Data Type
        message -- explanation of the error
    """

    def __init__(self, job_progress, variable, accepted_data_types, input_data_type):
        self.job_progress = job_progress
        self.variable = variable
        self.accepted_data_types = accepted_data_types
        self.input_data_type = input_data_type
        self.line = '=================================================================================================='
        super().__init__(self)

    def __str__(self):
        return f"""

        INPUT TYPE ERROR!
        {self.line}
        FAILED DURING: {self.job_progress}
        INPUT TYPE ERROR: Data type for {self.variable} does not match desired data type 
        SOLUTION: Accepted Data Types: {self.accepted_data_types.upper()}
                  Data Type Entered: {self.input_data_type.upper()} 
        {self.line}
        """


class ColumnMissingError(Exception):
    """
    DESC: Exception raised for errors within data_convert and int_convert

    VARIABLES:
        asd
    """

    def __init__(self, missing_column, job_progress):
        self.missing_column = missing_column
        self.job_progress = job_progress
        self.line = '=================================================================================================='
        super().__init__(self)

    def __str__(self):
        return f"""
        COLUMN NOT FOUND ERROR!
        {self.line}
        FAILED DURING: {self.job_progress}
        COLUMN NOT FOUND ERROR: Column name {self.missing_column} is not found
        SOLUTION: Make sure column names match the schema provided including case sensitivity
        {self.line}
        """
