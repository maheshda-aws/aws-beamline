SELECT 	order_date, count(*) as count_of_orders
FROM refarch_database.c_orders_output 
WHERE order_date <> '${YYYY}-${MM}-${DD}'
GROUP BY order_date