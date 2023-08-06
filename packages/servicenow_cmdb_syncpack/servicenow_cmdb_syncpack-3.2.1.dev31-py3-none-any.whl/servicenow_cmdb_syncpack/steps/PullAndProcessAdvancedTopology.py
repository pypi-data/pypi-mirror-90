from base_steps_syncpack.steps.QueryGQL import QueryGQL
from ipaascommon.content_manger import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from servicenow_base_syncpack.util.correlators import (
    DeviceCorrelation,
    prepopulate_dev_lookups,
)
from servicenow_base_syncpack.util.snow_parameters import (
    chunk_size_param,
    domain_sep_param,
    region_param,
)
from servicenow_cmdb_syncpack.util.cmdb_base_utils import chunk_cis
from servicenow_cmdb_syncpack.util.cmdb_constants import RELATION_OVERRIDES
from servicenow_cmdb_syncpack.util.cmdb_params import relation_overrides_param
from servicenow_cmdb_syncpack.util.device_utils import (
    generate_item_payload_from_correlation,
)


class PullAndProcessAdvancedTopology(QueryGQL):
    def __init__(self):
        super(PullAndProcessAdvancedTopology, self).__init__()
        self.friendly_name = "Pull and Process Advanced Topology from SL1"
        self.description = (
            "Pulls Advanced Topology from SL1 via GQL and "
            "Formats Relationships for ServiceNow"
        )
        self.version = "3.1.0"
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(domain_sep_param)
        self.add_step_parameter_from_object(relation_overrides_param)

        self.region = ""
        self.cmanager = None

    def execute(self):
        super(PullAndProcessAdvancedTopology, self).execute()
        self.cmanager = IpaasContentManager()
        self.region = self.get_parameter(region_param.name)
        customer_ci_relation_overrides = self.get_parameter(
            relation_overrides_param.name
        )
        if customer_ci_relation_overrides:
            RELATION_OVERRIDES.update(customer_ci_relation_overrides)

        chunk_size = int(self.get_parameter(chunk_size_param.name))
        domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))
        payloads = chunk_cis(
            self.process_relations(),
            chunk_size,
            domain_sep=domain_sep_enabled,
            logger=self.logger,
        )

        self.logger.flow("Sending {} chunks.".format(len(payloads)))
        self.logger.debug("Final Payloads: {}".format(payloads))
        self.save_data_for_next_step(payloads)

    def process_relations(self):
        sl1_relations = self.get_current_saved_data()
        self.logger.debug("sl1_relations: {}".format(sl1_relations))
        prepopulated_lookups = self.dev_sys_lookup_dict(sl1_relations)
        payloads = []

        for raw_relation in sl1_relations:
            relation = raw_relation["node"]
            parent_did = relation["parentDevice"]["id"]
            parent_correlation = DeviceCorrelation(
                self.region,
                parent_did,
                cmanager=self.cmanager,
                prepopulated_lookups=prepopulated_lookups,
            )
            if not parent_correlation.get_correlating_dev_snow_id():
                self.logger.warning(
                    "No sys_id found in cache for Parent DID: {}. "
                    "Skipping".format(parent_did)
                )
                continue

            child_did = relation["childDevice"]["id"]
            child_correlation = DeviceCorrelation(
                self.region,
                child_did,
                cmanager=self.cmanager,
                prepopulated_lookups=prepopulated_lookups,
            )
            if not child_correlation.get_correlating_dev_snow_id():
                self.logger.warning(
                    "No sys_id found in cache for Parent DID: {}. "
                    "Skipping".format(child_did)
                )
                continue
            relation_type = relation["deviceRelationshipType"]

            if relation_type["id"] in ["102", "3"]:
                # DCM+R + Layer 3
                if relation_type["id"] == "102":
                    payload_type = "DCMR"
                    dcmr_type = relation["dcmrRelationshipType"]["name"]
                    if child_correlation.merged_device:
                        child_snow_ci = child_correlation.get_correlating_dev_merged_info()[
                            "class"
                        ]
                    else:
                        child_snow_ci = child_correlation.get_correlating_dev_snow_ci()
                    if child_snow_ci in RELATION_OVERRIDES:
                        overrides = RELATION_OVERRIDES.get(child_snow_ci, dict()).get(
                            "relations", list()
                        )
                        if parent_correlation.merged_device:
                            parent_snow_ci = parent_correlation.get_correlating_dev_merged_info()[
                                "class"
                            ]
                        else:
                            parent_snow_ci = (
                                parent_correlation.get_correlating_dev_snow_ci()
                            )
                        override = next(
                            iter(
                                [x for x in overrides if x["parent"] == parent_snow_ci]
                            ),
                            {"rel_type": "Connects to::Connected by", "reverse": False},
                        )
                        type_str = override["rel_type"]
                        reverse = override["reverse"]
                    else:
                        type_str = "Connects to::Connected by"
                        reverse = False
                else:
                    payload_type = "device"
                    dcmr_type = "Layer 3"
                    type_str = "IP Connection::IP Connection"
                    reverse = False

                self.logger.debug(
                    "Parent: {} Child: {} Type: {}".format(
                        parent_did, child_did, dcmr_type
                    )
                )
                parent_item_payload = generate_item_payload_from_correlation(
                    parent_correlation, parent_did, payload_type
                )
                child_item_payload = generate_item_payload_from_correlation(
                    child_correlation, child_did, payload_type
                )
            else:  # Layer2 + LLDP + CDP
                payload_type = "interface"
                type_str = "IP Connection::IP Connection"
                r_type = relation_type["type"]
                reverse = False

                if relation.get("parentInterface") and relation.get("childInterface"):
                    parent_ifid = relation["parentInterface"]["id"]
                    if not parent_correlation.get_correlating_dev_interface(
                        parent_ifid
                    ):
                        self.logger.warning(
                            "No sys_id found in cache for parent DID/IF ID: "
                            "{}/{}. Skipping".format(parent_did, parent_ifid)
                        )
                        continue
                    parent_item_payload = generate_item_payload_from_correlation(
                        parent_correlation, parent_ifid, payload_type
                    )

                    child_ifid = relation["childInterface"]["id"]
                    if not child_correlation.get_correlating_dev_interface(child_ifid):
                        self.logger.warning(
                            "No sys_id found in cache for parent DID/IF ID: "
                            "{}/{}. Skipping".format(child_did, child_ifid)
                        )
                        continue
                    child_item_payload = generate_item_payload_from_correlation(
                        child_correlation, child_ifid, payload_type
                    )

                    self.logger.debug(
                        "Parent DID/IF ID: {}/{}, Child DID/IF ID: {}/{}, "
                        "Type: {}".format(
                            parent_did, parent_ifid, child_did, child_ifid, r_type
                        )
                    )
                else:
                    self.logger.error(
                        "Interfaces Missing in Interface Type relationships from SL1. Dropping"
                    )
                    self.logger.debug(f"relation: {relation}")
                    continue

            payloads.append(
                self.snow_relation_payload(
                    parent_item_payload, child_item_payload, type_str, reverse
                )
            )

        self.logger.flow("Sending {} relationships.".format(len(payloads)))
        self.logger.debug("Pre-chunked Payloads: {}".format(payloads))
        return payloads

    def dev_sys_lookup_dict(self, relations):
        """ prepopulated_sl1_dev_data -> dict()
        Using the em7 collected data, create a list of all dids found. And
        do a bulk lookup for all dids in the DB at once
        Args:
            relations (list): list of all devices dicts returned from em7
        Returns:
            dict: did to sys_id mappings

        """
        did_set = set()
        for relation in relations:
            did_set.add(relation["node"]["parentDevice"]["id"])
            did_set.add(relation["node"]["childDevice"]["id"])
        return prepopulate_dev_lookups(self.region, list(did_set))

    @staticmethod
    def snow_relation_payload(
        parent: dict, child: dict, rel_type: str, reverse: bool
    ) -> dict:
        """
        Generates full relation payload for ServiceNow
        Args:
            parent (dict): Parent Item Payload
            child (dict): Child Item Payload
            rel_type (str): Relation Type String.
            reverse: Is relation reversed

        Returns: Identification Engine Payload.

        """
        if reverse:
            relations = [{"child": 0, "parent": 1, "type": rel_type}]
        else:
            relations = [{"child": 1, "parent": 0, "type": rel_type}]
        payload = {"items": [parent, child], "relations": relations}
        return payload
