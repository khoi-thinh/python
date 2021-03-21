#Install necessary library
#pip install pandas, xlsxwriter, openpyxl
#Read original excel file, filter column, remove unnecessary column and export final data to new excel file

import pandas as pd
data = pd.read_excel(r"C:\Users\user\Desktop\Sample.xlsx")

print(data)
print("-------------------")

#result1 = data[(data["City"]=="Tokyo") & (data["Job"]=="Engineer")] 
result2 = data[(data["Job"]=="Engineer") | (data["Job"]=="Teacher") & (data["Gender"]=="Female")] 

#print(result1)
#print("-------------------")
#print(result2)
#print("-------------------")

#Create a new Excel file to store filtered data
writer = pd.ExcelWriter(r"C:\Users\user\Desktop\Result.xlsx", engine='xlsxwriter')
writer.save()

#Use Dataframe to sort/filter data
processDrop = pd.DataFrame(result2)
print(processDrop)
print("------------------")

#Remove Gender column
del processDrop["Gender"]
print(processDrop)

#Export final data to new Excel
processDrop.to_excel(r"C:\Users\user\Desktop\Result.xlsx", index=False)
