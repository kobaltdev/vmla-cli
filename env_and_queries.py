# WORKING DIRS
source_dir = "source_files"
extraction_dir = "extracted_files"
reports_dir = "reports"
custom_dir = "custom_searches"

# SETTINGS
verbose_mode = False

# GENEREIC SEARCH EXPRESSIONS
esxi_generic = ["shutdown",
                "Host has booted",
                "Host is rebooting",
                "Exception Type",
                "Hardware errors",
                "Lost network connectivity on virtual switch",
                "esx.problem",
                ]

# vcenter_generic = ["Destroy VM called"]
vcenter_generic = []