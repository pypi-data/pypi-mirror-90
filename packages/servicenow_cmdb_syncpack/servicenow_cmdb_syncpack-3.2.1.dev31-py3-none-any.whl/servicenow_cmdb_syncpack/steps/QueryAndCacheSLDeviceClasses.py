from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon.content_manger import IpaasContentManager
from isbaseutils.ipaas_constants import EM7_KEY_VAL
from servicenow_cmdb_syncpack.util.device_utils import dev_class_list_key
from servicenow_base_syncpack.util.snow_parameters import region_param


class QueryAndCacheSLDeviceClasses(QueryREST):
    def __init__(self):
        super(QueryAndCacheSLDeviceClasses, self).__init__()
        self.friendly_name = "Query and Cache SL1 Device Class info"
        self.description = (
            "Queries a SL1 instance for all available Device Classes and saves "
            "the data to cache with the specified SL1 id",
        )
        self.version = "3.0.0"
        self.add_step_parameter_from_object(region_param)

    def execute(self):
        """
        All logic main logic for executing the step happens here
        :return:
        """
        # Execute main query rest first
        super(QueryAndCacheSLDeviceClasses, self).execute()
        dev_classes = self.get_current_saved_data()
        region = self.get_parameter(region_param.name)

        dev_class_usable_data = []

        for dev_class in dev_classes:
            dev_class_usable_data.append(
                {
                    "id": dev_class[EM7_KEY_VAL],
                    "guid": dev_class["guid"],
                    "class": dev_class["class"],
                    "description": dev_class["description"],
                    "virtual_type": dev_class["virtual_type"],
                }
            )

        cmanager = IpaasContentManager()
        cmanager.save_to_cache(dev_class_list_key("EM71"), dev_class_usable_data)
        cmanager.save_to_cache(dev_class_list_key(region), dev_class_usable_data)
        # This doesn't have data for a next step. Clean out whatever
        # may be there
        self.save_data_for_next_step({})
