import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=MSI;"
    "Database=customers;"
    "Trusted_Connection=yes;"
)

def 