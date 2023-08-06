from ipaascommon.content_manger import IpaasContentManager
from ipaascore.BaseStep import BaseStep
from servicenow_cmdb_syncpack.util.cmdb_params import mappings_param


class FetchMappingsFromApp(BaseStep):
    def __init__(self):
        self.friendly_name = "Fetch Mappings"
        self.description = "Fetches Application from IS"
        self.version = "1.0.0"

    def execute(self):
        cmanager = IpaasContentManager()
        sl1_app_data = cmanager.get_application_dict_from_db(
            "Device_Sync_ScienceLogic_To_ServiceNow"
        ).get("app_variables")
        self.logger.debug(f"Data for SL1 Mapping: {sl1_app_data}")

        snow_app_data = cmanager.get_application_dict_from_db(
            "sync_ci_attributes"
        ).get("app_variables")
        self.logger.debug(f"Data from SNOW Mapping: {snow_app_data}")

        sl1_map_list = self.get_data_from_list(sl1_app_data)
        snow_map_list = self.get_data_from_list(snow_app_data)

        data = {"snow_list": snow_map_list, "sl1_list": sl1_map_list}
        self.save_data_for_next_step(data)

    @staticmethod
    def get_data_from_list(list_data):
        mappings = next(
            (
                x["value"]
                for x in list_data
                if x["name"] == mappings_param.name
            ),
            dict(),
        )
        my_list = [v for k, v in mappings.items() if "cmdb_ci" in k]

        return my_list
