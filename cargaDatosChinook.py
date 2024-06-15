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
    
    origen = 'Chinook'
    destino = 'ChinookSTAGING'
    
    cursor.execute(f"USE {origen}")
    cursor.execute("SELECT name FROM sys.tables")  # Solo necesitamos los nombres de las tablas
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"Migrando tabla {table_name}...")
        
        cursor.execute(f"USE {origen}")
        # Recorremos tomando todos los datos de cada tabla
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        cursor.commit()
        print(f"Se encontraron {len(data)} registros en la tabla {table_name}.")
        
        # Cambiamos a la base de datos de destino
        cursor.execute(f"USE {destino}")
        
        for row in data:
            # Generamos la consulta de inserción con placeholders (?)
            placeholders = ', '.join(['?' for _ in range(len(row))])
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            # Insertamos la fila en la tabla de destino
            cursor.execute(insert_query, row)
        
        print(f"Tabla {table_name} migrada correctamente.")
    
    print("Datos migrados correctamente.")

except pyodbc.Error as e:
    print(f"Error en la conexión: {e}")
