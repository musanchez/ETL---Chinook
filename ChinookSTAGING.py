import pypyodbc

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
    conn = pypyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    
    
    database = 'ChinookSTAGING'
    cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database}') CREATE DATABASE {database}")
    print(f"Se creó la base de datos {database}")
    conn.commit()
    
    create_table_statements = [
        'CREATE TABLE [dbo].[Album]([AlbumId] [int] NOT NULL,[Title] [nvarchar](160) NOT NULL,[ArtistId] [int] NOT NULL)',
        'CREATE TABLE [dbo].[Artist]([ArtistId] [int] NOT NULL,[Name] [nvarchar](120) NULL)',
        'CREATE TABLE [dbo].[Customer]([CustomerId] [int] NOT NULL,[FirstName] [nvarchar](40) NOT NULL,[LastName] [nvarchar](20) NOT NULL,[Company] [nvarchar](80) NULL,[Address] [nvarchar](70) NULL,[City] [nvarchar](40) NULL,[State] [nvarchar](40) NULL,[Country] [nvarchar](40) NULL,[PostalCode] [nvarchar](10) NULL,[Phone] [nvarchar](24) NULL,[Fax] [nvarchar](24) NULL,[Email] [nvarchar](60) NOT NULL,[SupportRepId] [int] NULL)',
        'CREATE TABLE [dbo].[Employee]([EmployeeId] [int] NOT NULL,[LastName] [nvarchar](20) NOT NULL,[FirstName] [nvarchar](20) NOT NULL,[Title] [nvarchar](30) NULL,[ReportsTo] [int] NULL,[BirthDate] [datetime] NULL,[HireDate] [datetime] NULL,[Address] [nvarchar](70) NULL,[City] [nvarchar](40) NULL,[State] [nvarchar](40) NULL,[Country] [nvarchar](40) NULL,[PostalCode] [nvarchar](10) NULL,[Phone] [nvarchar](24) NULL,[Fax] [nvarchar](24) NULL,[Email] [nvarchar](60) NULL)',
        'CREATE TABLE [dbo].[Genre]([GenreId] [int] NOT NULL,[Name] [nvarchar](120) NULL)',
        'CREATE TABLE [dbo].[Invoice]([InvoiceId] [int] NOT NULL,[CustomerId] [int] NOT NULL,[InvoiceDate] [datetime] NOT NULL,[BillingAddress] [nvarchar](70) NULL,[BillingCity] [nvarchar](40) NULL,[BillingState] [nvarchar](40) NULL,[BillingCountry] [nvarchar](40) NULL,[BillingPostalCode] [nvarchar](10) NULL,[Total] [numeric](10, 2) NOT NULL)',
        'CREATE TABLE [dbo].[InvoiceLine]([InvoiceLineId] [int] NOT NULL,[InvoiceId] [int] NOT NULL,[TrackId] [int] NOT NULL,[UnitPrice] [numeric](10, 2) NOT NULL,[Quantity] [int] NOT NULL)',
        'CREATE TABLE [dbo].[MediaType]([MediaTypeId] [int] NOT NULL,[Name] [nvarchar](120) NULL)',
        'CREATE TABLE [dbo].[Playlist]([PlaylistId] [int] NOT NULL,[Name] [nvarchar](120) NULL)',
        'CREATE TABLE [dbo].[PlaylistTrack]([PlaylistId] [int] NOT NULL,[TrackId] [int] NOT NULL)',
        'CREATE TABLE [dbo].[Track]([TrackId] [int] NOT NULL,[Name] [nvarchar](200) NOT NULL,[AlbumId] [int] NULL,[MediaTypeId] [int] NOT NULL,[GenreId] [int] NULL,[Composer] [nvarchar](220) NULL,[Milliseconds] [int] NOT NULL,[Bytes] [int] NULL,[UnitPrice] [numeric](10, 2) NOT NULL)'
    ]
    
    cursor.execute(f"USE {database}")
    conn.commit()
    table_list = ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
    
    drop_table_statements = [f"DROP TABLE {table}" for table in table_list]
    condition_drop_statements = [f"IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}')" for table in table_list]
    
    complete_statements = [f"{condition} {drop}" for condition, drop in zip(condition_drop_statements, drop_table_statements)]

    cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'ChinookSTAGING'")
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
            
    with open('table_count.txt', 'w') as file:
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

    
except pypyodbc.Error as e:
    print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")


finally:
    if 'conn' in locals():
        conn.close()
    if 'cursor' in locals():
        cursor.close()
    print("Conexión cerrada")