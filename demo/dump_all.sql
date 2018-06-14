SELECT
    minidump.id 					AS minidump_id,
    minidump.timestamp 				AS minidump_timestamp,
	minidump.product_id				AS product_id,
	minidump.crash_id				AS crashs_id,
	minidump.signature 				AS minidump_signature, 
	minidump.build 					AS minidump_build,
	minidump.system_info 			AS minidump_system_info, 
	minidump.name 					AS minidump_name, 
	minidump.minidump 				AS minidump_minidump,
	minidump.data 					AS minidump_data,
	product.name 					AS product_name,
	product.version 				AS product_version,
	crashs.count 					AS crashs_count, 
	crashs.name 					AS crashs_name,
	crashs.signature 				AS crashs_signature,
	crashs.created 					AS crashs_created,
	crashs.updated 					AS crashs_updated
FROM
	minidump
INNER JOIN crashs
    ON minidump.crash_id = crashs.id 
INNER JOIN product
    ON minidump.product_id = product.id 