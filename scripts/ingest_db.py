import os
import json
import mysql.connector
import subprocess

# Connect to the MySQL database
mysql_connect = mysql.connector.connect(user='root',
                              host='localhost', database='catalogue')
cursor = mysql_connect.cursor()

# Delete previously insterted data
delete_query = "DELETE FROM apps"
cursor.execute(delete_query)
mysql_connect.commit()

# Open JSON files
apps_catalogue_path='/user-docs/apps_json'
for file in os.listdir(apps_catalogue_path):
    if file.endswith('.json'):
        with open(os.path.join(apps_catalogue_path, file), 'r') as f:
            data = json.load(f)

        # Insert each data into the MySQ table
        system_name = data['system_name']
        system_build_ver = data['system_build_ver']
        app_name = data['app_name']
        app_version = data['app_version']
        app_compiler_ver = data['app_compiler_ver']
        classification = data['app_classification']
        description = data['description']

        record = "INSERT INTO apps (system_name,system_build_ver,app_name,app_ver,compiler_ver,classification,description) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(record, (system_name,system_build_ver,app_name,app_version,app_compiler_ver,classification,description))

update_query = "UPDATE apps t1 JOIN pre_class t2 ON t1.app_name = t2.app_name SET t1.classification = t2.classification"
cursor.execute(update_query)
mysql_connect.commit()

mysql_connect.commit()
cursor.close()
mysql_connect.close()

# Database backup

backup_cmd=f'mysqldump -u root catalogue > /user-docs/apps-catalogue/catalogue-db.sql'
subprocess.run(backup_cmd, shell=True)
