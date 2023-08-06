message = {
    "MLU_GEN_GROUP": {
        "code": "MLU_GEN"
        , "message": "Group for generic error or warning regarding Metadata Lake Utilities"
        , "level": "INFO"
        , "reference": "Info about location and/or values that lead to the error (non-PII)"
    },
    "ok": {
        "code": "OK"
        , "message": "No errors encountered"
        , "level": "INFO"
        , "reference": "None"
    },
    "not_implemented": {
        "code": "MLU-GEN-000"
        , "message": "Function not yet implemented. Please contact the development team and mention code 'MLU-GEN-000'."
        , "level": "ERROR"
        , "reference": "None"
    },
    "not_found": {
        "code": "MLU-GEN-001"
        , "message": "Could not find what we were looking for"
        , "level": "ERROR"
        , "reference": "None"
    },
    "os_error": {
        "code": "MLU-GEN-002"
        , "message": "An OS error occurred"
        , "level": "ERROR"
        , "reference": "None"
    },
    "undetermined": {
        "code": "MLU-GEN-003"
        , "message": "An unexpected error occurred. Please contact the development team."
        , "level": "ERROR"
        , "reference": "None"
    },
    "main_config_not_found": {
        "code": "MLU-GEN-004"
        , "message": "Main configuration file not found"
        , "level": "FATAL"
        , "reference": "None"
    },
    "azure_secrets_not_found": {
        "code": "MLU-GEN-005"
        , "message": "azure secrets file not found"
        , "level": "FATAL"
        , "reference": "None"
    },
    "file_locations_not_found": {
        "code": "MLU-GEN-006"
        , "message": "file_locations file not found"
        , "level": "ERROR"
        , "reference": "None"
    },
    #
    # file file_handler messages
    #
    "list_directory_error": {
        "code": "MLU-FH-001"
        , "message": "Could not list content of the directory"
        , "level": "ERROR"
        , "reference": "None"
    },
    "copy_files_failed": {
        "code": "MLU-FH-002"
        , "message": "Could not copy files"
        , "level": "ERROR"
        , "reference": "None"
    },
    "remove_files_failed": {
        "code": "MLU-FH-003"
        , "message": "Could not remove files"
        , "level": "ERROR"
        , "reference": "None"
    },
    "check_files_difference_found": {
        "code": "MLU-FH-004"
        , "message": "Differences found"
        , "level": "ERROR"
        , "reference": "None"
    },
    "resource_not_found": {
        "code": "MLU-FH-005"
        , "message": "Resource could not be found"
        , "level": "ERROR"
        , "reference": "None"
    },
    "upload_failed": {
        "code": "MLU-FH-006"
        , "message": "File could not be uploaded"
        , "level": "ERROR"
        , "reference": "None"
    },
    "download_failed": {
        "code": "MLU-FH-007"
        , "message": "File could not be downloaded"
        , "level": "ERROR"
        , "reference": "None"
    },
    "could_not_determine_oldest_folder": {
        "code": "MLU-FH-008"
        , "message": "Could not determine the oldest (based on folder name) folder"
        , "level": "ERROR"
        , "reference": "None"
    },
    "no_files_in_source": {
        "code": "MLU-FH-009"
        , "message": "No files found in folder"
        , "level": "WARNING"
        , "reference": "None"
    },
    #
    # Security related messages
    #
    "unsupported_meta_version_azure_secrets": {
        "code": "MLU-SEC-001"
        , "message": "Incorrect meta_version used in secrets file"
        , "level": "FATAL"
        , "reference": "None"
    },
    #
    # directory handling messages
    #
    "directory_creation_error": {
        "code": "MLU-DIR-001"
        , "message": "Directory could not be created"
        , "level": "ERROR"
        , "reference": "None"
    },
    "directory_removal_error": {
        "code": "MLU-DIR-002"
        , "message": "Directory could not be removed"
        , "level": "ERROR"
        , "reference": "None"
    }
}
