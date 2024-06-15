SELECT i.InvoiceId, i.InvoiceDate, i.BillingAddress, i.BillingCity, i.BillingState, i.BillingCountry, i.BillingPostalCode,
il.UnitPrice, il.Quantity, i.Total, c.CustomerId
FROM Invoice i
LEFT JOIN InvoiceLine il
ON i.InvoiceId = il.InvoiceId
LEFT JOIN Customer c
ON c.CustomerId = i.CustomerId