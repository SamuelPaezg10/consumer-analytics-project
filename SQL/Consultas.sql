
-- IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'consumer_analytics')
-- Esta función de arriba es para automatizar la creación debases de datos.


CREATE DATABASE consumer_analytics
;
USE consumer_analytics
;

SELECT
    *
FROM dbo.consumer_data
WHERE customer_id = 547
;

--1-- ¿Qué porcentaje de clientes compró cada producto?

WITH Clientes_unicos AS (
    SELECT
        product,
        COUNT(DISTINCT customer_id) AS [Clientes unicos]
    FROM dbo.consumer_data
    GROUP BY product
),
total_clientes As (
    SELECT
        product,
        COUNT(customer_id) AS [Total clientes]
    FROM dbo.consumer_data
    GROUP BY product
)
SELECT
    cu.product,
    cu.[Clientes unicos],
    tc.[Total clientes],
    (cu.[Clientes unicos] * 1.0 /tc.[Total clientes]) *100 AS PCt
FROM Clientes_unicos cu
JOIN total_clientes tc
    ON cu.product = tc.product
;

--2-- ¿Cuántas compras hace en promedio un cliente?

WITH Compras_Cliente AS (
    SELECT
        customer_id,
        COUNT(customer_id) AS [Compras Por Cliente]
    FROM dbo.consumer_data
    GROUP BY customer_id
)
SELECT
    AVG([Compras Por Cliente]) AS [Promedio Por Cliente]
FROM Compras_Cliente
;


--3-- ¿Cuánto gasta en promedio un cliente?

WITH Total_Consumer AS (
    SELECT
        customer_id,
        SUM(sales) AS [Ventas por cliente]
    FROM dbo.consumer_data
    GROUP BY customer_id
)
SELECT
    ROUND(AVG([Ventas por cliente]), 4) AS [Promedio Por Cliente]
FROM Total_Consumer tc
;

--4-- ¿Cuáles son el top´10 clientes que mas gastan?

WITH Clientes AS (
    SELECT
        customer_id,
        COUNT(customer_id) AS [Total Compras],
        SUM(sales) AS [Sales Por Cliente]
    FROM dbo.consumer_data
    GROUP BY customer_id
),
Rank AS (
    SELECT
    customer_id,
        RANK() OVER (
            ORDER BY [Sales Por Cliente] DESC
        ) AS Rn
    FROM Clientes
)
SELECT
    c.customer_id,
    c.[Total Compras],
    c.[Sales Por Cliente],
    r.Rn
FROM Clientes c
JOIN Rank r
    ON r.customer_id = c.customer_id
WHERE rn < 11
ORDER BY rn ASC
;

--5-- Clasificar clientes en - VIP (5%) y Normal

WITH Gasto_Cliente AS (
    SELECT
        customer_id,
        SUM(sales) AS total_gasto
    FROM dbo.consumer_data
    GROUP BY customer_id
),
Ranking AS (
    SELECT
        customer_id,
        total_gasto,
        NTILE(80) OVER 
        (ORDER BY total_gasto DESC
        ) AS percentil
    FROM Gasto_Cliente
)
SELECT
    customer_id,
    total_gasto,
    CASE
        WHEN percentil = 1 THEN 'VIP'
        ELSE 'Normal'
    END AS segmento
FROM Ranking
;