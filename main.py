from glob import glob
from pikepdf import Pdf
import sys

import pdfplumber
import os

import pandas as pd
import altair as alt
import fileinput
passw=input('please enter password::')


pdf = Pdf.new()
version = pdf.pdf_version
#add all pdfs in the file directory in the mpesa_analysis
for f in glob('/home/mclnerney/mpesa_analysis/files/*.pdf'):
    src= Pdf.open(f,password=passw)
    pdf.pages.extend(src.pages)

pdf.remove_unreferenced_resources()
pdf.save('mergd.pdf',min_version=version)



pdf=pdfplumber.open("/home/mclnerney/mpesa_analysis/mergd.pdf")
numpage=len(pdf.pages)
listtable=[]
for i in range(numpage):
    
    p0 = pdf.pages[i]

    table = p0.extract_table()
    df = pd.DataFrame(table[1:], columns=table[0])

    listtable.append(df)

listtable=pd.concat(listtable)
        
 
data=listtable
data['Completion Time'] = pd.to_datetime(data['Completion Time']) 
data.sort_values(by='Completion Time') 
p=['Receipt No.','Balance', 'Details','Transaction\nStatus']
df=data.drop(p,axis=1) 

df.loc[:,'Balance'] = df[['Paid In', 'Withdrawn']].sum(axis=1)
df.loc['Total']= df.sum(numeric_only=True, axis=0)

df.to_excel("output.xlsx") 

chart1=alt.Chart(df).mark_point(color='red').encode(
    x='Completion Time:T',
    y='Withdrawn:Q'
   
)
chart2=alt.Chart(df).mark_point(color='green').encode(
    x='Completion Time:T',
    y='Paid In:Q'
)
chart=chart2 + chart1
chart.show()

        
        
