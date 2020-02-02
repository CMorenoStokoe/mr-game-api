#Populate this datafile with list of mrbaseIds of nodes you are specifying custom activation default, min and max values for (inCDs) and specify these values in dictionary (CDS)
inCDS = [
            "22",
            "1187",
            "UKB-b:6519",
            "UKB-b:5779",
            "961",
            "UKB-b:1585",
            "UKB-b:4779",
            "UKB-b:17999",
            "1239",
            "UKB-b:19953",
            "UKB-b:4710",
            "UKB-b:4077",
            "1189",
            "UKB-b:5238",
        ]

CDS = { 
        "22" : {
                    "activation" : 0.002,
                    "activation_min" : 0,
                    "activation_max" : 1,
                    "negative" : "False",
                    "units" : "Log odds",
                    "units_type" : "float",
                    "units_mapping" : None
        },
        "1187": {
                    "activation" : 0.04,
                    "activation_min" : 0,
                    "activation_max" : 1,
                    "negative" : "False",
                    "units" : "Prevalence (%)",
                    "units_type" : "binary",
                    "units_mapping" : None
        },
        "UKB-b:6519": {
                    "activation" : 0.75,
                    "activation_min" : 0,
                    "activation_max" : 1,
                    "negative" : "False",
                    "units" : "Prevalence (%)",
                    "units_type" : "binary",
                    "units_mapping" : None
        },
        "UKB-b:5779": {
                    "activation" : 0.2,
                    "activation_min" : 6,
                    "activation_max" : 1,
                    "negative" : "True",
                    "units" : "Category",
                    "units_type" : "nominal",
                    "units_mapping" : {
                        1:	"Daily or almost daily", 
                        2:	"Three or four times a week",
                        3:	"Once or twice a week",
                        4:	"One to three times a month",
                        5:	"Special occasions only",
                        6:	"Never"
                    }
        },
        "961": {
                    "activation" : 1.5,
                    "activation_min" : 0,
                    "activation_max" : 145,
                    "negative" : "False",
                    "units" : "Cigarettes per day",
                    "units_type" : "float",
                    "units_mapping" : None
        },
        "UKB-b:1585": {
                    "activation" : 0.1,
                    "activation_min" : 0,
                    "activation_max" : 1,
                    "negative" : "False",
                    "units" : "Prevalence (%)",
                    "units_type" : "binary",
                    "units_mapping" : None
        },
        "UKB-b:4779": {
                    "activation" : 0.25,
                    "activation_min" : 0,
                    "activation_max" : 2,
                    "negative" : "False",
                    "units" : "Category",
                    "units_type" : "nominal",
                    "units_mapping" : {
                        0:"Never/rarely",
                        1:"Sometimes",
                        2:"Often",
                    }
        },
        "UKB-b:17999": {
                    "activation" : 1.95,
                    "activation_min" : 0,
                    "activation_max" : 5,
                    "negative" : "False",
                    "units" : "Category",
                    "units_type" : "nominal",
                    "units_mapping" : {
                        0:"Less than 5mins",
                        1:"5-29 mins",
                        2:"30-59 mins",
                        3:"1-3 hours",
                        4:"4-6 hours",
                        5:"More than 6 hours",
                    }
        },
        "1239": {
                    "activation" : 17,
                    "activation_min" : 12,
                    "activation_max" : 25,
                    "negative" : "False",
                    "units" : "Years",
                    "units_type" : "float",
                    "units_mapping" : None
        },
        "UKB-b:19953": {
                    "activation" : 27,
                    "activation_min" : 10,
                    "activation_max" : 70,
                    "negative" : "False",
                    "units" : "Units",
                    "units_type" : "float",
                    "units_mapping" : None
        },
        "UKB-b:4710": {
                    "activation" : 3,
                    "activation_min" : 0,
                    "activation_max" : 7,
                    "negative" : "False",
                    "units" : "Days per week",
                    "units_type" : "int",
                    "units_mapping" : None
        },
        "UKB-b:4077": {
                    "activation" : 0.75,
                    "activation_min" : 0,
                    "activation_max" : 1,
                    "negative" : "False",
                    "units" : "Prevalence (%)",
                    "units_type" : "binary",
                    "units_mapping" : None
        },
        "1189": {
                    "activation" : 0.002,
                    "activation_min" : 0,
                    "activation_max" : 1,
                    "negative" : "False",
                    "units" : "Prevalence (%)",
                    "units_type" : "binary",
                    "units_mapping" : None
        },
        "UKB-b:5238": {
                    "activation" : 6,
                    "activation_min" : 0,
                    "activation_max" : 13,
                    "negative" : "False",
                    "units" : "Test score",
                    "units_type" : "int",
                    "units_mapping" : None
        },
}