-- Get data from SB1
SELECT
*
FROM StationDescription SD
	INNER JOIN SensorLocationDescription SLD
		ON SD.`_oid` = SLD.`_parent_oid`
	LEFT JOIN NetworkDescription ND
		ON SD.`_parent_oid` = ND.`_oid`
	LEFT JOIN BoreHole BH
		ON SD.`_oid` = BH.`_parent_oid`