from future.moves.itertools import zip_longest

from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.correlators import (
    DeviceCorrelation,
    prepopulate_dev_lookups,
)
from servicenow_base_syncpack.util.snow_parameters import chunk_size_param, region_param


class CompareSoftware(BaseStep):
    def __init__(self):
        self.friendly_name = "Compare SL1 Software and ServiceNow CIs"
        self.description = (
            "Compares SL1 Software and ServiceNow CIs for Syncing to ServiceNow"
        )
        self.version = "1.0.1"
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(chunk_size_param)

        self.cmanager = None
        self.region = str()

    def execute(self):
        self.cmanager = IpaasContentManager()
        self.region = self.get_parameter(region_param.name)
        chunk_size = int(self.get_parameter(chunk_size_param.name))

        software = self.get_software_payloads()
        chunks = self.grouper(chunk_size, software)
        payloads = list()
        for chunk in chunks:
            payloads.append([{"records": chunk}])

        self.logger.flow("Sending {} chunks.".format(len(payloads)))

        self.save_data_for_next_step(payloads)

    def get_software_payloads(self):
        snow_software = self.get_data_from_step_by_name(
            "Pull and Parse ServiceNow Software"
        ).get("results")
        sl1_software = self.get_data_from_step_by_name(
            "Fetch Installed Software from SL1"
        )
        prepopulated_lookups = self.dev_sys_lookup_dict()

        self.logger.debug(u"SNOW Software: {}".format(snow_software))
        self.logger.debug(u"SL1 Software: {}".format(sl1_software))

        payloads = list()

        for sl1_sw in sl1_software:
            snow_sw = snow_software.get(sl1_sw.get("title"))
            if not snow_sw:
                self.logger.info(
                    "{} has no matching software package in "
                    "ServiceNow. Skipping.".format(sl1_sw.get("title"))
                )
                continue
            dids = sl1_sw.get("dids").split(",")
            if not dids:
                self.logger.info(
                    "{} has no devices aligned. Skipping".format(sl1_sw.get("title"))
                )
                continue
            sw_payload = {
                "software": snow_sw.get("sys_id"),
                "active": True,
                "cmdb_ci": list(),
                "name": sl1_sw.get("title"),
            }

            for did in dids:
                if did not in snow_sw.get("dids"):
                    correlation = DeviceCorrelation(
                        self.region,
                        did,
                        cmanager=self.cmanager,
                        prepopulated_lookups=prepopulated_lookups,
                    )
                    if not correlation.get_correlating_dev_snow_id():
                        self.logger.info(
                            "DID {} has no matching Device in cache. Skipping.".format(
                                did
                            )
                        )
                        continue
                    sw_payload["cmdb_ci"].append(
                        correlation.get_correlating_dev_snow_id()
                    )
                else:
                    self.logger.debug(
                        "{} already connected to did {} in ServiceNow. Skipping.".format(
                            sl1_sw.get("title"), did
                        )
                    )
            if not sw_payload["cmdb_ci"]:
                self.logger.info(
                    "{} has no devices aligned. Skipping".format(sl1_sw.get("title"))
                )
                continue
            else:
                payloads.append(sw_payload)

        self.logger.flow(
            "Sending {} Installed Software Payloads to ServiceNow".format(len(payloads))
        )
        self.logger.debug(u"payloads: {}".format(payloads))

        return payloads

    def dev_sys_lookup_dict(self):
        """ prepopulated_sl1_dev_data -> dict()
        Using the SL1 collected data, create a list of all dids found. And
        do a bulk lookup for all dids in the DB at once
        Returns:
            dict: did to sys_id mappings

        """
        did_list = (
            self.get_data_from_step_by_name(
                "Fetch DIDs with Installed Software from SL1"
            )[0]
            .get("dids", str())
            .split(",")
        )

        return prepopulate_dev_lookups(self.region, did_list)

    @staticmethod
    def grouper(chunk_size, payloads):
        """
        Takes list and converts to list of lists.

        Args:
            chunk_size (int): Number of items per chunk.
            payloads (list): List to chunk

        Returns:
            list: List of lists
        """
        return [
            [entry for entry in iterable if entry is not None]
            for iterable in zip_longest(*[iter(payloads)] * chunk_size, fillvalue=None)
        ]
