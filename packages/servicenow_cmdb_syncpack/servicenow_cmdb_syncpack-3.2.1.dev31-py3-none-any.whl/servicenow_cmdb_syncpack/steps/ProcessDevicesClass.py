from ipaascore.BaseStep import BaseStep
from servicenow_cmdb_syncpack.util.cmdb_params import pf_host_param


class ProcessDevicesClass(BaseStep):
    def __init__(self):
        self.friendly_name = "Process Device Class Data"
        self.description = (
            "Finds the delta between Mappings in IS and used Device Classes in SL1"
        )
        self.version = "1.0.0"

        self.add_step_parameter_from_object(pf_host_param)

    def execute(self):
        # Step Logic goes here
        hostname = self.get_parameter(pf_host_param.name)
        device_class = self.get_data_from_step_by_name("Fetch Devices From SL1")
        application_data = self.get_data_from_step_by_name(
            "Fetch Mapping From IS Application"
        )

        snow_list = application_data["snow_list"]
        sl1_list = application_data["sl1_list"]

        clear_device_class = set(device_class)

        delta_snow = [
            dev_class for dev_class in clear_device_class if dev_class not in snow_list
        ]
        delta_sl1 = [
            dev_class for dev_class in clear_device_class if dev_class not in sl1_list
        ]

        self.logger.debug(f"Data for IS: SL1: {sl1_list} | SNOW: {snow_list}")

        self.logger.flow(
            f"Missing SNOW Mappings are: {len(delta_snow)}\nMissing SL1 Mappings are: {len(delta_sl1)}"
        )
        if not delta_snow or not delta_sl1:
            self.save_data_for_next_step({"enabled": False})
        else:
            payload = {
                "enabled": True,
                "raiseEvent": {
                    "message": f"PowerFlow: Missing Mappings: https://{hostname}/reports/",
                    "value": f"{len(delta_sl1)} | {len(delta_snow)}",
                    "aligned_resource": "/api/organization/0",
                },
                "snowMissing": delta_snow,
                "sl1Missing": delta_sl1,
            }
            self.save_data_for_next_step(payload)
