def getModelData():
	modelDictionary={
		"US_ANA":{
			"shapefiles":"Shapefiles/US_baby",
			"countryCode":"US",
			"imgHeight":321,
			"imgWidth":598,
			"imgDepth":23,
			"areaCode":"KT",
			"refFiles":"RefFiles/Refclipped_US",
			"statistics":"statistics/STATS_US_ALL_WHEAT_2000_2020.csv",
			"fieldcrop":"WHEAT"
		},
		"US_South_spatial":{
			"shapefilesAB":"Shapefiles/ABshapefiles",
			"countryCode":"US",
			"imgHeight":544,
			"imgWidth":993,
			"imgDepth":23,
			"areaCode":"KaTxNmCo",
			"refFiles":"RefFiles/Refclipped_South_A",
			"statistics":"statistics/STATS_US_ALL_WHEAT_2000_2020.csv",
			"fieldcrop":"WHEAT"
	}}

	return modelDictionary
