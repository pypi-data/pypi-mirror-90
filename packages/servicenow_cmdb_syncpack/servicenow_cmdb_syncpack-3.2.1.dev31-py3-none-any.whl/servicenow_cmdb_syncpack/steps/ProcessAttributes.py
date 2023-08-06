import pickle
from typing import Dict

from ipaascore.BaseStep import BaseStep
from servicenow_cmdb_syncpack.util.cmdb_base_utils import object_changed
from servicenow_cmdb_syncpack.util.cmdb_params import attribs_snow_to_sl_param
from servicenow_cmdb_syncpack.util.device_utils import (
    SL1Device,
    ServiceNowDevice,
    chunk_db_queries,
)


class ProcessAttributes(BaseStep):
    def __init__(self):
        self.friendly_name = "Process ServiceNow Attributes"
        self.description = (
            "Processes ServiceNow Attributes and converts to SL1 Asset Data."
        )
        self.version = "2.0.0"
        self.add_step_parameter_from_object(attribs_snow_to_sl_param)

    def execute(self):
        sl1_devices = pickle.loads(
            self.get_data_from_step_by_name("Pull and Process SL1 Devices")
        )
        snow_devices = pickle.loads(
            self.get_data_from_step_by_name("Pull and Process ServiceNow CIs")
        )

        db_queries, rest_posts = self.process_updates(sl1_devices, snow_devices)

        self.save_data_for_next_step(
            {"db_queries": chunk_db_queries(db_queries), "rest_posts": rest_posts}
        )

    def process_updates(
        self,
        sl1_device_map: Dict[str, SL1Device],
        snow_device_map: Dict[str, ServiceNowDevice],
    ):
        """
        Parse Updates
        Args:
            sl1_device_map (dict): SL1 Device Objects.
            snow_device_map (dict): ServiceNow Device Objects.

        Returns:

        """
        attr_mappings = self.get_parameter(attribs_snow_to_sl_param.name)
        queries = []
        rest_posts = []
        for key, sl1_item in sl1_device_map.items():
            snow_ci = snow_device_map.get(key, None)
            if not snow_ci:
                self.logger.debug(
                    f"SL1 device: {getattr(sl1_item, 'name')} (id: {sl1_item.sl1_id}) "
                    f"does not have a corresponding ci in ServiceNow. Skipping."
                )
                continue
            else:
                if object_changed(
                    sl1_item, snow_ci, attr_mappings=attr_mappings, logger=self.logger
                ):
                    query, attributes = snow_ci.generate_attribute_update_queries(
                        attr_mappings, sl1_item.asset_id, self.logger
                    )
                    if sl1_item.asset_id and query:
                        queries.append(query)
                    else:
                        self.logger.info(
                            "No Asset Record found for DID {}. "
                            "Skipping".format(sl1_item.sl1_id)
                        )
                    if attributes:
                        rest_posts.append(
                            {"attributes": attributes, "did": snow_ci.sl1_id}
                        )
                else:
                    continue

        self.logger.debug("List of asset update queries for SL1: {}".format(queries))
        self.logger.debug("List of custom attribute updates: {}".format(rest_posts))

        return queries, rest_posts
