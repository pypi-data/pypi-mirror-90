import pickle
from typing import Dict

from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore import parameter_types
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.snow_parameters import (
    chunk_size_param,
    domain_sep_param,
    region_param,
)
from servicenow_cmdb_syncpack.util.cmdb_base_utils import object_changed
from servicenow_cmdb_syncpack.util.cmdb_params import org_attribute_mappings_param
from servicenow_cmdb_syncpack.util.org_utils import SL1Org, ServiceNowCompany


class ProcessOrganizations(BaseStep):
    def __init__(self):
        self.friendly_name = "Process Organizations"
        self.description = "Parse pulled group data from SL1 and ServiceNow"
        self.version = "3.0.1"
        self.new_step_parameter(
            name="Source_of_Truth",
            description="Source of data to sync.",
            required=True,
            default_value="ServiceNow",
            param_type=parameter_types.SelectStaticDropdownParameter(
                ["ScienceLogic", "ServiceNow"]
            ),
        )
        self.new_step_parameter(
            name="Create_Missing",
            description="Enable to create missing Orgs/Companies in Sync Target",
            required=False,
            default_value=False,
            param_type=parameter_types.BoolParameterCheckbox(),
        )
        self.new_step_parameter(
            name="Update_Name",
            description="Enable to update Name/Company values in target system.",
            required=False,
            default_value=False,
            param_type=parameter_types.BoolParameterCheckbox(),
        )
        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(domain_sep_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(org_attribute_mappings_param)

        self.attr_mappings = dict()
        self.region = str()
        self.source_of_truth = str()

    def chunk_snow_payloads(self, snow_company_payloads):
        """
        Chunks ServiceNow Company Payloads.
        Args:
            snow_company_payloads (list): List of ServiceNow Companies to
            Chunk.

        Returns: Chunked Payloads.

        """
        chunk_size = int(self.get_parameter(chunk_size_param.name))
        loop_list = {"records": []}
        chunked_payloads = []
        count = 0

        for snow_company_payload in snow_company_payloads:
            if count + 1 <= chunk_size:
                loop_list["records"].append(snow_company_payload)
            else:
                chunked_payloads.append({"payload": loop_list})
                loop_list = {"records": []}
                count = 0
                loop_list["records"].append(snow_company_payload)
            count += 1
        if loop_list:
            chunked_payloads.append({"payload": loop_list})
        return chunked_payloads

    def org_payload_for_next_step(self, org_uri: str, org_payload: dict):
        return {
            "action": "sl1_create",
            "base_url": "${appvar.sl1_hostname}",
            "user": "${appvar.sl1_user}",
            "password": "${appvar.sl1_password}",
            "uri": org_uri,
            "payload": org_payload,
            "slregion": self.region,
        }

    def process_creates(
        self, sl1_orgs: Dict[str, SL1Org], snow_companies: Dict[str, ServiceNowCompany]
    ):
        create = str_to_bool(self.get_parameter("Create_Missing"))

        self.logger.flow("Source of Truth: {}".format(self.source_of_truth))
        self.logger.flow("Create Missing: {}".format(create))

        mappings = {}
        snow_company_payloads = []
        sl1_creates = []

        self.logger.info("Starting Org search.")
        for org in sl1_orgs.values():
            company = org.match_org_to_company(snow_companies)
            self.logger.debug(u"Org: {}".format(org.name))
            if company:
                sys_id = company.snow_sys_id
                mapping = mappings.get(sys_id)
                if mapping:
                    mapping["sl1"][org.sl1_id] = org
                else:
                    mappings[sys_id] = {"snow": company, "sl1": {org.sl1_id: org}}
            elif self.source_of_truth == "ScienceLogic" and create:
                self.logger.debug("No match found. Creating.")
                snow_company_payloads.append(
                    org.generate_company_payload(
                        self.attr_mappings, sync_name=True, logger=self.logger
                    )
                )
            else:
                self.logger.debug("No Match Found. Skipping due to app params.")
                continue

        self.logger.info("Starting Company Search")
        for snow_company in snow_companies.values():
            if not getattr(snow_company, "name", None):
                self.logger.error(
                    "Invalid company in snow payload. sys_id: {} Skipping".format(
                        snow_company.snow_sys_id
                    )
                )
                continue

            self.logger.debug(
                u"Company: {}, sys_id: {}".format(
                    getattr(snow_company, "name"), snow_company.snow_sys_id
                )
            )
            orgs = snow_company.match_company_to_orgs(sl1_orgs)
            if not orgs and self.source_of_truth == "ServiceNow" and create:
                self.logger.debug("No match found. Creating.")
                org_uri, org_payload = snow_company.generate_org_payload(
                    self.attr_mappings,
                    sync_name=True,
                    action="create",
                    logger=self.logger,
                )
                sl1_creates.append(self.org_payload_for_next_step(org_uri, org_payload))
            else:
                self.logger.debug("No Match Found. Skipping due to app params.")
                continue

        return snow_company_payloads, sl1_creates, mappings

    def process_updates(self, mappings: dict):
        sl1_updates = list()
        snow_updates = list()
        sync_name = str_to_bool(self.get_parameter("Update_Name"))

        self.logger.info("Processing updates.")
        for mapping in mappings.values():
            self.logger.debug(
                u"Processing Company: {}".format(mapping["snow"].snow_sys_id)
            )
            if len(mapping["sl1"]) > 1:
                self.logger.info("Multiple Matching Orgs Found.")
                orgs = [org for org in mapping["sl1"].keys()]
                self.logger.debug(u"Orgs: {}".format(orgs))
                if ",".join(orgs) == mapping["snow"].sl1_id:
                    self.logger.info(
                        "x_sclo_scilogic_id matches orgs list. Continuing."
                    )
                    continue
                else:
                    company_payload = {
                        "vendor": False,
                        "region": self.region,
                        "id": ",".join(orgs),
                        "manufacture": False,
                        "crm_id": mapping["snow"].snow_sys_id,
                    }
                    snow_updates.append(company_payload)
            else:
                missing_id = False
                company = mapping.get("snow")
                if not company:
                    continue
                if company.sl1_id is None:
                    company.sl1_id = next(
                        iter([x.sl1_id for x in mapping["sl1"].values()])
                    )
                    missing_id = True
                    self.logger.info(
                        f"Matching Org and Company found with missing sl1_id in ServiceNow. "
                        f"Updating Company {company.snow_sys_id} with sl1_id: {company.sl1_id}"
                    )
                org = mapping["sl1"].get(company.sl1_id, None)
                if org:
                    if self.source_of_truth == "ServiceNow" and missing_id:
                        snow_updates.append(
                            org.generate_company_payload(
                                {"crm_id": ["crm_id"]},
                                sync_name=False,
                                logger=self.logger,
                            )
                        )
                    update = object_changed(org, company, self.attr_mappings)
                else:
                    self.logger.error(
                        "No organization found for SL ID: {}. "
                        "Check your snow instance to confirm the SL ID field "
                        "is correct.".format(company.sl1_id)
                    )
                    continue
                if update and self.source_of_truth == "ScienceLogic":
                    self.logger.info("Updating ServiceNow Record.")
                    snow_updates.append(
                        org.generate_company_payload(
                            self.attr_mappings, sync_name=sync_name, logger=self.logger
                        )
                    )
                elif update and self.source_of_truth == "ServiceNow":
                    self.logger.info("Updating ScienceLogic Record.")
                    org_uri, org_payload = company.generate_org_payload(
                        self.attr_mappings,
                        sync_name=sync_name,
                        action="update",
                        logger=self.logger,
                    )
                    sl1_updates.append(
                        self.org_payload_for_next_step(org_uri, org_payload)
                    )
                else:
                    self.logger.info("Records are the same, continuing.")
                    continue
        return sl1_updates, snow_updates

    def execute(self):
        self.source_of_truth = self.get_parameter("Source_of_Truth")

        self.attr_mappings = self.get_parameter(org_attribute_mappings_param.name)

        self.region = self.get_parameter(region_param.name)
        sl1_orgs = pickle.loads(
            self.get_data_from_step_by_name("Pull Organizations from SL1")
        )
        snow_companies = pickle.loads(
            self.get_data_from_step_by_name("Pull Companies from ServiceNow")
        )

        snow_company_payloads, sl1_creates, mappings = self.process_creates(
            sl1_orgs, snow_companies
        )

        sl1_updates, snow_updates = self.process_updates(mappings)

        if snow_updates:
            snow_company_payloads.extend(snow_updates)

        payloads = {"snow_payloads": [], "sl1Creates": [], "sl1Updates": []}
        message = ""
        if snow_company_payloads:
            message += "Creating {} Companies.\n".format(len(snow_company_payloads))
            payloads["snow_payloads"] = self.chunk_snow_payloads(snow_company_payloads)
        if sl1_creates:
            message += "Creating {} Organizations. \n".format(len(sl1_creates))
            payloads["sl1Creates"] = sl1_creates
        if sl1_updates:
            message += "Updating {} Organizations. \n".format(len(sl1_updates))
            payloads["sl1Updates"] = sl1_updates
        if payloads:
            self.logger.flow(message)
            self.save_data_for_next_step(payloads)
        else:
            self.logger.flow("No Companies/Orgs to send.")
            self.save_data_for_next_step([])
