from base_steps_syncpack.steps.QueryGQL import QueryGQL
from ipaascommon.ipaas_exceptions import StepFailedException
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore.parameter_types import BoolParameterToggle, StringParameterShort
from servicenow_base_syncpack.util.helpers import validate_mappings
from servicenow_base_syncpack.util.servicenow_exceptions import InvalidMappings
from servicenow_base_syncpack.util.snow_parameters import region_param, chunk_size_param
from servicenow_cmdb_syncpack.util.cmdb_params import (
    cug_filter_param,
    mappings_param,
    org_filter_param,
    exclude_inactive_param,
)
from servicenow_cmdb_syncpack.util.device_utils import (
    ScienceLogicDeviceClassList,
    generate_devices_gql_query,
)


class PullDevicesFromSL1(QueryGQL):
    def __init__(self):
        super(PullDevicesFromSL1, self).__init__()
        self.friendly_name = "Pull Devices From SL1"
        self.description = "Pulls Devices from SL1 via GQL and re-formats result."
        self.version = "1.0.0"
        self.add_step_parameter_from_object(mappings_param)
        self.add_step_parameter_from_object(org_filter_param)
        self.add_step_parameter_from_object(cug_filter_param)
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(exclude_inactive_param)

        self.new_step_parameter(
            name="enable_device_active",
            description=(
                "Enables the Device Active block in the Device GQL Query. "
                "Accessing this data in the attribute mappings requires use of a "
                "Jinja2 Template. See documentation for more details."
            ),
            default_value=False,
            required=False,
            param_type=BoolParameterToggle(),
        )
        self.new_step_parameter(
            name="enable_asset_networks",
            description=(
                "WARNING: Enabling this feature may have a negative performance impact "
                "on SL1."
                "Enables the assetNetworks block in the Device GQL Query. "
                "Accessing this data in the attribute mappings requires use of a "
                "Jinja2 Template. See documentation for more details."
            ),
            default_value=False,
            required=False,
            param_type=BoolParameterToggle(),
        )

        # Reset Defaults
        del self.parameters["variables"]
        self.new_step_parameter(name="variables", param_type=StringParameterShort())
        del self.parameters["query"]
        self.new_step_parameter(name="query", param_type=StringParameterShort())

    def execute(self):
        self.generate_variables()
        enable_networks = str_to_bool(self.get_parameter("enable_asset_networks"))
        enable_active = str_to_bool(self.get_parameter("enable_device_active"))
        query_var = self.parameters.get("query")
        query_var.value = generate_devices_gql_query(
            enable_networks=enable_networks, enable_active=enable_active
        )
        super(PullDevicesFromSL1, self).execute()

    def generate_variables(self):
        mappings = self.get_parameter(mappings_param.name)
        chunk_size = int(self.get_parameter(chunk_size_param.name))

        try:
            validate_mappings(mappings)
        except InvalidMappings as err:
            self.logger.error("{}: {}".format(err[0], err[1]))
            raise StepFailedException(err)

        org_filter = self.get_parameter(org_filter_param.name)
        cug_filter = self.get_parameter(cug_filter_param.name)
        drop_inactive = str_to_bool(self.get_parameter(exclude_inactive_param.name))
        region = self.get_parameter(region_param.name)
        dev_classes = ScienceLogicDeviceClassList(
            region, mappings=mappings, org_filter=org_filter, cug_filter=cug_filter
        )
        if org_filter:
            self.logger.flow("Filtering by Organization IDs: {}".format(org_filter))
        if cug_filter:
            self.logger.flow("Filtering by Collector Group IDs: {}".format(cug_filter))

        variables = self.parameters.get("variables")
        variables.value = dev_classes.generate_gql_search_filter(
            chunk_size, drop_inactive=drop_inactive
        )
