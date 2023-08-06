from os.path import basename
from typing import Dict, Tuple, Optional
from jinja2.exceptions import TemplateError
import json

from servicenow_cmdb_syncpack.util.cmdb_base_utils import CMDBObject


class Company(CMDBObject):
    """Base Device class to provide common functions."""

    def is_usable_attribute(self, *args):
        raise NotImplementedError

    def __init__(self, sl1_id: str, region: str, sys_id: str):
        super(Company, self).__init__(sl1_id, region, sys_id=sys_id)

    def eval_template(self, template: str, logger=None) -> (str, None):
        """
        Evaluate Attribute Template.

        Args:
            template: Template to evaluate.
            logger: IpaasLogger from step.

        Returns:

        """
        try:
            value = super(Company, self).eval_template(
                template=template, obj_type="company"
            )
        except TemplateError as err:
            if logger:
                if isinstance(self, SL1Org):
                    type_msg = f"SL1 Org ID: {self.sl1_id}"
                else:
                    type_msg = f"ServiceNow Company sys_id: {self.snow_sys_id}"
                logger.warning(
                    f"Exception caught while processing Template: {template} "
                    f"for {type_msg}. Check Debug logs for more info."
                )
                logger.debug(
                    f"Exception: {err}, "
                    f"Device Properties: "
                    f"{json.dumps(self.__dict__, sort_keys=True)}"
                )
            return None
        else:
            return value


class SL1Org(Company):
    """SL1Org: Defines a SL1 Organization"""

    def __init__(self, uri: str, org_dict: dict, region: str):
        super(SL1Org, self).__init__(
            sl1_id=basename(uri), region=region, sys_id=org_dict.get("crm_id")
        )
        # Delete stuff we don't care about
        try:
            del org_dict["notes"]
        except KeyError:
            pass
        try:
            del org_dict["logs"]
        except KeyError:
            pass

        self.name = org_dict.pop("company", None)
        self.dict_to_properties(org_dict.pop("custom_fields", dict()))
        self.dict_to_properties(org_dict)

    def is_usable_attribute(self, sl1_field: str) -> bool:
        if "{{" in sl1_field:
            return True
        elif not getattr(self, sl1_field, None):
            return False
        elif not getattr(self, sl1_field):
            return False
        else:
            return True

    def generate_company_payload(
        self, mappings: dict, sync_name: bool = False, logger=None
    ):
        """
        Generates Company Payload to post to ServiceNow.
        Args:
            mappings: Field Mappings
            sync_name (bool): Update name - Appvar.
            logger: IS Logger from Step

        Returns: Formatted payload to post to ServiceNow.

        """
        company_payload = {"region": self.region, "id": self.sl1_id}
        for sl1_attr, snow_attrs in mappings.items():
            if not self.is_usable_attribute(sl1_attr):
                continue
            if "{{" in sl1_attr:
                sl1_value = self.eval_template(sl1_attr, logger=logger)
            else:
                sl1_value = getattr(self, sl1_attr)
            if not sl1_value:
                continue
            for snow_attr in snow_attrs:
                if snow_attr == "sys_id":
                    continue
                else:
                    company_payload[snow_attr] = sl1_value

        if sync_name:
            company_payload["name"] = self.name
        return company_payload

    def match_org_to_company(
        self, snow_companies: Dict[str, CMDBObject]
    ) -> Optional[CMDBObject]:
        """
        Match org to ServiceNow Company
        Args:
            snow_companies: ServiceNow Companies,

        Returns: Matched Companies.

        """
        company = snow_companies.get(self.snow_sys_id)
        if not company:
            try:
                company = next(
                    iter(
                        [x for x in snow_companies.values() if x.sl1_id == self.sl1_id]
                    )
                )
            except StopIteration:
                try:
                    company = next(
                        iter(
                            [
                                x
                                for x in snow_companies.values()
                                if getattr(x, "name").lower() == self.name.lower()
                            ]
                        )
                    )
                except StopIteration:
                    return None

        return company


class ServiceNowCompany(Company):
    def __init__(self, company_dict: dict):
        super(ServiceNowCompany, self).__init__(
            sl1_id=company_dict.pop("x_sclo_scilogic_id", None),
            region=company_dict.pop("x_sclo_scilogic_region"),
            sys_id=company_dict.pop("sys_id"),
        )
        self.domain = company_dict.pop("sys_domain", None)
        if self.domain == "global":
            self.domain = None
        self.dict_to_properties(company_dict)

    def is_usable_attribute(self, snow_field: str, sl1_field: str) -> bool:
        if snow_field == "crm_id":
            return False

        elif "{{" in snow_field:
            return True
        elif not getattr(self, snow_field, None):
            return False
        elif not getattr(self, snow_field):
            return False
        elif (
            "date" in sl1_field.lower() and getattr(self, snow_field, "") < "1900-01-01"
        ):
            return False
        else:
            return True

    def generate_org_payload(
        self,
        mappings: dict,
        sync_name: bool = False,
        action: str = "update",
        logger=None,
    ) -> Tuple[str, Dict[str, str]]:
        """
        Generates Org Payload to post to SL1.
        Args:
            mappings: Field Mappings
            sync_name (bool): Update name - Appvar.
            action (str): Action type needed to determine URI.
            logger: IS Logger from Step.

        Returns: Formatted payload to post to SL1.

        """
        uri = "/api/organization"

        if action == "update":
            uri += f"/{self.sl1_id}"

        org_payload = dict()
        for sl1_attr, snow_attrs in mappings.items():
            for snow_attr in snow_attrs:
                if snow_attr == "sys_id":
                    snow_value = self.snow_sys_id
                elif not self.is_usable_attribute(snow_attr, sl1_attr):
                    continue
                elif "{{" in snow_attr:
                    snow_value = self.eval_template(snow_attr, logger=logger)
                else:
                    snow_value = getattr(self, snow_attr, None)

                if snow_value:
                    org_payload[sl1_attr] = snow_value

        if sync_name:
            org_payload["company"] = getattr(self, "name")
        return uri, org_payload

    def match_company_to_orgs(self, sl1_orgs: Dict[str, SL1Org]) -> Optional[SL1Org]:
        """
        Match Companies to ScienceLogic Orgs.
        Returns: Matched Orgs.

        """
        try:
            org = next(
                iter(
                    [x for x in sl1_orgs.values() if x.snow_sys_id == self.snow_sys_id]
                )
            )
        except StopIteration:
            org = sl1_orgs.get(self.sl1_id)
            if not org:
                try:
                    org = next(
                        iter(
                            [
                                x
                                for x in sl1_orgs.values()
                                if x.name.lower()
                                == getattr(self, "name", str()).lower()
                            ]
                        )
                    )
                except StopIteration:
                    return None
        return org
