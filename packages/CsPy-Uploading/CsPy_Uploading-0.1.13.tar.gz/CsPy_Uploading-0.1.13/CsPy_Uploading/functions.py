import pandas as pd
import numpy as np
import datetime as dt
import dateutil as du
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

# TODO: Add better error exceptions
# TODO: Add full function descriptions
# TODO: Delete Big Query Tables Function


def read_query_from_file(file_path):
    with open(file_path, 'r') as text:
        query = text.read()
        text.close()
    return query


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset+amount]


def insert_line():
    print('===================================================================================================')


def thg_log():
    print("""
--=================================================================================================--                                                                                                                                                                                                  
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
--=================================================================================================--
    """)


def log(string):
    """
    INTERNAL FUNCTION
    """
    print(dt.datetime.now(), ': ', string)


def copy_excel(source, destination):
    """
    FUNCTION: copy_excel
        DESC: Copys a excel workbook to another location.
        EXAMPLE: copy_excel("C:Documents/file.xslx", "C:Documents/new_file.xslx")

    PARAM(STRING): source
        DESC: File path of excel document ou wish to copy.
        EXAMPLE: "C:Documents/file.xslx"

    PARAM(STRING): destination
        DESC: File path you wish to copy the excel workbook to.
        EXAMPLE: "C:Documents/new_file.xslx"
    """
    wb1 = xl.load_workbook(source, data_only=True)
    wb1.save(str(destination))


def save_excel_sheets_to_csv(xls_path, save_path, sheet_names=None):
    """
    FUNCTION: save_excel_sheets_to_csv
        DESC: Converts a xlsx file into csv files of each sheet.
        EXAMPLE: save_excel_sheet_to_csv("C:Documents/file.xslx", "C:Documents/{}.csv", sheet_names=['sheet1','sheet3'])

    PARAM(STRING): xls_path
        DESC: File path of the excel workbook you wish to split out.
        EXAMPLE: "C:Documents/file.xslx"

    PARAM(STRING): save_path
        DESC: Folder location that you wish to save the csv files to.
        EXAMPLE: "C:Documents/{}.csv"

    OPTIONAL(LIST): sheet_names
        DESC: Use if you only need specific sheets.
        EXAMPLE: ['sheet1','sheet3']
    """
    log('Loading {} into pandas.'.format(xls_path))
    wb = pd.ExcelFile(xls_path)
    for idx, name in enumerate(wb.sheet_names):
        if sheet_names is not None:
            if name in sheet_names:
                log('Reading sheet #{0}: {1}'.format(idx, name))
                sheet = wb.parse(name)
                sheet.to_csv(save_path.format(name), index=False)

        elif sheet_names is None:
            log('Reading sheet #{0}: {1}'.format(idx, name))
            sheet = wb.parse(name)
            sheet.to_csv(save_path.format(name), index=False)


def delete_folder_contents(directory):
    """
    FUNCTION: delete_folder_contents
        DESC: Deletes every file from input folder location.
        EXAMPLE: delete_folder_contents("C:Documents/folder/")

    PARAM(STRING): directory
        DESC: Folder Path that you wish to delete the contents of.
        EXAMPLE: "C:Documents/folder/"
    """
    log('Deleting files from: {}'.format(directory))
    for file in os.listdir(directory):
        log('Deleteing: {}'.format(file))
        os.unlink(directory + file)


def date_convert(data_frame, schema):
    """
    FUNCTION: date_convert
        DESC: Converts each date column in a dataframe to datekeys
        EXAMPLE: date_convert(pd.dataframe(), schema)

    PARAM(PANDAS DATAFRAME): data_frame
        DESC: Data Frame you wish to convert
        EXAMPLE: pd.dataframe()

    PARAM(ARRAY): schmea
        EXAMPLE: schema = [sf(name="Locale", field_type="STRING", mode="NULLABLE"),
                           sf(name="Revenue", field_type="FLOAT", mode="NULLABLE"),
                           sf(name="Order_Date", field_type="DATE", mode="NULLABLE")]
        NOTE: Column names and data types of dataframe having date columns labeled 'DATE' or 'DATETIME'

    """
    convert_columns = []
    new_schema = []
    for i in schema:
        if i.field_type in ('DATETIME', 'DATE'):
            convert_columns.append(i.name)

    if len(convert_columns) != 0:
        log('Date columns to be converted to keys: '.format(str(convert_columns)))

    for i in convert_columns:
        try:
            log('Converting date column '.format(i))
            data_frame[i] = pd.to_datetime(data_frame[i])
            data_frame[i] = data_frame[i].fillna(dt.datetime(1990, 1, 1))
            data_frame[i] = data_frame[i].dt.strftime('%Y%m%d').astype(int)
            data_frame[i] = data_frame[i].replace(19900101, np.nan)
        except Exception as e:
            log('Failed to convert {} column to a date.'.format(i))
            log('Error: {}'.format(e))

    for i in schema:
        if i.name in convert_columns:
            x = sf(name=i.name, field_type='INTEGER', mode=i.mode)
            new_schema.append(x)
        else:
            new_schema.append(i)

    return data_frame, new_schema


def sql_to_workbook(query, dsn, save_path_file, num_tables, sheet_names=None):
    # TODO: finish this function using temp query and select queries
    """
    WORK IN PROGRESS
    """
    print('Reading Sql Query using {0} connection.'.format(dsn))
    connection = odbc.connect(dsn)
    for i in range(0, num_tables):
        print()


def date_selection(date_type, dates_included, interval=None, exclude_today=None, custom_start=None, custom_end=None,
                   preset=None, comps=None, alignment=None, wow=None, mom=None, yoy=None):
    """
    FUNCTION: date_selection
        DESC: Outputs Dates and Date Keys for various date ranges specified by the user
        EXAMPLE: date_selection(date_type='Custom', custom_start='2020-03-01', custom_end='2020-03-05',
                                comps=True, alignment='Date', wow=True, mom=True, yoy=True)

    PARAM(STRING): date_type
        DESC: Tells the function which type of request you want
        OPTIONS(Case Sensitive):

            1. 'Last' - Last x number of days
                REQUIREMENTS:
                    PARAM(INT): interval - How many days back you want to include
                    EXAMPLE: 7

            2. 'Custom' - Choose your own start and end dates
                REQUIREMENTS:
                    PARAM(STRING): custom_start - The start date
                    EXAMPLE: '2020-01-01'

                    PARAM(STRING): custom_end - The end date
                    EXMAPLE: '2020-01-01'

            3. 'Preset' - Choose fixed periods of time
                REQUIREMENTS:
                    PARAM(STRING): preset - A fixed period of time
                    OPTIONS(Case Sensitive):
                        'YTD' - Year to date
                        'MTD' - Month to date
                    NOTE: On the first of the month or year this will return the entire last month or year

    PARAM(STRING): dates_included
        DESC: Tells the function which date types you want to be ouptutted
        OPTIONS(Case Sensitive):

            1. 'Dates' - Will only return dates

            2. 'Keys' - Will only return date Keys

            3. 'Both' - Will return both dates and date keys of each date

    OPTIONAL(BOOLEAN): comps
        DESC: Tells the function to calculated comparison dates for the settings chosen
        REQUIREMENTS:
            PARAM(STRING): alignment
            DESC: Which date alignment should be used for comparison dates
            OPTIONS(Case Sensitive):

                1. 'Day' - Will take a day to day comparison (Comparing a Monday to a Monday)

                2. 'Date' - Comparing the same date for the comparison type

            PARAM(BOOLEAN): wow
            DESC: A toggle to include wow comparisons

            PARAM(BOOLEAN): mom
            DESC: A toggle to include mom comparisons

            PARAM(BOOLEAN): yoy
            DESC: A toggle to include yoy comparisons

    OPTIONAL(BOOLEAN): exclude_today
        DESC: Tells the function whether to include the current date in date ranges or remove it

    OUTPUT:
        The output size varies depending on the options chosen but the structure will always follow the below ordering
        (
            Start_Date
            Start_Date_WoW
            Start_Date_MoM
            Start_Date_YoY
            Start_Date_Key
            Start_Date_Key_WoW
            Start_Date_Key_MoM
            Start_Date_Key_YoY
            End_Date
            End_Date_WoW
            End_Date_MoM
            End_Date_YoY
            End_Date_Key
            End_Date_Key_WoW
            End_Date_Key_MoM
            End_Date_Key_YoY
        )
    """
    start_date = ''
    end_date = ''
    start_date_key = 1
    end_date_key = 1

    if date_type == 'Last':
        start_date = dt.datetime.now().date() + dt.timedelta(days=-1*interval)
        if exclude_today:
            interval = 1
        else:
            interval = 0
        end_date = dt.datetime.now().date() + dt.timedelta(days=-1*interval)

    if date_type == 'Custom':
        start_date = custom_start
        end_date = custom_end

    if date_type == 'Preset':
        year = (dt.datetime.now().date()).year
        month = (dt.datetime.now().date()).month
        day = (dt.datetime.now().date()).day
        m_flag = 0
        y_flag = 0

        if month != (dt.datetime.now() + dt.timedelta(days=-1)).month:
            month += -1
            m_flag = 1
        if year != (dt.datetime.now() + dt.timedelta(days=-1)).year:
            year += -1
            y_flag = 1

        if preset == 'MTD':
            start_date = dt.date(year, month, 1)
            if exclude_today:
                end_date = (dt.datetime.now() + dt.timedelta(days=-1)).date()
            else:
                end_date = (dt.datetime.now()).date()
                if m_flag == 1:
                    end_date = (dt.datetime.now() + dt.timedelta(days=-1)).date()

        if preset == 'YTD':
            start_date = dt.date(year, 1, 1)
            if exclude_today:
                end_date = (dt.datetime.now() + dt.timedelta(days=-1)).date()
            else:
                end_date = (dt.datetime.now()).date()
                if y_flag == 1:
                    end_date = (dt.datetime.now() + dt.timedelta(days=-1)).date()

    start_date = str(start_date)
    end_date = str(end_date)
    start_date_key = str(start_date).replace('-', '')
    end_date_key = str(end_date).replace('-', '')

    if comps:
        start_date_wow = ''
        start_date_mom = ''
        start_date_yoy = ''
        end_date_wow = ''
        end_date_mom = ''
        end_date_yoy = ''

        if alignment == 'Date':
            start_date_wow = (dt.datetime.strptime(start_date, '%Y-%m-%d') + dt.timedelta(weeks=-1)).date()
            end_date_wow = (dt.datetime.strptime(end_date, '%Y-%m-%d') + dt.timedelta(weeks=-1)).date()
            start_date_mom = (dt.datetime.strptime(start_date, '%Y-%m-%d') + du.relativedelta.relativedelta(months=-1)).date()
            end_date_mom = (dt.datetime.strptime(end_date, '%Y-%m-%d') + du.relativedelta.relativedelta(months=-1)).date()
            start_date_yoy = (dt.datetime.strptime(start_date, '%Y-%m-%d') + du.relativedelta.relativedelta(years=-1)).date()
            end_date_yoy = (dt.datetime.strptime(end_date, '%Y-%m-%d') + du.relativedelta.relativedelta(years=-1)).date()

        elif alignment == 'Day':
            start_date_wow = (dt.datetime.strptime(start_date, '%Y-%m-%d') + dt.timedelta(weeks=-1)).date()
            end_date_wow = (dt.datetime.strptime(end_date, '%Y-%m-%d') + dt.timedelta(weeks=-1)).date()
            start_date_mom = (dt.datetime.strptime(start_date, '%Y-%m-%d') + dt.timedelta(days=-28)).date()
            end_date_mom = (dt.datetime.strptime(end_date, '%Y-%m-%d') + dt.timedelta(days=-28)).date()
            start_date_yoy = (dt.datetime.strptime(start_date, '%Y-%m-%d') + dt.timedelta(days=-364)).date()
            end_date_yoy = (dt.datetime.strptime(end_date, '%Y-%m-%d') + dt.timedelta(days=-364)).date()

        start_date_key_wow = str(start_date_wow).replace('-', '')
        start_date_key_mom = str(start_date_mom).replace('-', '')
        start_date_key_yoy = str(start_date_yoy).replace('-', '')
        end_date_key_wow = str(end_date_wow).replace('-', '')
        end_date_key_mom = str(end_date_mom).replace('-', '')
        end_date_key_yoy = str(end_date_yoy).replace('-', '')

    start = [start_date]
    start_key = [start_date_key]
    end = [end_date]
    end_key = [end_date_key]

    if comps:
        if wow:
            start.append(start_date_wow)
            start_key.append(start_date_key_wow)
            end.append(end_date_wow)
            end_key.append(end_date_key_wow)

        if mom:
            start.append(start_date_mom)
            start_key.append(start_date_key_mom)
            end.append(end_date_mom)
            end_key.append(end_date_key_mom)

        if yoy:
            start.append(start_date_yoy)
            start_key.append(start_date_key_yoy)
            end.append(end_date_yoy)
            end_key.append(end_date_key_yoy)

    if dates_included == 'Both':
        start = start + start_key
        end = end + end_key
        final = tuple(start + end)

    if dates_included == 'Keys':
        final = tuple(start_key + end_key)

    if dates_included == 'Dates':
        final = tuple(start + end)

    return final

