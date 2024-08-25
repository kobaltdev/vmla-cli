# WORKING DIRS
source_dir = "source_files"
extraction_dir = "extracted_files"
reports_dir = "reports"


# SEARCH EXPRESSIONS
esxi_hardware = ["shutdown",
                "Host has booted",
                "Host is rebooting",
                "Exception Type",
                "VeeamProxyOVH1",
                "Hardware errors",
                "Lost network connectivity on virtual switch",
                "esx.problem",
                "smartd:"
                ]

vcenter_expressions = ["testlog",
                       "srvtest_ansible"]