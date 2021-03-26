import pyodbc


conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=MSI;"
    "Database=customers;"
    "Trusted_Connection=yes;"
)
u_name = ''
crsr=conn.cursor()
query = f"Select id from Publishers where u_name= 'vendor@me'"
crsr=conn.cursor()
u_name=crsr.execute(query)

for i in u_name:
    print(i[0])