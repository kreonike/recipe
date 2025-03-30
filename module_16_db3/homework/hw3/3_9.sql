SELECT DISTINCT p.maker
FROM Product p
JOIN PC pc ON p.model = pc.model
WHERE p.type = 'PC'
  AND pc.speed >= 450;