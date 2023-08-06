import pickle

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon.content_manger import IpaasContentManager
from servicenow_cmdb_syncpack.util.device_utils import ServiceNowDevice


class PullAndProcessSnowCiAttributes(QueryREST):
    def __init__(self):
        super(PullAndProcessSnowCiAttributes, self).__init__()
        self.friendly_name = "Pull and Process ServiceNow CI Attributes"
        self.description = (
            "Pulls CIs from ServiceNow and converts them to ServiceNowDevice Objects"
        )
        self.version = "1.0.0"

    def execute(self):
        super(PullAndProcessSnowCiAttributes, self).execute()
        cmanager = IpaasContentManager()
        snow_data = self.get_current_saved_data()
        self.logger.flow(f"Pulled {len(snow_data)} CIs")
        self.logger.info(f"SNOW CIs: {snow_data}")

        snow_devices = dict()

        errors = list()
        for device_dict in snow_data:
            if device_dict.get("error"):
                errors.append(device_dict)
                continue

            snow_device = ServiceNowDevice(device_dict, cmanager=cmanager)

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
                snow_device.clear_correlation()
                snow_devices[snow_device.sl1_id] = snow_device
        if errors:
            self.logger.error(f"Errors in ServiceNow CI Payload: {errors}")

        self.save_data_for_next_step(pickle.dumps(snow_devices))
