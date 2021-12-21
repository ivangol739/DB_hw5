import sqlalchemy

db = 'postgresql://ivangol739:********@localhost:5432/music'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

# s1 = connection.execute("""
# SELECT album_name, album_year FROM album
# WHERE album_year = 2018;
# """).fetchall()
#
# s2 = connection.execute("""
# SELECT track_name, track_duration FROM track
# ORDER BY track_duration DESC;
# """).fetchmany(1)
#
# s3 = connection.execute("""
# SELECT track_name FROM track
# WHERE track_duration >= 3.5 * 60;
# """).fetchall()
#
# s4 = connection.execute("""
# SELECT collection_name FROM collection
# WHERE collection_year BETWEEN 2018 AND 2020;
# """).fetchall()
#
# s5 = connection.execute("""
# SELECT performer_name FROM performer
# WHERE performer_name NOT LIKE '%% %%';
# """).fetchall()
#
# s6 = connection.execute("""
# SELECT track_name FROM track
# WHERE track_name LIKE '%%My%%' OR track_name LIKE '%%Мой%%';
# """).fetchall()

s7 = connection.execute("""
SELECT a.genre_name, COUNT(performer_id) FROM genre a
LEFT JOIN performer_genre b ON a.genre_id = b.genre_id
GROUP BY a.genre_name;
""").fetchall()

s8 = connection.execute("""
SELECT b.album_name, b.album_year, COUNT(track_id) FROM track a
LEFT JOIN album b ON a.album_id = b.album_id
WHERE b.album_year BETWEEN 2019 AND 2020
GROUP BY b.album_name, b.album_year
""").fetchall()

s9 = connection.execute("""
SELECT a.album_name, ROUND(AVG(b.track_duration)) FROM album a
LEFT JOIN track b ON a.album_id = b.track_id
GROUP BY a.album_name;
""").fetchall()

s10 = connection.execute("""
SELECT performer_name
FROM (SELECT * FROM album WHERE album_year <> 2020) a
LEFT JOIN performer_album b
	ON a.album_id = b.album_id
LEFT JOIN performer c
	ON b.performer_id = c.performer_id;
""").fetchall()

s11 = connection.execute("""
SELECT collection_name FROM collection a
LEFT JOIN collection_track b
    ON a.collection_id = b.collection_id
LEFT JOIN track c
    ON b.track_id = c.track_id
LEFT JOIN performer_album d
    ON d.album_id = c.album_id
LEFT JOIN performer e
    ON d.performer_id = e.performer_id
WHERE e.performer_name = 'KiSH';
""").fetchall()

s12 = connection.execute("""
SELECT album_name FROM album a
LEFT JOIN performer_album b
    ON a.album_id = b.album_id
LEFT JOIN performer c
    ON b.performer_id = c.performer_id
LEFT JOIN performer_genre d
    ON c.performer_id = d.performer_id
GROUP BY album_name 
HAVING count(genre_id) > 1;
""").fetchall()

s13 = connection.execute("""
SELECT track_name FROM track a
LEFT JOIN collection_track b
    ON a.track_id = b.track_id
WHERE b.collection_id IS NULL;
""").fetchall()

s14 = connection.execute("""
SELECT d.performer_name FROM track a
LEFT JOIN album b
    ON a.album_id = b.album_id
LEFT JOIN performer_album c
    ON b.album_id = c.album_id 
LEFT JOIN performer d
    ON c.performer_id = d.performer_id
WHERE a.track_duration = (
    SELECT MIN(a.track_duration) FROM track a);
""").fetchall()

s15 = connection.execute("""
SELECT a.album_name, count(b.track_id) FROM album a
LEFT JOIN track b
	ON a.album_id = b.album_id
GROUP BY a.album_name
HAVING count(b.track_id) = 
				(SELECT count(d.track_id)
					FROM album c
				LEFT JOIN track d
					ON c.album_id = d.album_id
				GROUP BY c.album_name
				ORDER BY count(d.track_id) ASC
				LIMIT 1)
""").fetchall()
print(s15)
