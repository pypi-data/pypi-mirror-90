import pickle
from datetime import datetime
from itertools import chain
from typing import Dict, List, Optional, Tuple

from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascommon.report_manager import ParentReport
from ipaascore import parameter_types
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.snow_parameters import chunk_size_param
from servicenow_cmdb_syncpack.util.cmdb_base_utils import chunk_cis, object_changed
from servicenow_cmdb_syncpack.util.cmdb_constants import RELATION_OVERRIDES
from servicenow_cmdb_syncpack.util.cmdb_params import (
    attribute_mappings_param,
    discovery_source_param,
    domain_sep_param,
    drop_company_param,
    relation_overrides_param,
)
from servicenow_cmdb_syncpack.util.device_utils import (
    SL1Device,
    ServiceNowDevice,
    get_info_with_reload,
    update_correlations,
)


class SL1SnowDeviceCompare(BaseStep):
    """
    Analyzes the devices available in EM7 and ServiceNow, and creates a dict of
    devices to be added to em7, devices to be added to snow, devices to remove
    from em7, and devices to remove from snow.
    """

    def __init__(self):
        self.friendly_name = "Compare SL1 and ServiceNow Devices"
        self.description = (
            "Step compares data between existing SNOW and SL1 "
            "devices. Creates data structures for properly "
            "update the SNOW system."
        )
        self.version = "3.1.0"
        self.add_step_parameter_from_object(domain_sep_param)
        self.add_step_parameter_from_object(attribute_mappings_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(drop_company_param)
        self.add_step_parameter_from_object(relation_overrides_param)
        self.add_step_parameter_from_object(discovery_source_param)

        self.new_step_parameter(
            name="drop_sys_id",
            description="Whether or not to drop the sys id for existing CIs "
            "from the payload. If you set this to True, you should"
            " be sure ServiceNow can correctly identify your CIS "
            "with the properties available",
            required=False,
            default_value=False,
            param_type=parameter_types.BoolParameterToggle(),
        )

        self.attr_mappings = dict()
        self.cmanager: Optional[IpaasContentManager] = None
        self.domain_sep_enabled = bool()
        self.should_drop_sysid = False
        self.drop_company = False
        self.start_time = str()
        self.source_name = str()

    def execute(self):
        self.start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.source_name = self.get_parameter(discovery_source_param.name)
        self.should_drop_sysid = str_to_bool(self.get_parameter("drop_sys_id"))
        self.drop_company = str_to_bool(self.get_parameter(drop_company_param.name))
        self.attr_mappings = self.get_parameter(attribute_mappings_param.name)
        self.cmanager = IpaasContentManager()  # Only instantiate cmanager once
        self.domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))

        customer_ci_relation_overrides = self.get_parameter(
            relation_overrides_param.name
        )
        if customer_ci_relation_overrides:
            RELATION_OVERRIDES.update(customer_ci_relation_overrides)

        sl1_devices = pickle.loads(
            self.get_data_from_step_by_name("Process SL1 Devices")
        )
        snow_data = pickle.loads(
            self.get_data_from_step_by_name("Process ServiceNow CIs")
        )
        disconnects = self.find_snow_deletions(
            sl1_devices, snow_data["snow_devices"], snow_data["duplicates"]
        )
        additions, updates, unchanged = self.find_snow_additions_and_updates(
            sl1_devices, snow_data["snow_devices"]
        )

        self.logger.flow(
            "Sending {} Creates, {} Updates, and {} Disconnections to "
            "ServiceNow".format(len(additions), len(updates), len(disconnects))
        )
        self.logger.info(f"Creates: {additions}")
        self.logger.info(f"Updates: {updates}")
        self.logger.info(f"Disconnects: {disconnects}")

        chunk_size = int(self.get_app_variable(chunk_size_param.name))
        payloads = chunk_cis(
            chain(additions, updates, disconnects),
            chunk_size,
            domain_sep=self.domain_sep_enabled,
            logger=self.logger,
        )

        if self.generate_report:
            self.logger.flow("Creating report.")
            report = ParentReport(self)
            self.report_device_list(report, disconnects, "Removed")
            self.report_device_list(report, additions, "New")
            self.report_device_list(report, updates, "Updated")
            self.report_device_list(report, unchanged, "Unchanged")
            self.logger.flow("Report {} completed.".format(report.report_id))

        self.logger.flow(f"Sending {len(payloads)} chunks.")
        self.logger.debug(f"Final Payloads: {payloads}")
        self.save_data_for_next_step(payloads)

    def find_snow_deletions(
        self,
        sl1_devices: Dict[str, SL1Device],
        snow_devices: Dict[str, ServiceNowDevice],
        duplicate_devices: List[ServiceNowDevice],
    ) -> List[dict]:
        """
        Iterate over snow map and finds devices which no longer exist in em7.

        If any are found, it's sys_id will be added to a list so that it can
        be deleted in a future step.

        """
        deletes = []
        deletes_from_cache = []
        for dupe_device in duplicate_devices:
            dupe_device.set_correlation(cmanager=self.cmanager)
            del_dict = self.generate_disconnect_payload(dupe_device)
            deletes.append(del_dict)
            deletes_from_cache.append(dupe_device)

        for sl1_id, snow_item in snow_devices.items():
            snow_item.set_correlation(cmanager=self.cmanager)
            if not sl1_devices.get(sl1_id, None):
                device = {
                    "name": getattr(snow_item, "name", "Unknown"),
                    "sys_id": snow_item.snow_sys_id,
                }
                self.logger.debug(
                    f"ServiceNow CI: {device} does not exist in SL1. " f"Disconnecting"
                )
                del_dict = self.generate_disconnect_payload(snow_item)
                deletes.append(del_dict)
                deletes_from_cache.append(snow_item)

        self.cmanager.db_connector.batch_remove_keys_from_logs(
            [del_dev.correlation.device_lookup_key for del_dev in deletes_from_cache]
        )
        return deletes

    def generate_disconnect_payload(self, snow_device: ServiceNowDevice) -> dict:
        del_dict = {
            "items": [
                {
                    "className": snow_device.snow_ci_class,
                    "values": {
                        "sys_id": snow_device.snow_sys_id,
                        "company": snow_device.company_sys_id,
                        "x_sclo_scilogic_monitored": False,
                    },
                    "sys_object_source_info": {
                        "source_feed": snow_device.region,
                        "source_name": self.source_name,
                        "source_native_key": snow_device.sl1_id,
                        "source_recency_timestamp": self.start_time,
                    },
                }
            ],
            "relations": [],
        }
        if snow_device.domain_sys_id:
            del_dict["items"][0]["values"]["sys_domain"] = snow_device.domain_sys_id
        return del_dict

    def find_snow_additions_and_updates(
        self,
        sl1_devices: Dict[str, SL1Device],
        snow_devices: Dict[str, ServiceNowDevice],
    ) -> Tuple[List[dict], List[dict], List[dict]]:
        """
        Parse additions and updates.

        """
        additions = []
        updates = []
        unchanged = []
        sys_ids_to_clear = []
        merged_devices = list()
        for did, sl1_device in sl1_devices.items():
            sl1_device.set_correlation(cmanager=self.cmanager)
            snow_ci = snow_devices.get(did, None)
            if not snow_ci:
                self.logger.debug(
                    f"New SL1 device: {getattr(sl1_device, 'name')} (id: {sl1_device.sl1_id}) "
                    f"will be added into ServiceNow as CI type: {sl1_device.snow_ci_class}"
                )
                sl1_device.snow_sys_id = None
                item_dict = get_info_with_reload(
                    sl1_device,
                    self.attr_mappings,
                    self.logger,
                    drop_sys_id=self.should_drop_sysid,
                    relation_overrides=RELATION_OVERRIDES,
                    domain_sep_enabled=self.domain_sep_enabled,
                    drop_company=self.drop_company,
                    start_time=self.start_time,
                    source_name=self.source_name,
                )
                additions.append(item_dict)
                sys_ids_to_clear.append(sl1_device)
            else:
                sl1_device.snow_sys_id = snow_ci.snow_sys_id
                if sl1_device.merged:
                    if sl1_device.parent_device.snow_sys_id:
                        sl1_device.correlation.merged_device = {
                            "sys_id": sl1_device.parent_device.snow_sys_id,
                            "class": sl1_device.parent_device.snow_ci_class,
                        }
                        merged_devices.append(sl1_device)
                if object_changed(
                    sl1_device,
                    snow_ci,
                    attr_mappings=self.attr_mappings,
                    logger=self.logger,
                ):
                    item_dict = get_info_with_reload(
                        sl1_device,
                        self.attr_mappings,
                        self.logger,
                        drop_sys_id=self.should_drop_sysid,
                        relation_overrides=RELATION_OVERRIDES,
                        domain_sep_enabled=self.domain_sep_enabled,
                        drop_company=self.drop_company,
                        start_time=self.start_time,
                        source_name=self.source_name,
                    )
                    updates.append(item_dict)

        # Be sure to delete the sys_id mapping for any new devices, in case the
        # current id we have is stale, or the device was added to ServiceNow
        # manually
        self.cmanager.db_connector.batch_remove_keys_from_logs(
            [new_dev.correlation.device_lookup_key for new_dev in sys_ids_to_clear]
        )
        self.cmanager.batch_data_and_save_to_cache(update_correlations(merged_devices))

        return additions, updates, unchanged

    def report_device(self, report, device_dict, subreport_name=None, status=None):
        """
        Adds data for an individual device to the report
        :param report: The report data is added to
        :param device_dict: The dict with device data to be added
        :param subreport_name: Name of subreport to add this data to
        :param status: Sync status of the device
        :return:
        """
        self.logger.debug("Reporting on {} device: {}".format(status, device_dict))
        if "x_sclo_scilogic_id" in device_dict:
            report.add_row(
                "SL1 Device ID",
                device_dict["x_sclo_scilogic_id"],
                data_key=subreport_name,
            )
        else:
            report.add_row("SL1 Device ID", "", data_key=subreport_name)
        if "sys_id" in device_dict:
            report.add_row(
                "ServiceNOW Sys ID", device_dict["sys_id"], data_key=subreport_name
            )
        else:
            report.add_row("ServiceNOW Sys ID", "", data_key=subreport_name)
        if "name" in device_dict:
            report.add_row("Device Name", device_dict["name"], data_key=subreport_name)
        else:
            report.add_row("Device Name", "", data_key=subreport_name)
        if "ip_address" in device_dict:
            report.add_row(
                "IP Address", device_dict["ip_address"], data_key=subreport_name
            )
        else:
            report.add_row("IP Address", "", data_key=subreport_name)
        if "x_sclo_scilogic_url" in device_dict:
            report.add_row(
                "ScienceLogic URL",
                device_dict["x_sclo_scilogic_url"],
                data_key=subreport_name,
            )
        else:
            report.add_row("ScienceLogic URL", "", data_key=subreport_name)
        report.add_row("Status", status, data_key=subreport_name)

    def report_device_list(self, report, device_list, status=None):
        """
        Creates report entries for all devices in a given list
        :param report: The report to add the devices to
        :param device_list: The list of devices to be added to the report
        :param status: The status of the devices in the list
        :return:
        """
        self.logger.flow("Updating report with {} devices.".format(status))
        for device in device_list:
            ci_class = device["items"][-1]["className"]
            self.create_subreport(report, ci_class)
            self.report_device(report, device["items"][-1]["values"], ci_class, status)

    @staticmethod
    def create_subreport(report, subreport_name):
        """
        Creates a new subreport with the header of the subreport_name
        :param report: The reporting object to add the subreport to
        :param subreport_name: The name of the subreport that will get created
        :return: The report object gets passed back
        """
        report.add_column("SL1 Device ID", data_key=subreport_name)
        report.add_column("ServiceNOW Sys ID", data_key=subreport_name)
        report.add_column("Device Name", data_key=subreport_name)
        report.add_column("IP Address", data_key=subreport_name)
        report.add_column("Status", data_key=subreport_name)
        report.add_column("ScienceLogic URL", data_key=subreport_name)
        return report
