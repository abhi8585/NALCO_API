# this is a helper modules containing reusable functions

import configparser

config = configparser.ConfigParser()
config.read('configurations.ini')
print(config.sections())
host = config['Database']['host']
print(host)
# user = config['Database']['user']
# password = config['Database']['password']
# trusted_connection = config['Database']['trusted_connection']
# driver = config['Database']['driver']
# TrustServerCertificate = config['Database']['TrustServerCertificate']
# database_name = config['Database']['database']

# print([host, user , password, trusted_connection, driver, TrustServerCertificate])


# def make_database_connection():
#     import pyodbc
#     cnxn = pyodbc.connect(driver='{FreeTDS}', host=host, database=database_name,
#                         trusted_connection='no', user=user, password=password,
#                         TrustServerCertificate='yes')
#     return cnxn

# make_database_connection()


