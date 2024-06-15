import pyodbc

# Configurar la conexión
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'localhost'
DATABASE_NAME = 'master'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

try:
    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    
    origen = 'ChinookSTAGING'
    destino = 'ChinookDW'
    
    cursor.execute(f"USE {origen}")
    
    #LLenamos la tabla de dimCustomer
    cursor.execute("SELECT * FROM Customer")
    data = cursor.fetchall()
    
    for row in data:
        cursor.execute(f"USE {destino}")
        customer_id = row[0]
        name = f"{row[1]} {row[2]}"
        street = row[3]
        company = row[4]
        city = row[5]
        state = row[6]
        country = row[7]
        modified = (customer_id, name, street, company, city, state, country)
        insert_query = f"INSERT INTO DimCustomer VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Insertamos la fila en la tabla de destino
        cursor.execute(insert_query, modified)
    
    #Llenamos la tabla Employee
    cursor.execute(f"USE {origen}")
    cursor.execute("SELECT * FROM Employee")
    data = cursor.fetchall()
    
    for row in data:
        cursor.execute(f"USE {destino}")
        employee_id = row[0]
        name = f"{row[2]} {row[1]}"
        title = row[3]
        modified = (employee_id, name, title)
        insert_query = f"INSERT INTO DimEmployee VALUES (?, ?, ?)"
        cursor.execute(insert_query, modified)
        
    #Llenamos la tabla DimTrack
    
    cursor.execute(f"USE {origen}")
    
        
    

except pyodbc.Error as e:
    print(f"Error en la conexión: {e}")
    
finally:
    cursor.close()
    conn.close()