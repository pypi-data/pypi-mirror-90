from future.utils import iteritems

from ipaascommon.ipaas_manager import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.correlators import (
    DeviceCorrelation,
    prepopulate_dev_lookups,
)
from servicenow_base_syncpack.util.helpers import (
    fix_query_rest_result,
    generate_item_payload_from_correlation,
)
from servicenow_base_syncpack.util.snow_parameters import (
    chunk_size_param,
    domain_sep_param,
    generate_service_classification_param,
    region_param,
    sl1_hostname_param,
)
from servicenow_cmdb_syncpack.util.cmdb_base_utils import chunk_cis
from servicenow_cmdb_syncpack.util.cmdb_params import sl1_url_override_param


class ProcessBusinessServices(BaseStep):
    def __init__(self):
        self.friendly_name = "Process Business Services"
        self.description = (
            "Processes SL1 Business Services and formats for " "ServiceNow."
        )
        self.version = "1.1.0"

        self.add_step_parameter_from_object(region_param)
        self.add_step_parameter_from_object(domain_sep_param)
        self.add_step_parameter_from_object(chunk_size_param)
        self.add_step_parameter_from_object(sl1_hostname_param)
        self.add_step_parameter_from_object(sl1_url_override_param)

        classification_params = {
            "business_service": "Business Service",
            "it_service": "Application Service",
            "device_service": "Technical Service",
        }
        for (service, default) in iteritems(classification_params):
            self.add_step_parameter_from_object(
                generate_service_classification_param(service, default)
            )

        self.region = ""
        self.cmanager = None
        self.domain_sep_enabled = bool()
        self.snow_companies = list()
        self.services = list()
        self.org_data = dict()
        self.prepopulated_lookups = dict()
        self.ci_class = "cmdb_ci_service"
        self.base_url = ""

    def execute(self):
        self.cmanager = IpaasContentManager()
        self.region = self.get_parameter(region_param.name)
        chunk_size = int(self.get_parameter(chunk_size_param.name))
        self.domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))
        self.snow_companies = self.get_data_from_step_by_name(
            "Pull Companies from ServiceNow"
        )
        self.services = self.get_data_from_step_by_name(
            "Fetch Business Services from SL1"
        )
        self.org_data = fix_query_rest_result(
            self.get_data_from_step_by_name("Fetch Orgs from SL1")
        )
        self.prepopulated_lookups = self.dev_sys_lookup_dict(self.services)
        url_override = self.get_parameter(sl1_url_override_param.name)
        if url_override.strip():
            self.base_url = "https://{}/inventory/services".format(url_override.strip())
        else:
            self.base_url = "https://{}/inventory/services".format(
                self.get_parameter(sl1_hostname_param.name)
            )

        payloads = chunk_cis(
            self.process_business_services(),
            chunk_size,
            domain_sep=self.domain_sep_enabled,
            logger=self.logger,
        )

        self.logger.flow("Sending {} chunks.".format(len(payloads)))
        self.logger.debug("Final Payloads: {}".format(payloads))
        self.save_data_for_next_step(payloads)

    def process_business_services(self):
        """
        Processes SL1 Business/IT/Device Services and returns payloads for
        ServiceNow.

        Returns:
            list: ServiceNow Payloads
        """
        self.logger.debug("sl1_services: {}".format(self.services))

        service_classifications = {
            "businessService": self.get_parameter("business_service_classification"),
            "itService": self.get_parameter("it_service_classification"),
            "deviceService": self.get_parameter("device_service_classification"),
        }

        unsupported_services = [
            "applicationComponent",
            "application",
        ]  # TODO: INT-2458

        payloads = []

        for raw_service in self.services:
            service = raw_service["service"]
            if service["type"] in unsupported_services:
                continue
            org_lookup = "/api/organization/{}".format(service["organization"]["id"])
            company = self.org_data.get(org_lookup, {}).get("crm_id", None)

            service_payload = {
                "className": self.ci_class,
                "values": {
                    "name": service["name"],
                    "short_description": service["description"],
                    "service_classification": service_classifications.get(
                        service["type"]
                    ),
                    "company": company,
                    "correlation_id": service["id"],
                    "x_sclo_scilogic_region": self.region,
                    "x_sclo_scilogic_url": "{}/{}/overview".format(
                        self.base_url, service["id"]
                    ),
                },
            }
            if self.domain_sep_enabled:
                domains = [
                    x.get("sys_domain")
                    for x in self.snow_companies
                    if x["sys_id"] == company
                ]
                if domains:
                    service_payload["values"]["sys_domain"] = domains[0]

            children = self.get_children(service)

            payloads.append(self.snow_relation_payload(service_payload, children))

        self.logger.flow("Sending {} Business Services.".format(len(payloads)))
        self.logger.debug("Pre-chunked Payloads: {}".format(payloads))

        return payloads

    def dev_sys_lookup_dict(self, services):
        """ prepopulated_sl1_dev_data -> dict()
        Using the em7 collected data, create a list of all dids found. And
        do a bulk lookup for all dids in the DB at once
        Args:
            services (list): list of all devices dicts returned from em7
        Returns:
            dict: did to sys_id mappings

        """
        did_set = set()
        for service in services:
            service = service["service"]
            if service["type"] == "deviceService":
                for device in service["constituents"]["edges"]:
                    did_set.add(device["node"]["id"])
            else:
                continue
        return prepopulate_dev_lookups(self.region, list(did_set))

    @staticmethod
    def snow_relation_payload(parent, children):
        """
        Generates full relation payload for ServiceNow
        Args:
            parent (dict): Parent Item Payload
            children (list): List of Child Item Payloads

        Returns: Identification Engine Payload.

        """
        if len(children) > 0:
            items = list()
            items.append(parent)
            items.extend(children)

            relations = list()
            for i in range(len(children)):
                relations.append(
                    {"child": i + 1, "parent": 0, "type": "Depends on::Used by"}
                )

            payload = {"items": items, "relations": relations}
        else:
            payload = {"items": [parent]}
        return payload

    def get_children(self, service):
        """
        Get children payloads.

        Args:
            service (dict): Service Dictionary.

        Returns:
            list: List of child payloads.
        """
        children = list()
        if service["type"] == "deviceService":
            for device in service["constituents"]["edges"]:
                correlation = DeviceCorrelation(
                    self.region,
                    device["node"]["id"],
                    cmanager=self.cmanager,
                    prepopulated_lookups=self.prepopulated_lookups,
                )
                if correlation.get_correlating_dev_snow_id():
                    children.append(
                        generate_item_payload_from_correlation(
                            correlation, device["node"]["id"], "device"
                        )
                    )
                else:
                    self.logger.warning(
                        "No sys_id found in cache for DID: {}. "
                        "Skipping".format(device["node"]["id"])
                    )
                    continue

        else:  # Business Service, IT Service
            for raw_child_service in service["constituents"]["edges"]:
                child_service = raw_child_service["node"]
                child_org_lookup = "/api/organization/{}".format(
                    child_service["organization"]["id"]
                )
                child_company = self.org_data.get(child_org_lookup, {}).get(
                    "crm_id", None
                )

                child_payload = {
                    "className": self.ci_class,
                    "values": {
                        "name": child_service["name"],
                        "company": child_company,
                        "correlation_id": child_service["id"],
                    },
                }
                if self.domain_sep_enabled:
                    domains = [
                        x.get("sys_domain")
                        for x in self.snow_companies
                        if x["sys_id"] == child_company
                    ]
                    if domains:
                        child_payload["values"]["sys_domain"] = domains[0]
                children.append(child_payload)

        return children
