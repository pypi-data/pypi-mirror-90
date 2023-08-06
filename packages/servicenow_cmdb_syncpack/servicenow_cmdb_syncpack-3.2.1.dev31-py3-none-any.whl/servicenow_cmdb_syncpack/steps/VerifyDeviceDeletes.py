from ipaascore.BaseStep import BaseStep


class VerifyDeviceDeletes(BaseStep):
    def __init__(self):
        self.friendly_name = "Verify Device Delete Requests"
        self.description = (
            "Verifies Device Delete Requests and Generates SL1 API payloads."
        )
        self.version = "1.0.0"

    def reformat_sql_query_response(self):
        mysql_data = self.get_data_from_step_by_name(
            "Pull Affected Device Info from SL1 (MySQL)"
        )
        data = dict()
        if mysql_data:
            for row in mysql_data:
                data[int(row["component_did"])] = row
        return data

    def execute(self):
        gql_data = self.get_data_from_step_by_name(
            "Pull Affected Device Info from SL1 (GQL)"
        )
        del_set = set()
        root_set = set()
        if gql_data:
            sql_data = self.reformat_sql_query_response()
            for raw_device in gql_data:
                device = raw_device['device']
                if len(device["componentDescendants"]["edges"]) > 0:
                    cug_set = set()
                    cug_set.add(device["collectorGroup"]["id"])
                    for child in device["componentDescendants"]["edges"]:
                        cug_set.add(child['child']["collectorGroup"]["id"])
                    if len(cug_set) > 1:
                        self.logger.warning(
                            "Unable to delete DID: {} as it has children who are not all "
                            "in the same collector group. Skipping.".format(
                                device["id"]
                            )
                        )
                        self.logger.debug(
                            "Device Details: {}".format(device)
                        )
                        continue
                    else:
                        for child in device["componentDescendants"]["edges"]:
                            del_set.add(int(child['child']['id']))
                    if sql_data.get(device["id"]) is None:
                        root_set.add(int(device['id']))
                    pass
                else:
                    del_set.add(int(device["id"]))
            del_devices = list(del_set)
            del_devices.extend(root_set)
            self.logger.flow(
                "Deleting {} devices.".format(len(del_devices))
            )
            self.save_data_for_next_step(del_devices)
        else:
            self.logger.flow("No Devices to Delete")
            self.save_data_for_next_step(list())
