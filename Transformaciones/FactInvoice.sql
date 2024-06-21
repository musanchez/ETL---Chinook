SELECT i.InvoiceId, il.TrackId, c.CustomerId, i.InvoiceDate ,i.BillingAddress, i.BillingCity, i.BillingState, i.BillingCountry, i.BillingPostalCode,
il.UnitPrice, il.Quantity, i.Total
FROM Invoice i
LEFT JOIN InvoiceLine il
ON i.InvoiceId = il.InvoiceId
LEFT JOIN Customer c
ON c.CustomerId = i.CustomerId
LEFT JOIN Track t
ON t.TrackId = il.TrackId