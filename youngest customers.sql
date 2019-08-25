/* SQL 1 */
SELECT name
FROM customer c
LEFT JOIN (select max(dob) as mdob from customer) mtable ON mtable.mdob = c.dob
where mtable.mdob is not null;

/* SQL 2 */
SELECT name
FROM customer
WHERE dob = (select max(dob) from customer)
 