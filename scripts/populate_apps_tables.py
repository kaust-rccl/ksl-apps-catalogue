import shutil
import mysql.connector
from tabulate import tabulate

# Copy the pages to the working directory

src1 = '/home/mohamm0a/ibex.rst'
dst1 = '.'
src2 = '/home/mohamm0a/shaheen3.rst'
dst2 = '.'

shutil.copy(src1, dst1)
shutil.copy(src2, dst2)

# Connect to MySQL database
cnx = mysql.connector.connect(user='readthedocs',
                              host='db2.hpc.kaust.edu.sa', password='thisisreadthedocspassword', database='Apps_catalogue')
cursor = cnx.cursor()

# Retrieve data from MySQL database
ibex_query = ("SELECT * FROM Apps")
cursor.execute(ibex_query)
rows = cursor.fetchall()

classifications = ['Compilers', 'Optimized Librarires','Computational Chemistry','Bioscience','Computational Fluid Dynamics','Data Science','Others']
data = []
data_shaheen = []
table = ""
table_shaheen = ""
specific_text = ""

for classification in classifications:
  for row in rows:
    if row[1] == 'Ibex':
      if classification != 'Others':
        if row[6] == classification:
          specific_text = classification
          data_row = [row[2], row[3], row[4], row[5]]
          data.append(data_row)
          table = tabulate(data, headers=['System Build', 'App', 'Version','Compiler'], tablefmt='rst')
      else:
        if row[6] == "":
          specific_text = classification
          data_row = [row[2], row[3], row[4], row[5]]
          data.append(data_row)
          table = tabulate(data, headers=['System Build', 'App', 'Version','Compiler'], tablefmt='rst')
    elif row[1] == 'Shaheen':
      if classification != 'Others':
        if row[6] == classification:
          specific_text = classification
          data_row = [row[2], row[3], row[4], row[5]]
          data_shaheen.append(data_row)
          table_shaheen = tabulate(data_shaheen, headers=['System Build', 'App', 'Version','Compiler'], tablefmt='rst')
      else:
        if row[6] == "":
          specific_text = classification
          data_row = [row[2], row[3], row[4], row[5]]
          data_shaheen.append(data_row)
          table_shaheen = tabulate(data_shaheen, headers=['System Build', 'App', 'Version','Compiler'], tablefmt='rst')

  # Append RST table to file after specific text
  filename = 'ibex.rst'
  with open(filename, 'r+') as f:
       lines = f.readlines()
  # Find the index of the specific text
       index = -1
       for i, line in enumerate(lines):
           if specific_text in line:
               index = i
               break
     # If the specific text is found, insert the table after it without deleting what comes after it
       if index != -1:
           index += 2
           while index < len(lines) and lines[index].startswith('   '):
               index += 1
           lines.insert(index, '\n')
           lines.insert(index + 1, table+'\n')

     # Write the modified list of lines back to the file
           f.seek(0)
           f.writelines(lines)
  data = []
  table = ""

  # Append RST table to file after specific text
  filename = 'shaheen3.rst'
  with open(filename, 'r+') as f:
       lines = f.readlines()
  # Find the index of the specific text
       index = -1
       for i, line in enumerate(lines):
           if specific_text in line:
               index = i
               break
     # If the specific text is found, insert the table after it without deleting what comes after it
       if index != -1:
           index += 2
           while index < len(lines) and lines[index].startswith('   '):
               index += 1
           lines.insert(index, '\n')
           lines.insert(index + 1, table_shaheen+'\n')
     # Write the modified list of lines back to the file
           f.seek(0)
           f.writelines(lines)
  data_shaheen = []
  table_shaheen = ""

# Close database connection
cursor.close()
cnx.close()
