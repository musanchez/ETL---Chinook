CREATE TABLE DimEmployee
(
	EmployeeId INT PRIMARY KEY,
	Name NVARCHAR(70),
	Title NVARCHAR(30)
)

CREATE TABLE DimCustomer
(
	CustomerId INT PRIMARY KEY,
	Name NVARCHAR(70),
	Company NVARCHAR(70),
	Street NVARCHAR(100),
	City NVARCHAR(40),
	State NVARCHAR(40),
	Country NVARCHAR(40),
	EmployeeId INT,
	FOREIGN KEY (EmployeeId) REFERENCES DimEmployee(EmployeeId)
)

CREATE TABLE DimTrack
(
	TrackId INT PRIMARY KEY,
	Track NVARCHAR(200),
	Album NVARCHAR(200),
	MediaType NVARCHAR(120),
	Genre NVARCHAR(120),
	Composer NVARCHAR(220)
)

CREATE TABLE FactInvoice
(
	InvoiceId INT,
	TrackId INT,
	CustomerId INT,
	FOREIGN KEY (TrackId) REFERENCES DimTrack(TrackId),
	FOREIGN KEY (CustomerId) REFERENCES DimCustomer(CustomerId),
	InvoiceDate DATETIME
	BillingAddress NVARCHAR(70),
	BillingCity NVARCHAR(40),
	BillingState NVARCHAR(40),
	BillingCountry NVARCHAR(40),
	BillingPostalCode NVARCHAR(10),
	UnitPrice DECIMAL(10, 2),
	Quantity INT,
	Total DECIMAL(10, 2)
)
