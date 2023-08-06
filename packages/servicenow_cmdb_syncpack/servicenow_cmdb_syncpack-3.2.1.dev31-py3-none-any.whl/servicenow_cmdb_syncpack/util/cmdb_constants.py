RELATION_OVERRIDES = {
    "cmdb_ci_db_mssql_instance": {
        "relations": [
            {
                "parent": "cmdb_ci_win_server",
                "rel_type": "Runs on::Runs",
                "reverse": True,
            }
        ],
        "values": {"sys_class_name": "snow_ci_class", "instance_name": "name"},
    },
    "cmdb_ci_db_mssql_database": {
        "relations": [
            {
                "parent": "cmdb_ci_db_mssql_instance",
                "rel_type": "Contains::Contained by",
                "reverse": False,
            }
        ],
        "values": {"sys_class_name": "snow_ci_class", "database": "name"},
    },
    "cmdb_ci_db_mssql_server": {
        "relations": [
            {
                "parent": "cmdb_ci_win_server",
                "rel_type": "Runs on::Runs",
                "reverse": True,
            }
        ],
        "values": {"sys_class_name": "snow_ci_class", "instance_name": "name"},
    },
}
