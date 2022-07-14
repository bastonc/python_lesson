def get_full_info_track():
	return """
           SELECT artists.Name AS Artist,
              tracks.Name AS Track,
              strftime("%M:%S", tracks.Milliseconds/1000, "unixepoch") as Lenght,
              albums.Title AS Album,
              tracks.Composer AS Composer,
              genres.Name AS Genres,
              tracks.Bytes AS Bytes,
              media_types.Name AS "Media types",
              tracks.UnitPrice AS Price,
              SUM(invoice_items.Quantity) AS Quantity,
              tracks.UnitPrice  * sum(invoice_items.Quantity)
           FROM tracks LEFT JOIN albums ON tracks.AlbumId = albums.AlbumId
           LEFT JOIN artists ON albums.ArtistId = artists.ArtistId
           LEFT JOIN genres ON tracks.GenreId = genres.GenreId
           LEFT JOIN media_types ON tracks.MediaTypeId = media_types.MediaTypeId
           LEFT JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
        """


def get_time_all_tracks():
	return """ SELECT	strftime("%H:%M:%S", sum(tracks.Milliseconds) / 1000, "unixepoch") as Lenght
			   FROM tracks 
		"""


def get_total_sale():
	return """ SELECT BillingCountry, ROUND(SUM(Total), 2) FROM invoices
		"""

def get_city_popular_genre():
	return """ SELECT  g.Name, i.BillingCity, COUNT(*) AS Result
				FROM tracks
				JOIN genres g on tracks.GenreId = g.GenreId
				JOIN invoice_items ii on tracks.GenreId = ii.TrackId
				JOIN invoices i on ii.InvoiceId = i.InvoiceId
				GROUP BY i.BillingCity, g.Name
				HAVING  g.Name == ?
				ORDER BY Result LIMIT 1;
	
	"""