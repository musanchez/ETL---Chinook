import pyodbc

# Configurar la conexión
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'localhost'
DATABASE_NAME = 'master'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
try:
    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    
    
    database = 'ChinookDW'
    cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database}') CREATE DATABASE {database}")
    print(f"Se creó la base de datos {database}")
    conn.commit()
    
    create_table_statements = [
    f"""
    CREATE TABLE DimEmployee
    (
	    EmployeeId INT PRIMARY KEY,
	    Name NVARCHAR(70),
	    Title NVARCHAR(30)
    )
    """,
    f"""
    CREATE TABLE DimCustomer
    (
        CustomerId INT PRIMARY KEY,
        Name NVARCHAR(70),
        Company NVARCHAR(70),
        Address NVARCHAR(100),
        City NVARCHAR(40),
        State NVARCHAR(40),
        Country NVARCHAR(40),
        EmployeeId INT,
        FOREIGN KEY (EmployeeId) REFERENCES DimEmployee(EmployeeId)
    )
    """,
    f"""
    CREATE TABLE DimTrack
    (
        TrackId INT PRIMARY KEY,
        Track NVARCHAR(200),
        Album NVARCHAR(200),
        MediaType NVARCHAR(120),
        Genre NVARCHAR(120),
        Composer NVARCHAR(220)
    )
    """,
    f"""
    CREATE TABLE FactInvoice
    (
        InvoiceId INT,
        TrackId INT,
        CustomerId INT,
        FOREIGN KEY (TrackId) REFERENCES DimTrack(TrackId),
        FOREIGN KEY (CustomerId) REFERENCES DimCustomer(CustomerId),
        InvoiceDate DATETIME,
        BillingAddress NVARCHAR(70),
        BillingCity NVARCHAR(40),
        BillingState NVARCHAR(40),
        BillingCountry NVARCHAR(40),
        BillingPostalCode NVARCHAR(10),
        UnitPrice DECIMAL(10, 2),
        Quantity INT,
        TOTAL DECIMAL(10, 2)
    )
    """   
    ]
    
    cursor.execute(f"USE {database}")
    conn.commit()
    table_list = ['FactInvoice', 'DimTrack', 'DimCustomer', 'DimEmployee']
    
    drop_table_statements = [f"DROP TABLE {table}" for table in table_list]
    condition_drop_statements = [f"IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}')" for table in table_list]
    
    complete_statements = [f"{condition} {drop}" for condition, drop in zip(condition_drop_statements, drop_table_statements)]

    cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'ChinookDW'")
    exists = cursor.fetchone()[0]
    
    table_count = 0

    if exists:
        for statement in complete_statements:
            cursor.execute(statement)
            conn.commit()

        for statement in create_table_statements:
            cursor.execute(statement)
            conn.commit()
            table_count += 1
            
    with open('table_count_DW.txt', 'w') as file:
        file.write(f"Se crearon {table_count} tablas en la base de datos {database}")
        
        tables_sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        cursor.execute(tables_sql)
        tables = cursor.fetchall()
            
        for table in tables:
            table_name = table[0]
            file.write(f"\nTabla: {table_name}")
        
            columns_info_sql = f"""
        SELECT 
            COLUMN_NAME, 
            DATA_TYPE, 
            CHARACTER_MAXIMUM_LENGTH 
        FROM 
            INFORMATION_SCHEMA.COLUMNS 
        WHERE 
            TABLE_NAME = '{table_name}'
        """
            cursor.execute(columns_info_sql)
            columns_info = cursor.fetchall()

            for column in columns_info:
                column_name, data_type, max_length = column
                file.write(f"    Columna: {column_name}, Tipo de dato: {data_type}, Longitud máxima: {max_length}")

    
except pyodbc.Error as e:
    print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")


finally:
    cursor.close()
    conn.close()
    print("Conexión cerrada")