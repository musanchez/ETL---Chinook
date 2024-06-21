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
    
    origen = 'ChinookLANDING'
    destino = 'ChinookDW'
    
    #Llenamos la tabla DimEmployee
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
    
    #LLenamos la tabla de DimCustomer
    cursor.execute(f"USE {origen}")
    cursor.execute(f"""
    SELECT CustomerId, (FirstName + ' ' + LastName) as Name, Company, Address, City, State, Country, SupportRepId as EmployeeId
    FROM Customer
    """)
    data = cursor.fetchall()
    
    for row in data:
        cursor.execute(f"USE {destino}")
        modified = tuple(row)
        insert_query = f"INSERT INTO DimCustomer VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # Insertamos la fila en la tabla de destino
        cursor.execute(insert_query, modified)
        
        
    #Llenamos la tabla DimTrack
    cursor.execute(f"USE {origen}")
    cursor.execute(f"""
    SELECT t.TrackId, t.Name as Track, a.Title as Album, m.Name as MediaType, g.Name as Genre, t.Composer
    FROM Track t
    LEFT JOIN Album a
    ON t.AlbumId = a.AlbumId
    LEFT JOIN Genre g
    ON g.GenreId = t.GenreId
    LEFT JOIN MediaType m
    ON m.MediaTypeId = t.MediaTypeId
    """)
    data = cursor.fetchall()
    for row in data:
        cursor.execute(f"USE {destino}")
        modified = tuple(row)
        insert_query = "INSERT INTO DimTrack VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(insert_query, modified)
    
        
    
    #Llenamos la tabla FactInvoice
    cursor.execute(f"USE {origen}")
    cursor.execute(f"""
    SELECT i.InvoiceId, il.TrackId, c.CustomerId, i.InvoiceDate ,i.BillingAddress, i.BillingCity, i.BillingState, i.BillingCountry, i.BillingPostalCode,
    il.UnitPrice, il.Quantity, i.Total
    FROM Invoice i
    LEFT JOIN InvoiceLine il
    ON i.InvoiceId = il.InvoiceId
    LEFT JOIN Customer c
    ON c.CustomerId = i.CustomerId
    LEFT JOIN Track t
    ON t.TrackId = il.TrackId
    """
    )
    data = cursor.fetchall()
    for row in data:
        cursor.execute(f"USE {destino}")
        modified = tuple(row)
        insert_query = "INSERT INTO FactInvoice VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(insert_query, modified)  

except pyodbc.Error as e:
    print(f"Error en la conexión: {e}")
    
finally:
    cursor.close()
    conn.close()