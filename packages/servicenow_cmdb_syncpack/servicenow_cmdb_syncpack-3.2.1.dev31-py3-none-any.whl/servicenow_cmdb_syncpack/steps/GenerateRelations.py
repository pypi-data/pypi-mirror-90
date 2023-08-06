from collections import namedtuple
from json import dumps

from base_steps_syncpack.steps.QueryGQL import QueryGQL
from ipaascommon.ipaas_exceptions import (
    MissingRequiredStepParameter,
    StepFailedException,
)
from ipaascommon.ipaas_manager import IpaasContentManager
from servicenow_base_syncpack.util.helpers import invert_mappings, validate_mappings
from servicenow_base_syncpack.util.servicenow_exceptions import InvalidMappings
from servicenow_cmdb_syncpack.util.cmdb_params import ci_attrib_mappings_param
from servicenow_cmdb_syncpack.util.device_utils import ServiceNowCIList


class GenerateRelations(QueryGQL):
    def __init__(self):
        super(GenerateRelations, self).__init__()
        self.friendly_name = "Generate CI Relations"
        self.description = "Generates CI Relations for ServiceNow"
        self.version = "2.1.0"
        self.add_step_parameter_from_object(ci_attrib_mappings_param)

    def execute(self):
        super(GenerateRelations, self).execute()
        missing_relations, found_relations = self.generate_relations()
        if missing_relations:
            self.logger.flow(u"Missing Relations: {}".format(dumps(missing_relations)))
        else:
            self.logger.flow("No missing relations found!")
        self.logger.info(u"Found Relations: {}".format(dumps(found_relations)))
        self.save_data_for_next_step(dict())

    def generate_relations(self):
        sl1_data = self.get_current_saved_data()
        mappings = self.get_parameter(ci_attrib_mappings_param.name)
        cmanager = IpaasContentManager()
        if not mappings:
            dev_sync_vars = cmanager.get_application_dict_from_db(
                "Device_Sync_ScienceLogic_To_ServiceNow"
            ).get("app_variables")
            mappings = next(
                (x["value"] for x in dev_sync_vars if x["name"] == "mappings"), None
            )
            if not mappings:
                raise MissingRequiredStepParameter(
                    "{} is required but is not populated in either {} or in "
                    "Device_Sync_ScienceLogic_To_ServiceNow.".format(
                        ci_attrib_mappings_param.name, self.application_name
                    )
                )
        try:
            validate_mappings(mappings)
        except InvalidMappings as err:
            self.logger.error("{}: {}".format(err[0], err[1]))
            raise StepFailedException(err)

        inverted_mappings = invert_mappings(mappings)
        cis = ServiceNowCIList(cmanager=cmanager)

        self.logger.debug("sl1_data: {}".format(sl1_data))
        # Mappings of em7 id to device
        valid_relations_set = set()
        invalid_relations_set = set()
        missing_relations_list = list()
        found_relations_list = list()
        bad_sl1_payload = int()
        missing_mappings = int()

        Relation = namedtuple("Relation", "parent child")

        for raw_device_dict in sl1_data:
            device_dict = raw_device_dict["node"]
            child_dict = device_dict["childDevice"]
            if child_dict and isinstance(child_dict, dict):
                child_device = {
                    "id": child_dict.get("id"),
                    "class": u"{} | {}".format(
                        child_dict.get("deviceClass", dict()).get("class"),
                        child_dict.get("deviceClass", {}).get("description"),
                    ),
                }
            else:
                bad_sl1_payload += 1
                continue

            parent_dict = device_dict["parentDevice"]
            if parent_dict and isinstance(parent_dict, dict):
                parent_device = {
                    "id": parent_dict.get("id"),
                    "class": u"{} | {}".format(
                        parent_dict.get("deviceClass", dict()).get("class"),
                        parent_dict.get("deviceClass", dict()).get("description"),
                    ),
                }
            else:
                bad_sl1_payload += 1
                continue

            self.logger.debug(
                u"parent_device: {}\n child_device: {}".format(
                    parent_device, child_device
                )
            )

            child_device["ci"] = inverted_mappings.get(child_device["class"])
            parent_device["ci"] = inverted_mappings.get(parent_device["class"])

            if not child_device["ci"] or not parent_device["ci"]:
                missing_mappings += 1
                self.logger.debug(
                    "Missing Mapping for Device. Parent: {}, Child: {}".format(
                        parent_device, child_device
                    )
                )
                continue

            rel = Relation(parent_device["ci"], child_device["ci"])
            self.logger.debug("relation: {}".format(rel))
            if rel in valid_relations_set or rel in invalid_relations_set:
                continue
            try:
                cis.get_child_ci(child_device["ci"], parent_device["ci"])
            except AttributeError:
                invalid_relations_set.add(rel)
            else:
                valid_relations_set.add(rel)

        for relation in invalid_relations_set:
            missing_relations_list.append(
                {"parent": relation.parent, "child": relation.child}
            )

        for relation in valid_relations_set:
            found_relations_list.append(
                {"parent": relation.parent, "child": relation.child}
            )

        if bad_sl1_payload:
            self.logger.warning(
                "{} bad payloads received from SL1. Re-run app in debug to "
                "troubleshoot.".format(bad_sl1_payload)
            )

        if missing_mappings:
            self.logger.warning(
                "{} Relations with missing mappings detected. Please re-run "
                "app with loglevel 10 to troubleshoot.".format(missing_mappings)
            )

        return missing_relations_list, found_relations_list
