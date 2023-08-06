import pickle
from copy import deepcopy
from typing import Dict, Optional, Tuple

from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore import parameter_types
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.correlators import prepopulate_dev_lookups
from servicenow_base_syncpack.util.helpers import fix_query_rest_result
from servicenow_base_syncpack.util.snow_parameters import (
    lookup_chunk_size_param,
    region_param,
    sl1_hostname_param,
)
from servicenow_cmdb_syncpack.util.cmdb_params import (
    domain_sep_param,
    mappings_param,
    selected_devices_param,
    sl1_url_override_param,
)
from servicenow_cmdb_syncpack.util.device_utils import (
    SL1Device,
    extract_make_model_from_device_asset,
    invert_mappings,
)
from servicenow_cmdb_syncpack.util.org_utils import SL1Org


class ProcessSL1Devices(BaseStep):
    def __init__(self):
        self.friendly_name = "Process SL1 Devices"
        self.description = "Processes SL1 Devices"
        self.version = "1.1.0"

        self.new_step_parameter(
            name="excluded_devices",
            default_value=[],
            required=False,
            description="The list of excluded devices to not include when syncing",
            param_type=parameter_types.ArrayParameterString(),
            sample_value=["device_name_a", "device_id_232"],
        )
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(sl1_hostname_param)
        self.add_step_parameter_from_object(domain_sep_param)
        self.add_step_parameter_from_object(lookup_chunk_size_param)
        self.add_step_parameter_from_object(sl1_url_override_param)
        self.add_step_parameter_from_object(selected_devices_param)
        self.add_step_parameter_from_object(mappings_param)

        self.region = str()
        self.cmanager: Optional[IpaasContentManager] = None
        self.snow_companies = dict()
        self.domain_sep_enabled = bool()
        self.org_data: Dict[str, SL1Org] = dict()
        self.sl1_hostname = str()
        self.parent_device_dicts = dict()
        self.sl1_devices = dict()
        self.prepopulated_lookups = dict()
        self.models = dict()
        self.manufacturers = dict()
        self.url_override = str()
        self.should_drop_sysid = bool()
        self.inverted_mappings = dict()
        self.additional_data = None
        self.processed_devices: Dict[str, SL1Device] = dict()

    def execute(self, additional_data=None):
        sl1_devices_list = self.get_data_from_step_by_name("Fetch Devices from SL1")
        for device in sl1_devices_list:
            self.sl1_devices[device["device"]["id"]] = device["device"]

        self.parent_device_dicts = self.get_data_from_step_by_name(
            "Fetch Parent Devices From SL1"
        )
        self.org_data = pickle.loads(
            self.get_data_from_step_by_name("Pull and Process SL1 Organizations")
        )
        self.snow_companies = self.get_data_from_step_by_name(
            "Pull Companies from ServiceNow"
        )
        self.manufacturers = fix_query_rest_result(
            self.get_data_from_step_by_name("Query ServiceNow Manufacturers")
        ).get("result", dict())
        self.models = fix_query_rest_result(
            self.get_data_from_step_by_name("Query ServiceNow Hardware Models")
        ).get("result", dict())

        self.domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))
        self.region = self.get_parameter(region_param.name)
        self.sl1_hostname = self.get_parameter(sl1_hostname_param.name)
        lookup_chunk_size = int(self.get_parameter(lookup_chunk_size_param.name))
        self.url_override = self.get_parameter(sl1_url_override_param.name)
        self.cmanager = IpaasContentManager()  # Only instantiate cmanager once
        self.prepopulated_lookups = prepopulate_dev_lookups(
            self.region, self.sl1_devices.keys(), chunk_size=lookup_chunk_size
        )
        self.inverted_mappings = invert_mappings(
            self.get_parameter(mappings_param.name)
        )
        if additional_data:
            self.additional_data = additional_data

        self.save_data_for_next_step(pickle.dumps(self.process_devices()))

    def generate_sl1_device_object(
        self,
        device_dict: dict,
        parent_device: Optional[SL1Device] = None,
        component_details: Optional[dict] = None,
    ) -> Tuple[Optional[SL1Device], Optional[str]]:
        """
        Generate SL1Device Object. Create Fake unmerged device if required. (INT-3113)

        Args:
            device_dict: GQL Payload of device
            parent_device: Parent Device Object
            component_details: Additional details if device is a component.

        Returns:

        """

        component_unique_id = None
        if component_details:
            component_unique_id = component_details.get("unique_id", None)

        class_str = (
            f'{device_dict["deviceClass"]["class"]} | '
            f'{device_dict["deviceClass"]["description"]}'
        )
        self.logger.debug("class_str: %s" % class_str)
        sl1_org = self.org_data.get(device_dict.pop("organization", dict()).get("id"))

        snow_ci = self.inverted_mappings.get(class_str.lower())
        if not snow_ci:
            return None, class_str
        domain = self.get_domain(sl1_org)

        make, model = extract_make_model_from_device_asset(device_dict["asset"])
        manufacturer = self.manufacturers.get(make)
        model = self.models.get(model)
        if self.additional_data:
            additional_data = self.additional_data.get(device_dict["id"])
        else:
            additional_data = None

        actual_device = SL1Device(
            self.sl1_hostname,
            self.region,
            device_dict,
            snow_ci,
            org=sl1_org,
            parent_device=parent_device,
            component_unique_id=component_unique_id,
            cmanager=self.cmanager,
            prepopulated_lookups=self.prepopulated_lookups,
            domain_sys_id=domain,
            manufacturer_sys_id=manufacturer,
            model_sys_id=model,
            url_override=self.url_override,
            additional_data=additional_data,
        )
        if isinstance(component_details, dict):
            if component_details.get("merge_did"):
                # Create a fake device to "unmerge"
                fake_device = deepcopy(actual_device)  # duplicate original
                fake_device.sl1_id = str(
                    component_details["merge_did"]
                )  # override device id
                fake_device.name = component_details["merge_name"]  # override name
                fake_device.device_class = component_details.get(
                    "class", str()
                )  # override class
                fake_device.snow_ci_class = self.inverted_mappings.get(
                    fake_device.device_class.lower()
                )  # override snow ci class.
                fake_device.device_category = (
                    "Virtual"
                )  # hard-coded as the data isn't available

                # Override sys_id if found.
                fake_device.set_correlation(self.cmanager)
                if fake_device.correlation:
                    fake_device.snow_sys_id = (
                        fake_device.correlation.get_correlating_dev_snow_id()
                    )
                    fake_device.clear_correlation()
                else:
                    fake_device.snow_sys_id = None
                actual_device.component_unique_id = None  # Value no-longer needed.
                actual_device.parent_device = (
                    fake_device
                )  # Set fake device as parent or actual. fake will contain the original parent relation.
                actual_device.merged = True  # Sets hard-coded relation type
                self.processed_devices[
                    fake_device.sl1_id
                ] = fake_device  # add fake device to the processed cache
        return actual_device, None

    def get_parent_device_info(
        self, device_dict: dict
    ) -> Tuple[Optional[SL1Device], Optional[dict]]:
        """
        Find and build parent device relations or return none.

        Args:
            device_dict (dict): dictionary of device data.

        """
        if int(device_dict["id"]) in self.parent_device_dicts:
            component_details = self.parent_device_dicts.get(int(device_dict["id"]))
            self.logger.debug("Parent Device Found: %s" % component_details)
            if str(component_details["parent_did"]) in self.sl1_devices:
                parent_device_dict = self.sl1_devices[
                    str(component_details["parent_did"])
                ]
                if str(component_details["parent_did"]) in self.processed_devices:
                    parent_device = self.processed_devices.get(
                        str(component_details["parent_did"])
                    )
                else:
                    next_parent_device, parent_component_details = self.get_parent_device_info(
                        parent_device_dict
                    )
                    parent_device, class_str = self.generate_sl1_device_object(
                        parent_device_dict,
                        parent_device=next_parent_device,
                        component_details=parent_component_details,
                    )

                    self.processed_devices[parent_device.sl1_id] = parent_device

                return parent_device, component_details
        return None, None

    def process_devices(self) -> Dict[str, SL1Device]:
        """
        Retrieve device maps from input handlers.
        """
        selected_devices = self.get_parameter(selected_devices_param.name)
        if selected_devices:
            did_list = [int(x) for x in selected_devices if x]
            self.logger.flow(
                "Selective Device Sync Enabled. Syncing DIDs: {}".format(did_list)
            )
        else:
            did_list = list()

        excluded_devices = self.get_parameter("excluded_devices", {})
        # Mappings of em7 id to device

        for did, device_dict in self.sl1_devices.items():
            if did_list and int(did) not in did_list:
                continue
            if did in self.processed_devices:
                continue

            self.logger.debug("Current DID: {}".format(did))
            parent_device, component_details = self.get_parent_device_info(device_dict)
            sl1_device, class_str = self.generate_sl1_device_object(
                device_dict,
                parent_device=parent_device,
                component_details=component_details,
            )
            if not sl1_device:
                self.logger.warning(
                    f"DID: {did} with Class {class_str} has no matching CI class in mappings. "
                    f"Dropping"
                )
                continue

            if (
                getattr(sl1_device, "name") in excluded_devices
                or sl1_device.sl1_id in excluded_devices
            ):
                self.logger.info(
                    f"SL1 device: {sl1_device.sl1_id} - {getattr(sl1_device, 'name')} "
                    f"belongs to the excluded device list. Dropping"
                )
            else:
                self.processed_devices[sl1_device.sl1_id] = sl1_device
        return self.processed_devices

    def get_domain(self, sl1_org: SL1Org) -> Optional[str]:
        """Return Domain if domain sep is enabled and matching company found"""
        if self.domain_sep_enabled:
            if sl1_org:
                return self.snow_companies.get(sl1_org.snow_sys_id, dict()).get(
                    "sys_domain"
                )
        return None
