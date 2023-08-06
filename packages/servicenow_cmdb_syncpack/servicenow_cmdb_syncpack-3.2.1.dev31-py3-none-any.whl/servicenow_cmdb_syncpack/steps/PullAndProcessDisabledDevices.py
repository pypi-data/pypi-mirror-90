from datetime import datetime, timedelta
from os.path import basename

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon.ipaas_exceptions import MissingRequiredStepParameter
from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascore import parameter_types
from servicenow_cmdb_syncpack.util.cmdb_params import delete_device_vcug_param


class PullAndProcessDisabledDevices(QueryREST):
    def __init__(self):
        super(PullAndProcessDisabledDevices, self).__init__()
        self.friendly_name = "Pull and Process Disabled Devices"
        self.description = "Pulls Disabled Devices from Target VCUG and Generates list of Devices to delete."
        self.version = "1.0.0"

        self.add_step_parameter_from_object(delete_device_vcug_param)
        self.new_step_parameter(
            name="max_age",
            description="Delete Devices over max_age in days. Set 0 for instant.",
            default_value=None,
            required=True,
            param_type=parameter_types.NumberParameter(),
        )
        del self.parameters["relative_url"]
        self.new_step_parameter(
            name="relative_url", param_type=parameter_types.StringParameterShort()
        )

    @staticmethod
    def generate_mysql_query(devices):
        """
        Generate MySQL Query for Child Status or Null Query.

        Args:
            devices (list): List of devices.

        Returns:
            str: SQL Query
        """
        if devices:
            sql = (
                r"SELECT component_did, parent_did, root_did "
                r"FROM master_dev.component_dev_map "
                r"WHERE component_did in ({})"
            ).format(",".join([str(x) for x in devices]))
        else:
            sql = "SELECT null"
        return sql

    def execute(self):
        v_cug = self.get_parameter(delete_device_vcug_param.name, None)
        rel_url = self.parameters.get("relative_url")
        if int(v_cug) == -1:
            cmanager = IpaasContentManager()
            srv_req_vars = cmanager.get_application_dict_from_db(
                "process_discovery_requests"
            ).get("app_variables")
            v_cug = next(
                (
                    x["value"]
                    for x in srv_req_vars
                    if x["name"] == delete_device_vcug_param.name
                )
            )
            if not v_cug:
                raise MissingRequiredStepParameter(
                    "{} is required but is not populated in either {} or in Sync Service Requests".format(
                        delete_device_vcug_param.name, self.application_name
                    )
                )
        rel_url.value = "/api/device?link_disp_field=edit_date&filter.0.collector_group.eq={}".format(
            v_cug
        )
        self.logger.flow("Devices URL: {}".format(rel_url.value))

        max_age = int(self.get_parameter("max_age"))
        if max_age is None:
            raise MissingRequiredStepParameter(
                "Invalid max_age setting: {}. Must be a number.".format(max_age)
            )
        super(PullAndProcessDisabledDevices, self).execute()
        response = self.get_current_saved_data()
        max_timestamp = datetime.now() - timedelta(days=max_age)
        self.logger.debug("max_timestamp: {}".format(max_timestamp))
        del_devices = list()

        for device in response:
            last_edit = datetime.utcfromtimestamp(int(device["description"]))
            self.logger.debug(
                "DID: {}, Last Edit: {}".format(basename(device["URI"]), last_edit)
            )
            if last_edit < max_timestamp:
                del_devices.append(int(basename(device["URI"])))
            else:
                continue

        self.logger.flow(
            "Found {} devices to disable. DIDs: {}".format(
                len(del_devices), del_devices
            )
        )
        self.save_data_for_next_step(
            {
                "mysql_query": self.generate_mysql_query(del_devices),
                "gql_vars": {"search": {"id": {"in": del_devices}}},
                "enabled": True if del_devices else False,
            }
        )
