import datetime
import re
import time
import pandas as pd
import numpy as np
import PySimpleGUI as sg

def is_work(letter:str):
    return True if re.match(r'(W)([\d])',letter) else False

def is_hang_muc(letter:str):
    return True if re.match(r'(HM)([\d])',letter) else False

def is_norm(letter:str):
    return True if re.match(r'([A-Za-z]{2})(.)([\d]{5})',letter) else False

def is_machine(letter:str):
    return True if re.match(r'(^[Mm])([\d]+)',letter) else False

def is_worker(letter:str):
    return True if re.match(r'(^[Nn])([\d]+)',letter) else False

def is_material(letter):
    return True if re.match(r'([\d]+)',letter) else False

def is_dif_machine(letter):
    return True if letter in ['ZM999','zm999'] else False

def is_dif_material(letter):   
    return True if letter in ['ZV999','zv999'] else False

def read_excel(path) -> pd.DataFrame:
    dutoanDF = pd.read_excel(path,sheet_name='Chiết tính',header=4,usecols='c:g')

    # Fill cho hàng Mã CV
    dutoanDF[dutoanDF.columns[0]].fillna(inplace=True,method='ffill')
    #Xóa duplucate
    dutoanDF.drop_duplicates(subset=[dutoanDF.columns[0],dutoanDF.columns[1]],inplace=True)
    # Xóa dòng trống
    dutoanDF.dropna(subset=[dutoanDF.columns[1]],inplace=True)
    # Xóa TT và TĐG
    dutoanDF = dutoanDF[dutoanDF[dutoanDF.columns[0]].apply(len)==8]
    # Fill NA cho cột định mức 
    dutoanDF[dutoanDF.columns[4]].fillna(inplace=True,value=0)
    
    return dutoanDF

def display_date_time(date_time:datetime.datetime):
    format = r'%d/%m/%y'
    return date_time.strftime(format)

def to_date(text):
    date_pattern = {r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}$":r'%d/%m/%y', r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$":r'%d/%m/%Y',
                     r"^[0-9]{1,2}-[0-9]{1,2}-[0-9]{2}$":r'%d-%m-%y', r"^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$":r'%d-%m-%Y',
                    r"^[0-9]{1,2}.[0-9]{1,2}.[0-9]{2}$":r'%d.%m.%y', r"^[0-9]{1,2}.[0-9]{1,2}.[0-9]{4}$":r'%d.%m.%Y'}
    
    for p, format in date_pattern.items():
        if re.findall(re.compile(p),text):
            return datetime.datetime.strptime(text,format)
    return None

def try_parse_string_to_float(text:str,message:str=fr"Value error: can not convert to float",element_focus:sg.Element=None):
    try:
        return float(text)
    except ValueError:
        sg.popup_ok('input amount is not float!!!', keep_on_top=True)
        if element_focus:
            element_focus.set_focus()
        return text
        
def main():
    df = read_excel('D:\Python\QuanProject\qlcl project git\qlcl_project\PLHĐ nha thanh tra Kim Bang 2022.xls')
    # norm = df[df.iloc[1].map(is_norm)]
    a = ['AG.11113', 'AG.31121', 'AG.13111']
    norm = df[df.iloc[:,1].map(is_norm)]
    norm_1 = norm[norm.iloc[:,1].isin(a)]
    # print(norm_1.head(10))
    print(df.iloc[1])

if __name__ == "__main__":
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')


    
        
    