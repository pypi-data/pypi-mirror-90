from itertools import chain

from future.utils import iteritems

from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.correlators import prepopulate_dev_lookups
from servicenow_base_syncpack.util.snow_parameters import (
    chunk_size_param,
    domain_sep_param,
    region_param,
)
from servicenow_cmdb_syncpack.util.cmdb_base_utils import chunk_cis
from servicenow_cmdb_syncpack.util.file_system_utils import (
    file_system_changed,
    servicenow_ci_from_sl1_fs_data,
    servicenow_ci_from_snow_data,
)


class CompareFileSystems(BaseStep):
    def __init__(self):
        self.friendly_name = "Compare SL1 File Systems and ServiceNow CIs"
        self.description = (
            "Compares SL1 File Systems and ServiceNow CIs for " "Syncing to ServiceNow"
        )
        self.version = "1.1.0"
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(domain_sep_param)

        self.cmanager = None
        self.region = str()

    def execute(self):
        save_data = {}
        self.cmanager = IpaasContentManager()
        self.region = self.get_parameter(region_param.name)

        snow_data, sl1_data, duplicates = self.get_file_systems()
        new_file_systems, update_file_systems = self.find_snow_additions_and_updates(
            sl1_data, snow_data
        )

        delete_file_systems = self.find_snow_deletions(sl1_data, snow_data, duplicates)

        save_data.update(
            {
                "creates": new_file_systems,
                "updates": update_file_systems,
                "deletes": delete_file_systems,
            }
        )

        self.logger.flow(
            "Sending {} Creates, {} Updates, and {} Disconnections to "
            "ServiceNow".format(
                len(save_data["creates"]),
                len(save_data["updates"]),
                len(save_data["deletes"]),
            )
        )
        self.logger.debug(
            u"Creates: {}\n Updates: {}\n Disconnects: {}".format(
                save_data["creates"], save_data["updates"], save_data["deletes"]
            )
        )

        domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))
        chunk_size = int(self.get_app_variable(chunk_size_param.name))
        payloads = chunk_cis(
            chain.from_iterable(save_data.values()),
            chunk_size,
            domain_sep=domain_sep_enabled,
            logger=self.logger,
        )

        self.logger.flow("Sending {} chunks.".format(len(payloads)))
        self.logger.debug(u"Final Payloads: {}".format(payloads))
        self.save_data_for_next_step(payloads)

    def get_file_systems(self):
        snow_file_systems = self.get_data_from_step_by_name(
            "Fetch File Systems from ServiceNow"
        ).get("results", list())
        sl1_file_systems = self.get_data_from_step_by_name(
            "Fetch File Systems from SL1"
        )
        prepopulated_lookups = self.dev_sys_lookup_dict(sl1_file_systems)

        self.logger.debug(u"SNOW File Systems: {}".format(snow_file_systems))
        self.logger.debug(u"SL1 File Systems: {}".format(sl1_file_systems))

        sl1_data = {}
        snow_data = {}
        duplicates = []
        errors = list()

        for sl1_fs in sl1_file_systems:
            sl1_fs_object = servicenow_ci_from_sl1_fs_data(
                sl1_fs,
                self.region,
                cmanager=self.cmanager,
                prepopulated_lookups=prepopulated_lookups,
            )
            if not sl1_fs_object.snow_device_id:
                self.logger.info(
                    "FS id {} has no matching device in "
                    "ServiceNow. Skipping.".format(sl1_fs_object.sl1_fs_id)
                )
                continue
            sl1_data[str(sl1_fs_object.sl1_fs_id)] = sl1_fs_object

        for snow_fs in snow_file_systems:
            if snow_fs.get("error"):
                errors.append(snow_fs)
                continue
            snow_fs_object = servicenow_ci_from_snow_data(snow_fs)
            if snow_fs_object.region == self.region:
                existing_file_systems = snow_data.get(snow_fs_object.sl1_fs_id)
                if not existing_file_systems:
                    snow_data[snow_fs_object.sl1_fs_id] = snow_fs_object
                else:
                    if existing_file_systems.snow_device_id != snow_fs_object.sys_id:
                        duplicates.append(snow_fs_object)
        if errors:
            self.logger.error("Errors in ServiceNow CI Payload: {}".format(errors))

        return snow_data, sl1_data, duplicates

    @staticmethod
    def find_snow_additions_and_updates(sl1_data, snow_data):
        """
        Determine if SL1 File Systems are new or match existing SNOW CIs.
        Args:
            sl1_data (dict): Dict of servicenow_file_system objects.
            snow_data (dict): Dict of servicenow_file_system objects.

        Returns: New and Updated File Systems.

        """
        additions = []
        updates = []
        for (fs_id, sl1_item) in iteritems(sl1_data):
            corresponding_snow_ci = snow_data.get(fs_id, None)
            if not corresponding_snow_ci:
                if sl1_item.snow_device_id is not None:
                    additions.append(sl1_item.info_to_post())
            else:
                sl1_item.sys_id = corresponding_snow_ci.sys_id

                snow_fs = snow_data.get(str(fs_id))
                if file_system_changed(sl1_item, snow_fs):
                    sl1_item.sys_id = snow_fs.sys_id
                    if file_system_changed(sl1_item, corresponding_snow_ci):
                        updates.append(sl1_item.info_to_post())

        return additions, updates

    @staticmethod
    def generate_delete_payload(sys_id, company, domain):
        """
        Generate Delete Payload for SNOW.
        Args:
            sys_id (str): File System sys_id.
            company (str): File System company sys_id.
            domain (str): File System domain sys_id.

        Returns: Formatted delete Payload.

        """
        payload = {
            "items": [
                {
                    "className": "cmdb_ci_file_system",
                    "values": {
                        "sys_id": sys_id,
                        "company": company,
                        "x_sclo_scilogic_monitored": False,
                        "operational_status": 6,
                        "install_status": 7,
                    },
                }
            ],
            "relations": [],
        }
        if domain:
            payload["items"][0]["values"].update({"sys_domain": domain})
        return payload

    def find_snow_deletions(self, sl1_data, snow_data, duplicates):
        deletes = []
        for duplicate in duplicates:
            deletes.append(
                self.generate_delete_payload(
                    duplicate.sys_id, duplicate.company, duplicate.domain
                )
            )
        for (fs_id, file_system) in iteritems(snow_data):
            if not sl1_data.get(fs_id, None):
                deletes.append(
                    self.generate_delete_payload(
                        file_system.sys_id, file_system.company, file_system.domain
                    )
                )
        return deletes

    def dev_sys_lookup_dict(self, sl1_file_systems):
        """ prepopulated_sl1_dev_data -> dict()
        Using the SL1 collected data, create a list of all dids found. And
        do a bulk lookup for all dids in the DB at once
        Args:
            sl1_file_systems (list): list of all devices dicts returned from SL1
        Returns:
            dict: did to sys_id mappings

        """
        did_list = []
        for fs_dict in sl1_file_systems:
            dev_id = fs_dict.get("did")
            if dev_id:
                did_list.append(dev_id)

        return prepopulate_dev_lookups(self.region, did_list)
