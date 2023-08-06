import pickle
from typing import Dict, List

from base_steps_syncpack.steps.QueryGQL import QueryGQL
from ipaascommon.ipaas_exceptions import (
    MissingRequiredStepParameter,
    StepFailedException,
)
from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascore.parameter_types import StringParameterShort
from servicenow_base_syncpack.util.helpers import validate_mappings
from servicenow_base_syncpack.util.servicenow_exceptions import InvalidMappings
from servicenow_base_syncpack.util.snow_parameters import (
    chunk_size_param,
    region_param,
    sl1_hostname_param,
)
from servicenow_cmdb_syncpack.util.cmdb_params import (
    ci_attrib_mappings_param,
    cug_filter_param,
    org_filter_param,
)
from servicenow_cmdb_syncpack.util.device_utils import (
    SL1Device,
    ScienceLogicDeviceClassList,
    generate_devices_gql_query,
    prepopulate_dev_lookups,
)


class PullAndProcessSL1DeviceAttributes(QueryGQL):
    def __init__(self):
        super(PullAndProcessSL1DeviceAttributes, self).__init__()
        self.friendly_name = "Pull And Process SL1 Device Attributes"
        self.description = "Pulls Devices from SL1 and converts to SL1Device objects for Attribute Sync"
        self.version = "1.0.0"

        self.add_step_parameter_from_object(ci_attrib_mappings_param)
        self.add_step_parameter_from_object(org_filter_param)
        self.add_step_parameter_from_object(cug_filter_param)
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(sl1_hostname_param)

        self.cmanager = None
        self.region = None

        # Reset Defaults
        del self.parameters["variables"]
        self.new_step_parameter(name="variables", param_type=StringParameterShort())
        del self.parameters["query"]
        self.new_step_parameter(name="query", param_type=StringParameterShort())

    def execute(self):
        self.cmanager = IpaasContentManager()
        self.region = self.get_parameter(region_param.name)
        self.generate_variables()
        query_var = self.parameters.get("query")
        query_var.value = generate_devices_gql_query()

        super(PullAndProcessSL1DeviceAttributes, self).execute()

        self.save_data_for_next_step(self.convert_device_dicts_to_objects())

    def generate_variables(self):
        mappings = self.get_parameter(ci_attrib_mappings_param.name)

        dev_sync_vars = self.cmanager.get_application_dict_from_db(
            "Device_Sync_ScienceLogic_To_ServiceNow"
        ).get("app_variables")
        if not mappings:
            mappings = next(
                (
                    x["value"]
                    for x in dev_sync_vars
                    if x["name"] == ci_attrib_mappings_param.name
                ),
                None,
            )
            if not mappings:
                raise MissingRequiredStepParameter(
                    "{} is required but is not populated in either {} or in "
                    "Device_Sync_ScienceLogic_To_ServiceNow.".format(
                        ci_attrib_mappings_param.name, self.application_name
                    )
                )
        org_filter = self.get_parameter(org_filter_param.name)
        if not org_filter:
            org_filter = (
                next(
                    x["value"]
                    for x in dev_sync_vars
                    if x["name"] == org_filter_param.name
                ),
                None,
            )
        cug_filter = self.get_parameter(cug_filter_param.name)
        if not cug_filter:
            cug_filter = (
                next(
                    x["value"]
                    for x in dev_sync_vars
                    if x["name"] == cug_filter_param.name
                ),
                None,
            )
        try:
            validate_mappings(mappings)
        except InvalidMappings as err:
            self.logger.error("{}: {}".format(err[0], err[1]))
            raise StepFailedException(err)

        chunk_size = int(self.get_parameter(chunk_size_param.name))
        dev_classes = ScienceLogicDeviceClassList(
            self.region, mappings=mappings, org_filter=org_filter, cug_filter=cug_filter
        )
        if org_filter:
            self.logger.flow("Filtering by Organization IDs: {}".format(org_filter))
        if cug_filter:
            self.logger.flow("Filtering by Collector Group IDs: {}".format(cug_filter))

        variables = self.parameters.get("variables")
        variables.value = dev_classes.generate_gql_search_filter(chunk_size)

    def convert_device_dicts_to_objects(self):
        """Convert GQL response into a pickled dict of SL1Device Objects."""
        gql_data = self.get_current_saved_data()
        self.logger.flow(f"Pulled {len(gql_data)} Devices")
        self.logger.info(f"Pulled Devices: {gql_data}")
        sl1_devices = dict()
        sl1_hostname = self.get_parameter(sl1_hostname_param.name)
        prepopulated_lookups = prepopulate_dev_lookups(
            self.region, self.device_id_list(gql_data)
        )

        for device_dict in gql_data:
            did = device_dict["device"]["id"]
            self.logger.debug("Current DID: {}".format(did))
            class_str = "{} | {}".format(
                device_dict["device"]["deviceClass"]["class"],
                device_dict["device"]["deviceClass"]["description"],
            )
            self.logger.debug("class_str: %s" % class_str)

            sl1_device = SL1Device(
                sl1_hostname,
                self.region,
                device_dict["device"],
                snow_ci_class=str(),
                cmanager=self.cmanager,
                prepopulated_lookups=prepopulated_lookups,
            )

            sl1_devices[sl1_device.sl1_id] = sl1_device
        return pickle.dumps(sl1_devices)

    @staticmethod
    def device_id_list(gql_data: dict) -> List[Dict[str, str]]:
        return [{"id": x["device"]["id"]} for x in gql_data]
