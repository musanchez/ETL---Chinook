SELECT t.TrackId, t.Name as Track, a.Title as Album, m.Name as MediaType, g.Name as Genre, t.Composer
FROM Track t
LEFT JOIN Album a
ON t.AlbumId = a.AlbumId
LEFT JOIN Genre g
ON g.GenreId = t.GenreId
LEFT JOIN MediaType m
ON m.MediaTypeId = t.MediaTypeId