from ipaascore.BaseStep import BaseStep
from servicenow_cmdb_syncpack.util.device_utils import (
    ServiceNowDevice,
    group_correlations,
)
from servicenow_cmdb_syncpack.util.cmdb_params import selected_devices_param
from ipaascommon.content_manger import IpaasContentManager
import pickle


class ProcessSnowDevices(BaseStep):
    def __init__(self):
        self.friendly_name = "Process ServiceNow Devices"
        self.description = "Processes ServiceNow Devices"
        self.version = "1.0.0"

        self.add_step_parameter_from_object(selected_devices_param)

    def execute(self):
        cmanager = IpaasContentManager()
        snow_data = self.get_data_from_step_by_name("Pull ServiceNow CIs")
        self.logger.flow(f"Pulled {len(snow_data)} CIs")
        self.logger.info(f"SNOW CIs: {snow_data}")

        selected_devices = self.get_parameter(selected_devices_param.name)
        if selected_devices:
            did_list = [int(x) for x in selected_devices if x]
            self.logger.flow(
                "Selective Device Sync Enabled. Syncing DIDs: {}".format(did_list)
            )
        else:
            did_list = list()

        snow_devices = dict()
        newly_added_snow_devs = []
        duplicate_devices = []

        errors = list()
        for device_dict in snow_data:
            if device_dict.get("error"):
                errors.append(device_dict)
                continue

            snow_device = ServiceNowDevice(device_dict, cmanager=cmanager)

            if did_list and int(snow_device.sl1_id) not in did_list:
                continue

            # Drop duplicate devices.
            if getattr(snow_device, "discovery_source", None) == "Duplicate" or getattr(
                snow_device, "duplicate_of", None
            ):
                continue

            # If there already exists a device with this region in snow, it
            # means they are duplicates. Put the dupe in a separate list
            # for later
            existing_device_in_map = snow_devices.get(snow_device.sl1_id)
            if not existing_device_in_map:
                snow_devices[snow_device.sl1_id] = snow_device
                newly_added_snow_devs.append(snow_device)
            else:
                if existing_device_in_map.snow_sys_id != snow_device.snow_sys_id:
                    # If there's a dupe, make sure it's not the same sys_id
                    duplicate_devices.append(snow_device)
                    snow_device.clear_correlation()
        if errors:
            self.logger.error("Errors in ServiceNow CI Payload: {}".format(errors))

        cmanager.batch_data_and_save_to_cache(group_correlations(newly_added_snow_devs))

        self.save_data_for_next_step(
            pickle.dumps(
                {"snow_devices": snow_devices, "duplicates": duplicate_devices}
            )
        )
