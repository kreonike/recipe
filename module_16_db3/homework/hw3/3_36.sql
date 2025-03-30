SELECT DISTINCT
    CASE
        WHEN s.name IS NOT NULL THEN c.class
        ELSE o.ship
    END AS head_ship
FROM Classes c
LEFT JOIN Ships s ON c.class = s.name
LEFT JOIN Outcomes o ON c.class = o.ship AND o.ship NOT IN (SELECT name FROM Ships)
WHERE c.class = s.name OR (o.ship IS NOT NULL AND s.name IS NULL);