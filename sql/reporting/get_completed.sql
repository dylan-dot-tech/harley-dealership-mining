-- Author: https://dylan.tech

SELECT
	(SELECT count(*) FROM dealers) AS dealers_added,
	sum(CASE WHEN search_completed=1 THEN 1 ELSE 0 END) AS zip_completed,
	count(*) AS zip_total
FROM zip_codes;
