import os
from itertools import chain

from future.utils import iteritems

from ipaascommon import ipaas_exceptions
from ipaascommon.content_manger import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore import parameter_types
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.correlators import (
    group_interface_correlations,
    prepopulate_dev_lookups,
)
from servicenow_base_syncpack.util.helpers import get_lookup_chunk_size
from servicenow_base_syncpack.util.snow_parameters import (
    chunk_size_param,
    domain_sep_param,
    lookup_chunk_size_param,
    region_param,
)
from servicenow_cmdb_syncpack.util.cmdb_base_utils import chunk_cis
from servicenow_cmdb_syncpack.util.interface_utils import (
    interface_changed,
    scoped_service_now_interface_from_snow_data,
    service_now_interface_from_em7_interface_data,
)


class SnowEm7NetworkAdapterCompare(BaseStep):
    def __init__(self):
        self.friendly_name = "SNOW/SL1 Network Adapter Compare"
        self.description = (
            "Step compares data between existing SNOW network "
            "CIs and SL1 network adapters. Creates data "
            "structures for properly updating the SNOW system."
        )
        self.version = "2.4.0"
        self.new_step_parameter(
            name="adapter_sync",
            description="Which network adapters should be synced.",
            default_value="enabled",
            param_type=parameter_types.SelectStaticDropdownParameter(
                ["off", "all", "enabled"]
            ),
        )
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(domain_sep_param)
        self.add_step_parameter_from_object(lookup_chunk_size_param)
        self.cmanager = None
        self.region = str()

    def execute(self):
        self.cmanager = IpaasContentManager()
        self.region = self.get_parameter(region_param.name)

        snow_data, sl1_data, duplicate_interfaces = self.get_interfaces()
        new_interfaces, update_interfaces = self.find_snow_additions_and_updates(
            sl1_data, snow_data
        )

        delete_interfaces = self.find_snow_deletions(
            sl1_data, snow_data, duplicate_interfaces
        )

        self.logger.flow(
            "Sending {} Creates, {} Updates, and {} Disconnections to ServiceNow".format(
                len(new_interfaces), len(update_interfaces), len(delete_interfaces)
            )
        )
        self.logger.debug(u"Creates: {}".format(new_interfaces))
        self.logger.debug(u"Updates: {}".format(update_interfaces))
        self.logger.debug(u"Disconnects: {}".format(delete_interfaces))

        chunk_size = int(self.get_parameter(chunk_size_param.name))
        domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))
        payloads = chunk_cis(
            chain(new_interfaces, update_interfaces, delete_interfaces),
            chunk_size,
            domain_sep=domain_sep_enabled,
            logger=self.logger,
        )
        self.logger.flow("Sending {} chunks.".format(len(payloads)))
        self.logger.debug(u"Final Payloads: {}".format(payloads))
        self.save_data_for_next_step(payloads)

    def get_interfaces(self):
        snow_interfaces = self.get_data_from_step_by_name(
            "Fetch Interfaces from ServiceNow"
        ).get("results", {})
        sl1_interfaces = self.get_data_from_step_by_name("Fetch Interfaces from SL1")
        sl1_ips = self.get_data_from_step_by_name("Fetch IPs/Subnets from SL1")
        prepopulated_lookups = self.dev_sys_lookup_dict(sl1_interfaces)

        self.logger.debug(u"SNOW Interfaces: {}".format(snow_interfaces))
        self.logger.debug(u"SL1 Interfaces: {}".format(sl1_interfaces))
        self.logger.debug(u"SL1 IPs: {}".format(sl1_ips))

        sl1_data = {}
        snow_data = {}
        duplicate_interfaces_in_snow = []
        adapter_sync_setting = self.get_parameter("adapter_sync", {})

        if not adapter_sync_setting.lower() == "off":
            for interface in sl1_interfaces:
                if_id = os.path.basename(interface["AA__key_val__"])
                ip_subnet = [x for x in sl1_ips if str(x["if_id"]) == if_id]
                if ip_subnet:
                    ip_subnet = ip_subnet[0]
                else:
                    ip_subnet = {}
                em7_data_as_snow_interface = service_now_interface_from_em7_interface_data(
                    interface,
                    ip_subnet,
                    "",
                    self.region,
                    cmanager=self.cmanager,
                    scoped=True,
                    prepopulated_lookups=prepopulated_lookups,
                )
                if not em7_data_as_snow_interface.snow_device_id:
                    self.logger.info(
                        "Interface id {} has no matching device in "
                        "ServiceNow. Skipping.".format(
                            em7_data_as_snow_interface.em7_interface_id
                        )
                    )
                    continue
                if adapter_sync_setting.lower() == "enabled":
                    if int(interface["ifAdminStatus"]) == 1:
                        sl1_data[
                            str(em7_data_as_snow_interface.em7_interface_id)
                        ] = em7_data_as_snow_interface
                    else:
                        self.logger.info(
                            "Interface {} is Admin Down. Skipping due "
                            "to App Paramaters.".format(
                                em7_data_as_snow_interface.em7_interface_id
                            )
                        )
                elif adapter_sync_setting.lower() == "all":
                    sl1_data[
                        str(em7_data_as_snow_interface.em7_interface_id)
                    ] = em7_data_as_snow_interface
                else:
                    error = (
                        "Invalid adapter_sync_setting: {}. Must be in ["
                        "off, enabled, all]".format(adapter_sync_setting)
                    )
                    raise ipaas_exceptions.StepFailedException(error)

            newly_added_snow_interfaces = list()
            errors = list()
            for interface in snow_interfaces:
                if interface.get("error"):
                    errors.append(interface)
                    continue
                snow_data_as_snow_interface = scoped_service_now_interface_from_snow_data(
                    interface,
                    cmanager=self.cmanager,
                    prepopulated_lookups=prepopulated_lookups,
                )
                if snow_data_as_snow_interface.region == self.region:
                    existing_interface_in_map = snow_data.get(
                        snow_data_as_snow_interface.em7_interface_id
                    )
                    if not existing_interface_in_map:
                        snow_data[
                            snow_data_as_snow_interface.em7_interface_id
                        ] = snow_data_as_snow_interface
                        snow_data_as_snow_interface.correlation.add_or_update_interface(
                            snow_data_as_snow_interface.em7_interface_id,
                            snow_data_as_snow_interface.sys_id,
                        )
                        newly_added_snow_interfaces.append(snow_data_as_snow_interface)
                    else:
                        if (
                            existing_interface_in_map.snow_device_id
                            != snow_data_as_snow_interface.sys_id
                        ):
                            duplicate_interfaces_in_snow.append(
                                snow_data_as_snow_interface
                            )
            if errors:
                self.logger.error("Errors in ServiceNow CI Payload: {}".format(errors))
            self.cmanager.batch_data_and_save_to_cache(
                group_interface_correlations(newly_added_snow_interfaces)
            )

        return snow_data, sl1_data, duplicate_interfaces_in_snow

    @staticmethod
    def find_snow_additions_and_updates(sl1_data, snow_data):
        """
        Determine if SL1 interfaces are new or match existing SNOW CIs.
        Args:
            sl1_data (dict): Dict of servicenow_interface objects.
            snow_data (dict): Dict of servicenow_interface objects.

        Returns: New and Updated Interfaces.

        """
        additions = []
        updates = []
        for if_id, sl1_item in iteritems(sl1_data):
            corresponding_snow_ci = snow_data.get(if_id, None)
            if not corresponding_snow_ci:
                if sl1_item.snow_device_id is not None:
                    additions.append(sl1_item.info_to_post())
            else:
                sl1_item.sys_id = corresponding_snow_ci.sys_id

                snow_interface = snow_data.get(str(if_id))
                if interface_changed(sl1_item, snow_interface):
                    sl1_item.sys_id = snow_interface.sys_id
                    if interface_changed(sl1_item, corresponding_snow_ci):
                        updates.append(sl1_item.info_to_post())

        return additions, updates

    @staticmethod
    def generate_delete_payload(sys_id, company, domain):
        """
        Generate Delete Payload for SNOW.
        Args:
            sys_id (str): Interface sys_id.
            company (str): Interface company sys_id.
            domain (str): Interface domain sys_id.

        Returns: Formatted delete Payload.

        """
        payload = {
            "items": [
                {
                    "className": "cmdb_ci_network_adapter",
                    "values": {
                        "sys_id": sys_id,
                        "company": company,
                        "x_sclo_scilogic_monitored": False,
                    },
                }
            ],
            "relations": [],
        }
        if domain:
            payload["items"][0]["values"].update({"sys_domain": domain})
        return payload

    def find_snow_deletions(self, sl1_data, snow_data, duplicate_interfaces):
        deletes = []
        for dupe_interface in duplicate_interfaces:
            deletes.append(
                self.generate_delete_payload(
                    dupe_interface.sys_id, dupe_interface.company, dupe_interface.domain
                )
            )
            dupe_interface.correlation.remove_interface(dupe_interface.em7_interface_id)
        for if_id, interface in iteritems(snow_data):
            if not sl1_data.get(if_id, None):
                deletes.append(
                    self.generate_delete_payload(
                        interface.sys_id, interface.company, interface.domain
                    )
                )
                interface.correlation.remove_interface(interface.em7_interface_id)

        return deletes

    def dev_sys_lookup_dict(self, sl1_interfaces):
        """ prepopulated_sl1_dev_data -> dict()
        Using the em7 collected data, create a list of all DIDs found. And
        do a bulk lookup for all DIDs in the DB at once

        Args:
            sl1_interfaces (list): list of all devices dicts returned from em7
        Returns:
            dict: did to sys_id mappings

        """
        did_list = []
        chunk_size = get_lookup_chunk_size(self)
        self.logger.info(
            "Querying lookup documents in groups of: {}" "".format(chunk_size)
        )

        for interface_dict in sl1_interfaces:
            dev_id_url = interface_dict.get("device")
            if dev_id_url:
                did_list.append(os.path.basename(dev_id_url))

        return prepopulate_dev_lookups(
            self.region, did_list, logger=self.logger, chunk_size=chunk_size
        )
