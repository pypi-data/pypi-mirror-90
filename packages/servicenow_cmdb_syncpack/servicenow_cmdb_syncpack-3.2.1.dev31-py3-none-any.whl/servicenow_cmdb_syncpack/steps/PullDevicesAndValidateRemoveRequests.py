from base_steps_syncpack.steps.QueryGQL import QueryGQL
from ipaascommon.ipaas_utils import str_to_bool
from ipaascore import parameter_types
from servicenow_cmdb_syncpack.util.cmdb_params import (
    service_request_failed_param, service_request_in_progress_param,
    service_request_success_param, service_request_sys_id_param,
    service_request_vcug_param
)


class PullDevicesAndValidateRemoveRequests(QueryGQL):
    def __init__(self):
        super(PullDevicesAndValidateRemoveRequests, self).__init__()
        self.friendly_name = "Pull Devices and Validate Delete Requests"
        self.description = (
            "Validates Delete Requests and generates queries and responses."
        )
        self.version = "1.0.0"

        self.add_step_parameter_from_object(service_request_sys_id_param)
        self.add_step_parameter_from_object(service_request_in_progress_param)
        self.add_step_parameter_from_object(service_request_failed_param)
        self.add_step_parameter_from_object(service_request_success_param)
        self.add_step_parameter_from_object(service_request_vcug_param)
        self.new_step_parameter(
            name="recursively_disable_children",
            description="Should this app Recursively Disable children of the target device or Skip.",
            required=False,
            default_value=False,
            param_type=parameter_types.BoolParameterCheckbox(),
        )

    @staticmethod
    def reformat_sql_data(sql_data):
        reformatted_data = dict()
        for row in sql_data:
            reformatted_data[row["component_did"]] = row
        return reformatted_data

    def process_devices(self):
        disable_children = str_to_bool(
            self.get_parameter("recursively_disable_children")
        )
        device_data = self.get_current_saved_data()

        error_devices = list()
        del_devices = list()

        for raw_device in device_data:
            device = raw_device.get("device")

            if device["componentDescendants"]["edges"]:
                # Device has children
                children = [x["child"] for x in device["componentDescendants"]["edges"]]

                if disable_children:
                    del_devices.append(int(device["id"]))
                    del_devices.extend([int(x["id"]) for x in children])
                else:
                    err_msg = (
                        "Unable to delete DID {} as it has children and "
                        "recursively_disable_children is False\nChildren: {}".format(
                            device["id"], children
                        )
                    )
                    error_devices.append(err_msg)
                    self.logger.warning(err_msg)
                    continue
            else:
                del_devices.append(int(device["id"]))

        return del_devices, error_devices

    def generate_snow_payloads(self, error_devices, delete_devices, sys_id):
        """
        Generates ServiceNow Work Notes Payloads.

        Args:
            error_devices (list): List of device delete errors.
            delete_devices (list): List of DIDs to be deleted from SL1
            sys_id (str): ServiceNow RITM sys_id.

        Returns:
            list: List of ServiceNow Payloads.

        """
        failed_state = self.get_parameter(service_request_failed_param.name)
        in_progress_state = self.get_parameter(service_request_in_progress_param.name)
        success_state = self.get_parameter(service_request_success_param.name)
        payloads = list()
        if error_devices:
            for error in error_devices:
                payloads.append({"request": sys_id, "work_notes": error})
            if delete_devices:
                payloads.append(
                    {
                        "request": sys_id,
                        "work_notes": "{} Devices failed to delete. {} "
                        "still processing.".format(
                            len(error_devices), len(delete_devices)
                        ),
                        "request_state": in_progress_state,
                    }
                )
                final_state = failed_state
            else:
                payloads.append(
                    {
                        "request": sys_id,
                        "work_notes": "All devices failed to delete.",
                        "request_state": failed_state,
                    }
                )
                final_state = failed_state
        else:
            payloads.append(
                {
                    "request": sys_id,
                    "request_state": in_progress_state,
                    "work_notes": "Deleting the following devices from SL1 {}".format(
                        delete_devices
                    ),
                }
            )
            final_state = success_state

        return payloads, final_state

    def execute(self):
        sys_id = self.get_parameter(service_request_sys_id_param.name)
        v_cug = self.get_parameter(service_request_vcug_param.name)
        if not v_cug:
            self.logger.error(
                "No {} specified. Failing all devices.".format(
                    service_request_vcug_param.name
                )
            )
            self.save_data_for_next_step(
                {
                    "snow_payload": [
                        {
                            "request": sys_id,
                            "work_notes": "No {} configured in IS. Failing all devices.".format(
                                service_request_vcug_param.name
                            ),
                            "request_state": self.get_parameter(
                                service_request_failed_param.name
                            ),
                        }
                    ],
                    "gql_vars": {"ids": [], "cug": 0},
                }
            )
        else:
            super(PullDevicesAndValidateRemoveRequests, self).execute()
            v_cug = int(v_cug)

            del_devices, error_devices = self.process_devices()
            snow_payloads, final_state = self.generate_snow_payloads(
                error_devices, del_devices, sys_id
            )
            self.logger.flow(
                "Moving {} devices to CUG ID: {}. DIDs: {}".format(
                    len(del_devices), v_cug, del_devices
                )
            )
            self.save_data_for_next_step(
                {
                    "snow_payload": {"records": snow_payloads},
                    "gql_vars": {"ids": del_devices, "cug": v_cug},
                    "final_state": final_state,
                    "devices": del_devices,
                }
            )
