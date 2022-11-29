import configparser
# from configparser import ConfigParser


def make_database_connection():
    parser = configparser.ConfigParser()
    parser.read(r'app/helpers/connections.cfg')
    database = parser.get(r'database_connection','database_name')
    host = parser.get(r'database_connection','host')
    driver = parser.get(r'database_connection','driver')
    trusted_connection = parser.get(r'database_connection','trusted_connection')
    user = parser.get(r'database_connection','user')
    password = parser.get(r'database_connection','password')
    TrustServerCertificate = parser.get(r'database_connection','TrustServerCertificate')

    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                    trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                    TrustServerCertificate='yes')
    return cnxn



# print(make_database_connection())


# def make_database_connection():
#     import pyodbc
#     cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
#                         trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
#                         TrustServerCertificate='yes')
#     return cnxn

