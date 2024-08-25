# WORKING DIRS
source_dir = "source_files"
extraction_dir = "extracted_files"
reports_dir = "reports"


# SEARCH EXPRESSIONS
host_expressions = ["shutdown",
                    "Failed to resolve localhost IP address",
                    "Unable to stat VM config file",
                    "LoadFromConfig translated error to vim.fault.FileNotFound",
                    "Host has booted"]

vcenter_expressions = ["testlog",
                       "srvtest_ansible"]