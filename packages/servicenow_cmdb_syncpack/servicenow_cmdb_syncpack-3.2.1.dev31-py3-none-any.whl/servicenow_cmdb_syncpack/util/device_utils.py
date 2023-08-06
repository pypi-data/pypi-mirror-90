from __future__ import annotations

import json
from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from couchbase.exceptions import NotFoundError
from jinja2.exceptions import TemplateError

from ipaascommon import ipaas_exceptions
from ipaascommon.content_manger import IpaasContentManager
from ipaascommon.ipaas_utils import singleton, str_to_bool
from servicenow_base_syncpack.util.correlators import (
    DeviceCorrelation,
    prepopulate_dev_lookups,
)
from servicenow_base_syncpack.util.snow_constants import (
    SERVICENOW_DEFAULT_ID,
    SL1_DEV_CLASS_CACHE_KEY_PREFIX,
    SNOW_CI_CACHE_KEY_PREFIX,
)
from servicenow_cmdb_syncpack.util.cmdb_base_utils import (
    CMDBObject,
    sl1_transform_to_snow,
)
from servicenow_cmdb_syncpack.util.cmdb_exceptions import MissingRelationsException
from servicenow_cmdb_syncpack.util.org_utils import SL1Org


class ScienceLogicDeviceClassList(object):
    """
    Singleton class which contains the list of all ServiceNowCi Classes
    Should only query cache once, regardless of how many times its instantiated
    """

    def __init__(
        self,
        region="ScienceLogicRegion",
        logger=None,
        cmanager=None,
        force_new=False,
        mappings=None,
        org_filter=None,
        cug_filter=None,
    ):
        if not cmanager:
            cmanager = IpaasContentManager()
        try:
            ci_list = cmanager.load_from_cache_by_key(dev_class_list_key(region))
        except NotFoundError:
            raise ipaas_exceptions.MissingRequiredData(
                "Unable to retrieve cached device classes. "
                "Most likely the app which generates this "
                "info hasn't been run.",
                "cache_CIs_and_DevClasses",
            )
        self.logger = logger
        self.dev_class_mappings = self.create_class_mappings(ci_list)
        self.dev_class_mappings_lower = self.create_class_mappings(
            ci_list, normalize=True
        )
        if mappings:
            self.mappings = mappings
        else:
            self.mappings = dict()
        if org_filter:
            self.org_filter = [int(x) for x in org_filter if x]
        else:
            self.org_filter = list()
        if cug_filter:
            self.cug_filter = [int(x) for x in cug_filter if x]
        else:
            self.cug_filter = list()

    @staticmethod
    def create_class_mappings(
        class_list: List[dict], normalize: bool = False
    ) -> Dict[str, List[ScienceLogicDevClass]]:
        class_lookup_dict = {}
        for dev_class in class_list:
            dev_class_instance = ScienceLogicDevClass(dev_class)
            name = (
                f"{dev_class_instance.dev_class} | " f"{dev_class_instance.description}"
            )
            if name in class_lookup_dict or name.lower() in class_lookup_dict:
                if normalize:
                    class_lookup_dict[name.lower()].append(dev_class_instance)
                else:
                    class_lookup_dict[name].append(dev_class_instance)
            else:
                if normalize:
                    class_lookup_dict[name.lower()] = [dev_class_instance]
                else:
                    class_lookup_dict[name] = [dev_class_instance]
        return class_lookup_dict

    def get_dev_class(self, class_description):
        return self.dev_class_mappings.get(class_description)

    def get_all_dev_classes(self):
        return self.dev_class_mappings.keys()

    def generate_class_guids(self):
        """
        Generates a list of device class GUIDs from a mappings list.

        Returns:
            generator
        """
        for device_class_list in self.mappings.values():
            for device_class in device_class_list:
                dev_class_objs = self.dev_class_mappings_lower.get(
                    device_class.lower(), list()
                )
                for dev_class_obj in dev_class_objs:
                    yield dev_class_obj.guid

    def generate_where_clause_for_db_query(self):
        """
        Generates where clause for assets search.

        Returns:
            string: MySQL WHERE clause.
        """
        class_generator = self.generate_class_guids()
        search_string = "devtype_guid IN ("
        for guid in class_generator:
            search_string += "'{}',".format(guid)
        search_string = search_string.rstrip(",")
        search_string += ")"

        if self.org_filter:
            search_string += " AND leg_dev.roa_id IN ("
            for org in self.org_filter:
                search_string += "'{}',".format(org)
            search_string = search_string.rstrip(",")
            search_string += ")"

        if self.cug_filter:
            search_string += " AND leg_dev.cug_id IN ("
            for cug in self.cug_filter:
                search_string += "'{}',".format(cug)
            search_string = search_string.rstrip(",")
            search_string += ")"

        return search_string

    def generate_gql_search_filter(
        self, chunk_size: int = None, drop_inactive: bool = False
    ):
        """
        Generates GQL Search Filter for Device Sync.

        Returns:
            dict: GQL Search Filter
        """
        device_filter = {"search": {"and": list()}}
        dev_classes_in_filter = []
        for class_id in self.generate_class_guids():
            if class_id not in dev_classes_in_filter:
                dev_classes_in_filter.append(class_id)

        if dev_classes_in_filter:
            device_filter["search"]["and"].append(
                {"deviceClass": {"has": {"id": {"in": dev_classes_in_filter}}}}
            )
        else:
            raise ipaas_exceptions.StepFailedException(
                "No Device Classes pulled from Mappings"
            )
        if self.org_filter:
            device_filter["search"]["and"].append(
                {"organization": {"has": {"id": {"in": self.org_filter}}}}
            )
        if self.cug_filter:
            device_filter["search"]["and"].append(
                {"collectorGroup": {"has": {"id": {"in": self.cug_filter}}}}
            )
        if drop_inactive:
            device_filter["search"]["and"].append({"isActive": {"isTrue": True}})
        if chunk_size:
            device_filter["first"] = int(chunk_size)
        else:
            device_filter["first"] = 250

        return device_filter


class ScienceLogicDevClass(object):
    def __init__(self, dev_class_dict):
        self.virtual_type = dev_class_dict.get("virtual_type")
        self.description = dev_class_dict.get("description")
        self.id = dev_class_dict.get("id")
        self.dev_class = dev_class_dict.get("class")
        self.guid = dev_class_dict.get("guid")


@singleton
class ServiceNowCIList(object):
    """
    Singleton class which contains the list of all ServiceNowCi Classes
    Should only query cache once, regardless of how many times its instantiated
    """

    def __init__(self, snow_id=SERVICENOW_DEFAULT_ID, cmanager=None, force_new=False):
        """
        Initialize ServiceNowCIList object.
        Args:
            snow_id (str): Unique Identifier for ServiceNow Instance
            cmanager (IpaasContentManager): Content Manager Passthrough
            force_new: un-used.
        """
        if not cmanager:
            cmanager = IpaasContentManager()
        try:
            ci_list = cmanager.load_from_cache_by_key(ci_list_cache_key(snow_id))
        except NotFoundError:
            raise ipaas_exceptions.MissingRequiredData(
                "Unable to retrieve cached CIs. Most likely the app which generates this info hasn't been run.",
                "cache_CIs_and_DevClasses",
            )

        (self.parent_mappings, self.child_mappings) = self.create_ci_mappings(ci_list)

    @staticmethod
    def create_ci_mappings(ci_list: list) -> Tuple[dict, dict]:
        """
        Create CI mappings.

        Args:
            ci_list: List of CI Relation Dictionaries.

        Returns: Parent and Child dictionaries.

        """
        # First start by creating separating independent and dependent
        # CIs (root parents and children)
        parent_name_to_obj = {}
        child_name_to_obj = {}
        rule_types = {
            "containment_rule": "Containment",
            "hosting_rule": "Hosting",
            "reference_rule": "Reference",
        }
        for ci in ci_list:
            rules = dict()
            for key, rule_type in rule_types.items():
                rules[rule_type] = ci.pop(key)

            for r_type, rule_list in rules.items():
                for rule in rule_list:
                    ci_child = ServiceNowCIChild(ci, r_type, rule, parent_name_to_obj)
                    existing_children_for_table = child_name_to_obj.get(
                        ci_child.ci_class, {}
                    )
                    existing_children_for_table.update(
                        {ci_child.parent.ci_class: ci_child}
                    )
                    child_name_to_obj[ci_child.ci_class] = existing_children_for_table

        return parent_name_to_obj, child_name_to_obj

    def get_child_ci(self, table_name, parent_table):
        """
        Get Parent/Child mapping.
        Args:
            table_name (str): Child CI Type.
            parent_table (str): Parent CI Type.

        Returns: ServiceNowCiChild object.

        """
        cis_for_table = self.get_all_cis_for_table(table_name)
        if cis_for_table:
            parent_lookup = cis_for_table.get(parent_table)
            # Although the table name was found in the child list, the
            # parent may not exist for the expected relationship. If that's
            # the case, we need to attempt reversing
            if parent_lookup:
                return parent_lookup

        # Try reverse
        cis_for_table = self.get_all_cis_for_table(parent_table)
        return cis_for_table.get(table_name)

    def get_all_cis_for_table(self, table_name):
        """
        Return ServiceNowChildCi object for given CI Type
        Args:
            table_name (str): CI Type to lookup.

        Returns:

        """
        return self.child_mappings.get(table_name)

    def get_parent_ci(self, table_name):
        return self.parent_mappings.get(table_name)

    def get_parents_of_parent_by_obj(self, parent_obj):
        return self.child_mappings.get(parent_obj.ci_class)

    def get_parents_of_parent_by_table(self, table_name):
        return self.child_mappings.get(table_name)

    def get_all_ci_tables(self):
        return list(set(self.child_mappings.keys()) | set(self.parent_mappings.keys()))


class ServiceNowCIChild(object):
    def __init__(self, ci, r_type, rule, parent_name_to_obj):
        """
        Create ServiceNowCIChild
        Args:
            ci (dict): Cached CI Dictionary.
            r_type (str): Relation Class. (Hosting, Containment, Reference)
            rule (dict): Relation Rule.
            parent_name_to_obj (dict): Existing parent_name_to_obj dict.
        """
        self.relation_type = rule.get("rel_type")
        self.ci_class = ci.get("class_table")
        self.type = r_type
        self.parent_table = rule.get("parent")
        self.is_reverse = str_to_bool(rule.get("is_reverse"))

        parent = parent_name_to_obj.get(self.parent_table)
        if not parent:
            parent = ServiceNowCIParent(ci, rule)
            parent_name_to_obj[parent.ci_class] = parent
        parent.update_children_lookup(self)
        self.parent = parent


class ServiceNowCIParent(object):
    def __init__(self, ci, rule):
        """
        Create ServiceNowCiParent Object
        Args:
            ci (dict): Cached CI Dictionary.
            rule (dict): Relation Rule.
        """
        self.criterion_attributes = ci.get("criterion_attributes")
        self.attributes = ci.get("attributes")
        # used prior to INT-1379 Changes.
        # self.parent_class_name = ci.get("u_parent_type.u_parent_class")
        self.ci_class = rule.get("parent")
        self.independent = str_to_bool(ci.get("independent"))
        self.children_lookup = {}

    def update_children_lookup(self, child_obj):
        self.children_lookup[child_obj.ci_class] = child_obj


def ci_list_cache_key(snow_id):
    return SNOW_CI_CACHE_KEY_PREFIX + "{}".format(snow_id)


def dev_class_list_key(region):
    return SL1_DEV_CLASS_CACHE_KEY_PREFIX + "{}".format(region)


class Device(CMDBObject):
    """Base Device class to provide common functions."""

    def is_usable_attribute(self, *args):
        raise NotImplementedError

    def __init__(
        self,
        sl1_id: str,
        region: str,
        snow_ci_class: str,
        company_sys_id: str = None,
        sys_id: str = None,
        domain_sys_id: str = None,
    ):
        super(Device, self).__init__(sl1_id, region, sys_id=sys_id)
        self.set_domain_sys_id(domain_sys_id)
        self.snow_ci_class = snow_ci_class
        self.company_sys_id = company_sys_id
        self.correlation: Optional[DeviceCorrelation] = None

    def eval_template(self, template: str, logger=None) -> (str, None):
        """
        Evaluate Attribute Template.

        Args:
            template: Template to evaluate.
            logger: IpaasLogger from step.

        Returns:

        """
        try:
            value = super(Device, self).eval_template(template=template)
        except TemplateError as err:
            if logger:
                if isinstance(self, SL1Device):
                    type_msg = f"SL1 DID: {self.sl1_id}"
                else:
                    type_msg = f"ServiceNow CI sys_id: {self.snow_sys_id}"
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

    def clear_correlating_data(self):
        """
        Clear all SNOW correlation data related to this object. This is used
        when syncing, and we've identified that a SL1 device no longer
        exists on the ServiceNow system (but it exists in our cache). Clearing
        the object allows us to indicate that the related service_now ci
        no longer exists
        """
        self.snow_sys_id = None
        self.snow_ci_class = None
        self.company_sys_id = None
        self.domain_sys_id = None
        self.correlation.clear_correlation_data()

    def save_current_sys_id_mapping(self):
        self.correlation.save_sys_id_mapping(
            self.snow_sys_id,
            company=self.company_sys_id,
            snow_ci=self.snow_ci_class,
            domain=self.domain_sys_id,
        )

    def delete_sys_id_mapping(self):
        self.correlation.delete_sys_id_mapping()

    def set_correlation(self, cmanager: IpaasContentManager = None):
        self.correlation = DeviceCorrelation(
            self.region, self.sl1_id, cmanager=cmanager
        )

    def clear_correlation(self):
        self.correlation = None


class ServiceNowDevice(Device):
    def __init__(self, snow_dict: dict, cmanager: IpaasContentManager = None):
        """
        Initialize ScopedServiceNowDevice.

        Args:
            snow_dict (dict): Entire CI Dictionary from ServiceNow.
        """
        super(ServiceNowDevice, self).__init__(
            sl1_id=snow_dict.pop("x_sclo_scilogic_id", None),
            region=snow_dict.pop("x_sclo_scilogic_region", None),
            snow_ci_class=snow_dict.pop("sys_class_name", None),
            sys_id=snow_dict.get("sys_id", None),
            company_sys_id=snow_dict.pop("company", None),
            domain_sys_id=snow_dict.pop("sys_domain", None),
        )
        self.set_correlation(cmanager=cmanager)

        self.dict_to_properties(snow_dict)

    def generate_attribute_update_queries(
        self, attr_mappings: Dict[str, List[str]], asset_id: str, logger=None
    ) -> Tuple[Optional[str], dict]:
        """
        Generate SL1 Queries to Update Asset and Attribute records.

        Args:
            attr_mappings (dict): Dictionary of mappings from SL1 to SNOW
            values.
            asset_id (str): ID of asset record to update.
            logger: logger from step run.

        Returns:
            SL1 DB Query and Dictionary of custom attributes.

        """
        field_lookup = {
            "arraySize": "asst_config.array_size",
            "assetTag": "leg_asset.asset_tag",
            "cpuCount": "asst_config.cpu",
            "cpuMake": "asst_config.cpu_make",
            "cpuSpeed": "asst_config.speed",
            "depreciationMethod": "asst_svc.dep_method",
            "depreciationSchedule": "asst_svc.dep_schedule",
            "diskCount": "asst_config.dsk_count",
            "diskSize": "asst_config.dsk_size",
            "dnsDomain": "asst_config.dns_domain",
            "dnsName": "asst_config.dns_name",
            "firmwareVersion": "asst_config.fw_ver",
            "floor": "asst_loc.floor",
            "function": "leg_asset.function",
            "hostId": "asst_config.hostid",
            "hostname": "asst_config.hostname",
            "location": "asst_loc.location",
            "make": "leg_asset.make",
            "memory": "asst_config.memory",
            "model": "leg_asset.model",
            "operatingSystem": "asst_config.os",
            "owner": "leg_asset.owner",
            "panel": "asst_loc.panel",
            "plate": "asst_loc.plate",
            "punch": "asst_loc.punch",
            "purchaseCheck": "asst_svc.p_check",
            "purchaseCost": "asst_svc.p_cost",
            "purchaseDate": "asst_svc.p_date",
            "purchaseOrderNumber": "asst_svc.p_po_num",
            "rack": "asst_loc.rack",
            "rfid": "leg_asset.rfid",
            "room": "asst_loc.room",
            "serial": "leg_asset.serial",
            "serviceCheck": "asst_svc.s_check",
            "serviceCost": "asst_svc.s_cost",
            "serviceDate": "asst_svc.s_date",
            "serviceDescription": "asst_svc.s_descr",
            "serviceExpirationDate": "asst_svc.s_date_ex",
            "serviceOrderNumber": "asst_svc.s_po_num",
            "servicePolicyNumber": "asst_svc.s_num",
            "shelf": "asst_loc.shelf",
            "status": "leg_asset.status",
            "warrantyCheck": "asst_svc.w_check",
            "warrantyCost": "asst_svc.w_cost",
            "warrantyDate": "asst_svc.w_date",
            "warrantyDescription": "asst_svc.w_descr",
            "warrantyExpirationDate": "asst_svc.w_date_ex",
            "warrantyOrderNumber": "asst_svc.w_po_num",
            "warrantyPolicyNumber": "asst_svc.w_num",
            "zone": "asst_loc.zone",
        }

        base_query = (
            r"UPDATE master_biz.legend_asset leg_asset "
            r"JOIN master_biz.asset_service asst_svc "
            r"ON leg_asset.id = asst_svc.iid "
            r"JOIN master_biz.asset_configuration asst_config "
            r"ON leg_asset.id = asst_config.iid "
            r"JOIN master_biz.asset_location asst_loc "
            r"ON leg_asset.id = asst_loc.iid "
            r"SET %s "
            r"WHERE leg_asset.id = %s"
        )
        custom_attributes = dict()
        updates = []
        for sl1_field, snow_attrs in attr_mappings.items():
            for snow_attr in snow_attrs:
                if not self.is_usable_attribute(snow_attr, sl1_field):
                    continue
                if "{{" in snow_attr:  # Template handling
                    snow_value = self.eval_template(snow_attr, logger)
                    if not snow_value:
                        continue
                else:
                    snow_value = getattr(self, snow_attr)

                if field_lookup.get(sl1_field):
                    updates.append(f'{field_lookup[sl1_field]} = "{snow_value}"')
                else:
                    custom_attributes[f"c-{sl1_field}"] = snow_value
        if updates:
            return base_query % (", ".join(updates), asset_id), custom_attributes
        else:
            return None, custom_attributes

    def is_usable_attribute(self, snow_field: str, sl1_field: str) -> bool:
        if "{{" in snow_field:
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


class SL1Device(Device):
    def __init__(
        self,
        sl1_hostname: str,
        region: str,
        gql_payload: dict,
        snow_ci_class: str,
        org: Optional[SL1Org] = None,
        parent_device: Optional[SL1Device] = None,
        component_unique_id: Optional[str] = None,
        cmanager: IpaasContentManager = None,
        prepopulated_lookups: dict = None,
        domain_sys_id: str = None,
        manufacturer_sys_id: str = None,
        model_sys_id: str = None,
        url_override: str = None,
        additional_data: dict = None,
    ):
        """
        Convert an em7 response dictionary into the expected ServiceNow Device
        Class.

        Args:
            sl1_hostname: Hostname of target SL1 system.
            region:
            gql_payload: SL1 Device data.
            snow_ci_class: ServiceNow CI type.
            org: SL1Org object
            parent_device: SL1 Device Ancestry Tree data.
            component_unique_id: Component unique identifier from
                master_dev.component_dev_map table.
            cmanager: Content Manager Pass-through.
            prepopulated_lookups: Dictionary of mem-cached lookups.
            domain_sys_id: Sys_ID of Domain if Domain Separated.
            manufacturer_sys_id: sys_id of manufacturer.
            model_sys_id: sys_id of model.
            url_override: Url used to override the em7_hostname value in
                the device url.
        """
        did = gql_payload.pop("id")
        correlation = DeviceCorrelation(
            region, did, cmanager, prepopulated_lookups=prepopulated_lookups
        )
        if correlation:
            sys_id = correlation.get_correlating_dev_snow_id()
        else:
            sys_id = None

        super(SL1Device, self).__init__(
            sl1_id=did,
            region=region,
            snow_ci_class=snow_ci_class,
            sys_id=sys_id,
            domain_sys_id=domain_sys_id,
        )
        self.org = org
        self.asset_id = None
        self.asset_components = None
        self.asset_licenses = None
        self.asset_networks = None
        self.__process_asset_block(gql_payload.pop("asset", dict()))

        self.device_class = None
        self.device_category = None
        self.__process_device_class(gql_payload.pop("deviceClass", dict()))

        if org:
            self.org_id = org.sl1_id
            self.org_name = org.name
            self.company_sys_id = org.snow_sys_id
        else:
            self.org_id = None
            self.org_name = None

        self.__process_custom_attrs(gql_payload.pop("alignedAttributes", list()))

        self.dict_to_properties(gql_payload)

        if isinstance(additional_data, dict):
            self.dict_to_properties(additional_data)

        self.parent_device = parent_device
        self.component_unique_id = component_unique_id
        self.manufacturer_sys_id = manufacturer_sys_id
        self.model_sys_id = model_sys_id

        self.sl1_url = self.generate_em7_device_url(sl1_hostname, url_override)
        self.snow_payload = None
        self.merged = False

    def __process_device_class(self, device_class_details: dict):
        if device_class_details:
            self.device_class = f"{device_class_details['class']} | {device_class_details['description']}"

        device_category_details = device_class_details.get("deviceCategory", {})
        self.device_category = device_category_details.get("name")

    def __process_custom_attrs(self, custom_attrs: list):
        if type(custom_attrs) is not list:
            return

        # merge the asset details from gql with the asset details from db
        for custom_attr in custom_attrs:
            # custom attrs can either have value or text with the val
            val = custom_attr.get("value")
            if not val:
                val = custom_attr.get("text")
            setattr(self, custom_attr.get("id"), val)

    def __process_asset_block(self, asset: dict):
        if type(asset) is not dict:
            return
        else:
            self.asset_licenses = asset.pop("licenses", dict()).get("edges", list())
            self.asset_networks = asset.pop("networks", dict()).get("edges", list())
            self.asset_components = asset.pop("components", dict()).get("edges", list())
            self.asset_id = asset.pop("id", None)
            asset.update(asset.pop("configuration", dict()))
            asset.update(asset.pop("maintenance", dict()))

            self.dict_to_properties(asset)

    def generate_em7_device_url(
        self, sl1_hostname: str, url_override: str = None
    ) -> str:
        """
        Create the SL1 url for accessing the device.

        Args:
            sl1_hostname: SL1 Host Name
            url_override: Base URL override

        Returns: device url

        """
        if url_override:
            if url_override.strip():
                return "https://{}/em7/index.em7?exec=device_summary&did={}".format(
                    url_override.strip(), self.sl1_id
                )
            else:
                return "https://{}/em7/index.em7?exec=device_summary&did={}".format(
                    sl1_hostname, self.sl1_id
                )
        else:
            return "https://{}/em7/index.em7?exec=device_summary&did={}".format(
                sl1_hostname, self.sl1_id
            )

    def info_to_post(
        self,
        attrib_mappings: dict,
        logger=None,
        drop_sys_id: bool = False,
        relation_overrides: dict = None,
        domain_sep_enabled: bool = False,
        drop_company: bool = False,
        start_time: str = None,
        source_name: str = "Other Automated",
    ) -> dict:
        """
        Return dictionary with all properties ready to post to ServiceNow.
        """
        should_drop_company = False if domain_sep_enabled else drop_company
        if self.snow_payload:
            return deepcopy(self.snow_payload)

        if self.parent_device:
            info = self.parent_device.info_to_post(
                attrib_mappings,
                logger,
                drop_sys_id=drop_sys_id,
                relation_overrides=relation_overrides,
                domain_sep_enabled=domain_sep_enabled,
                drop_company=drop_company,
                start_time=start_time,
                source_name=source_name,
            )
            if self.snow_ci_class == "cmdb_ci_esx_resource_pool":
                if self.parent_device.snow_ci_class == "cmdb_ci_vcenter_cluster":
                    self.snow_payload = info
                    return info
                if isinstance(self.parent_device.parent_device, SL1Device):
                    if (
                        self.parent_device.snow_ci_class == "cmdb_ci_esx_resource_pool"
                        and self.parent_device.parent_device.snow_ci_class
                        == "cmdb_ci_vcenter_cluster"
                    ):
                        self.snow_payload = info
                        return info
        else:
            info = {"items": [], "relations": []}
        data = dict()
        data["className"] = self.snow_ci_class
        data["values"] = {
            "x_sclo_scilogic_monitored": True,
            "x_sclo_scilogic_id": self.sl1_id,
            "x_sclo_scilogic_region": self.region,
            "x_sclo_scilogic_url": self.sl1_url,
        }
        if self.snow_sys_id and not drop_sys_id:
            data["values"]["sys_id"] = self.snow_sys_id
        if self.component_unique_id:
            data["values"]["object_id"] = self.component_unique_id
        if self.company_sys_id and not should_drop_company:
            data["values"]["company"] = self.company_sys_id
        if self.domain_sys_id and domain_sep_enabled:
            data["values"]["sys_domain"] = self.domain_sys_id
        data["values"].update(self.process_attributes(attrib_mappings, logger))
        data["sys_object_source_info"] = {
            "source_feed": self.region,
            "source_name": source_name,
            "source_native_key": self.sl1_id,
            "source_recency_timestamp": start_time,
        }
        info["items"].append(data)
        if self.parent_device:
            info.update(self.process_relation_info(info, relation_overrides))

        self.snow_payload = info
        return info

    def process_attributes(self, attr_mappings: dict, logger=None) -> dict:
        payload = dict()
        for sl1_field, snow_fields in attr_mappings.items():
            if not self.is_usable_attribute(sl1_field):
                continue
            if "{{" in sl1_field:  # Template handling
                sl1_value = self.eval_template(sl1_field, logger)
                if not sl1_value:
                    continue
            else:
                sl1_value = getattr(self, sl1_field)
            for snow_field in snow_fields:
                try:
                    payload[snow_field] = sl1_transform_to_snow(sl1_field, sl1_value)
                except (ValueError, TypeError):
                    logger.warning(
                        f"DID {self.sl1_id} - {sl1_field} looks like a date "
                        f"but has an invalid value: {sl1_value}. Dropping"
                    )
                    continue

        return payload

    def is_usable_attribute(self, sl1_field: str) -> bool:
        if "{{" in sl1_field:
            return True
        elif not getattr(self, sl1_field, None):
            return False
        elif not getattr(self, sl1_field):
            return False
        else:
            return True

    def process_relation_info(
        self, parent_info: dict, relation_overrides: dict = None
    ) -> dict:
        """
        Appends relation info to info_to_post() and processes overrides.
        Args:
            parent_info: output from info_to_post()
            relation_overrides: dictionary of relationship overrides

        Returns: Updated info_to_post()

        """
        if self.merged:
            # Hard Code relation for merged devices.
            parent_pos = [
                pos
                for pos, x in enumerate(parent_info["items"])
                if x["values"]["x_sclo_scilogic_id"] == self.parent_device.sl1_id
            ]
            rel_type = "Connects to::Connected by"
            parent = parent_pos[0]
            child = len(parent_info["items"]) - 1

            rel_dict = {"parent": parent, "child": child, "type": rel_type}
            parent_info["relations"].append(rel_dict)

        elif self.snow_ci_class in relation_overrides:
            override = relation_overrides.get(self.snow_ci_class)
            override_info = dict()
            if "values" in override:
                for snow_key, dev_property in override["values"].items():
                    override_info[snow_key] = getattr(self, dev_property, "")
            parent_info["items"][-1]["values"].update(override_info)
            for relation in override.get("relations"):
                parent_pos = [
                    pos
                    for pos, x in enumerate(parent_info["items"])
                    if x["className"] == relation["parent"]
                ]
                if not parent_pos:
                    continue
                rel_type = relation["rel_type"]
                if relation["reverse"]:
                    parent = len(parent_info["items"]) - 1
                    child = parent_pos[0]
                else:
                    parent = parent_pos[0]
                    child = len(parent_info["items"]) - 1
                rel_dict = {"parent": parent, "child": child, "type": rel_type}
                parent_info["relations"].append(rel_dict)

        else:
            cis = ServiceNowCIList()
            parent_pos = [
                pos
                for pos, x in enumerate(parent_info["items"])
                if x["values"]["x_sclo_scilogic_id"] == self.parent_device.sl1_id
            ]
            try:
                parent_ci_obj = cis.get_child_ci(
                    self.snow_ci_class, self.parent_device.snow_ci_class
                )
            except AttributeError:
                raise MissingRelationsException(
                    self.parent_device.sl1_id,
                    self.parent_device.snow_ci_class,
                    self.sl1_id,
                    self.snow_ci_class,
                ) from None
            else:
                if parent_ci_obj:
                    rel_type = parent_ci_obj.relation_type
                    if parent_ci_obj.is_reverse:
                        parent = len(parent_info["items"]) - 1
                        child = parent_pos[0]
                    else:
                        parent = parent_pos[0]
                        child = len(parent_info["items"]) - 1

                    rel_dict = {"parent": parent, "child": child, "type": rel_type}
                    parent_info["relations"].append(rel_dict)

                else:
                    raise MissingRelationsException(
                        self.parent_device.sl1_id,
                        self.parent_device.snow_ci_class,
                        self.sl1_id,
                        self.snow_ci_class,
                    )
        return parent_info


def none_check(item, use_if_none):
    """
    When reading from SL1/ServiceNow, it's possible they return null for
    certain attributes. Use this check to change None into some other
    value
    Args:
        item: the item to do a none check on
        use_if_none: what will be returned if it is none

    Returns:
        object
    """
    if item is None:
        return use_if_none

    return item


def find_sys_id_in_snow_response(device):
    """
    Look at a device entry and extracts the sys_id from the correct place.

    For new devices, the id should be pulled from the target id that will be
    created on import. For existing devices, the id should just be the sys_id
    value.
    """
    target_info = device.get("sys_target_sys_id")
    if not target_info:
        return device.get("sys_id")

    return target_info.get("value")


def convert_list_to_did_lookup(data_list):
    """
    Converts a list of data returned by the db into a dict with the did
    as the lookup key
    Args:
        data_list:

    Returns:

    """
    lookup = dict()
    for item in data_list:
        did = str(item.get("did", ""))
        lookup[did] = item
    return lookup


def dev_sysid_lookup_dict(sl1_data: list, region: str, chunk_size: int = 1000) -> dict:
    """
    Using the em7 collected data, create a list of all DIDs found. And
    do a bulk lookup for all DIDs in the DB at once
    Args:
        sl1_data (list): list of all devices dicts returned from SL1.
        region (str): SL1 Region.
        chunk_size: Batch size for Couchbase Lookup
    Returns:
        dict: did to sys_id mappings

    """
    did_list = []
    for device_dict in sl1_data:
        did_list.append(device_dict["id"])
    return prepopulate_dev_lookups(region, did_list, chunk_size=chunk_size)


def extract_make_model_from_device_asset(asset: dict):
    """
    Safe way of extracting key data from a device asset. Performs
    checks to make sure the asset data is actually populated
    before returning the value from make and model
    :param asset: device asset data
    :return Tuple: (make, model)
    """
    if not asset:
        return None, None
    make = asset.get("make")
    model = asset.get("model")
    return make, model


def get_info_with_reload(
    device: SL1Device,
    attrib_mappings: dict,
    logger=None,
    drop_sys_id: bool = False,
    relation_overrides: dict = None,
    domain_sep_enabled: bool = False,
    drop_company: bool = False,
    start_time: str = None,
    source_name: str = None,
) -> dict:
    """
    Workaround function which will attempt to reload the ServiceNowCIList
    in the event the relationship wasn't located the first time.

    Workaround for INT-1353. For some reason the ServiceNowCIList singleton
    isn't consistently creating the ci lists.
    The workaround is to reload the singleton instance from the db

    Args:
        device: device to process
        attrib_mappings: Attribute mappings
        logger: Ipaaslogger
        drop_sys_id (bool): Drop Sys_id in payload
        relation_overrides: Relationship overrides dict
        domain_sep_enabled: Is domain sep enabled
        drop_company: drop company from payload
        start_time: Step start time
        source_name: snow discovery source
    Returns:
        dict
    """
    try:
        return device.info_to_post(
            attrib_mappings,
            logger,
            drop_sys_id=drop_sys_id,
            relation_overrides=relation_overrides,
            domain_sep_enabled=domain_sep_enabled,
            drop_company=drop_company,
            start_time=start_time,
            source_name=source_name,
        )
    except ipaas_exceptions.StepFailedException:
        logger.warning(
            "Unable to lookup a mapping. "
            "Attempting to reload mapping list, "
            "and trying again"
        )
        ServiceNowCIList(force_new=True)
        return device.info_to_post(
            attrib_mappings,
            logger,
            drop_sys_id=drop_sys_id,
            relation_overrides=relation_overrides,
            domain_sep_enabled=domain_sep_enabled,
            drop_company=drop_company,
            start_time=start_time,
            source_name=source_name,
        )


def invert_mappings(mappings: dict) -> dict:
    """
    Invert Class Mappings for faster lookups.

    Args:
        mappings (dict): Class Mappings

    Returns:
        dict
    """
    inverted_mappings = dict()
    for ci_type, sl1_classes in mappings.items():
        for sl1_class in sl1_classes:
            inverted_mappings[sl1_class.lower()] = ci_type

    return inverted_mappings


def group_correlations(device_list: List[ServiceNowDevice]) -> dict:
    """
    Batch save all correlations in the list. Each correlation to be saved will
    be batched into groups and saved in CB
    Args:
        device_list (list): list of ServiceNowDevice objects with correlation
    Returns:
        None
    """
    save_key_to_data = {}
    for device in device_list:
        save_key_to_data[
            device.correlation.device_lookup_key
        ] = device.correlation.correlation_data_to_save(
            device.snow_sys_id,
            device.company_sys_id,
            device.snow_ci_class,
            device.domain_sys_id,
            {},
        )
        device.clear_correlation()
    return save_key_to_data


def update_correlations(device_list: List[SL1Device]) -> Dict[str, dict]:
    """
    Receive a list of SL1Devices and generate a set of cache updates while preserving the original set.

    Args:
        device_list: list of SL1Devices

    Returns: dict of cache updates.

    """
    save_key_to_data = dict()
    for device in device_list:
        save_key_to_data[
            device.correlation.device_lookup_key
        ] = device.correlation.get_current_data()
    return save_key_to_data


def generate_devices_gql_query(
    enable_networks: bool = False,
    enable_active: bool = False,
    enable_components: bool = False,
    enable_licenses: bool = False,
    enable_vendors: bool = False,
) -> str:
    fragments = [
        "fragment deviceCategory on DeviceCategory{id name}",
        "fragment deviceClass on DeviceClass{"
        " id class description deviceCategory{...deviceCategory}}",
        "fragment assetConfig on AssetConfiguration{operatingSystem hostId"
        " hostname dnsName dnsDomain memory cpuCount cpuMake cpuSpeed"
        " firmwareVersion arraySize diskCount diskSize}",
        "fragment org on Organization{id}",
    ]
    device_fragment = (
        "fragment device on Device{id name ip hostname dateAdded asset{...asset}"
        " alignedAttributes{... on CustomIntAttribute{id value}"
        " ... on CustomStringAttribute{id text: value}} deviceClass{...deviceClass}"
        " organization{...org}"
    )
    if enable_active:
        fragments.append(
            "fragment active on DeviceActive{userDisabled unavailable "
            "maintenance systemDisabled userInitiatedMaintenance}"
        )
        device_fragment += " active{...active}}"
    else:
        device_fragment += "}"

    asset_maint_fragment = (
        "fragment assetMaint on AssetMaintenance{purchaseDate"
        " purchaseCost purchaseOrderNumber purchaseCheck depreciationMethod"
        " depreciationSchedule servicePolicyNumber serviceDescription serviceDate"
        " serviceOrderNumber serviceCost serviceExpirationDate serviceCheck"
        " warrantyPolicyNumber warrantyDate warrantyExpirationDate"
        " warrantyDescription warrantyCost warrantyOrderNumber"
        " warrantyCheck vitalServiceInformation"
    )
    if enable_vendors:
        fragments.append("fragment vendor on Vendor{id company}")
        asset_maint_fragment += (
            " purchaseVendor{...vendor}"
            " serviceVendor{...vendor} warrantyVendor{...vendor}}"
        )
        fragments.append(asset_maint_fragment)
    else:
        asset_maint_fragment += "}"
        fragments.append(asset_maint_fragment)
    assets_fragment = (
        "fragment asset on Asset{id serial make model location assetTag function status owner zone"
        " floor room rack shelf plate panel punch rfid vitalAssetInformation"
        " configuration{...assetConfig}"
        " maintenance{...assetMaint}"
    )
    if enable_components:  # Toggle to enable components
        fragments.append(
            "fragment assetComponent on AssetComponent{id make model serial type connect slot memo}"
        )
        assets_fragment += " components{edges{component: node{...assetComponent}}}"

    if enable_networks:
        fragments.append(
            "fragment assetNetworks on AssetNetwork{id identification ip speed "
            "dnsIp mask mac gateway bladePort}"
        )
        assets_fragment += " networks{edges{network: node{...assetNetworks}}}"

    if enable_licenses:
        fragments.append(
            "fragment assetLicense on AssetLicense{id vendor{ ...vendor} product "
            "version serial license register notes}"
        )
        assets_fragment += " licenses{edges{license: node{...assetLicense}}}"

    assets_fragment += "}"

    fragments.append(assets_fragment)
    fragments.append(device_fragment)

    gql_query = (
        " query DeviceFetch($search: DeviceSearch, $order: [ConnectionOrder], $first: Int)"
        '{devices(first: $first, search: $search, after: "", order: $order)'
        "{pageInfo{hasNextPage matchCount} edges{"
        "cursor device: node{...device}}}}"
    )
    return " ".join(fragments) + gql_query


def chunk_db_queries(db_queries: list) -> List[List[str]]:
    """
    Chunk DB Queries into groups of 500.
    Args:
        db_queries (list): List of all DB Queries.

    Returns: List of Lists of 500 Queries

    """
    loop_list = []
    chunked_queries = []
    count = 0

    for query in db_queries:
        if count + 1 <= 500:
            loop_list.append(query)
        else:
            chunked_queries.append(loop_list)
            loop_list = []
            count = 0
            loop_list.append(query)
        count += 1
    if loop_list:
        chunked_queries.append(loop_list)
    return chunked_queries


def generate_item_payload_from_correlation(
    item: DeviceCorrelation, item_id: str, item_type: str
) -> dict:
    """
    Generate SNOW Payloads

    Args:
        item (DeviceCorrelation): Item to process
        item_id (str): Item SL1 ID
        item_type (str): Device or Interface

    Returns:
        dict: Formatted Item payload.

    """
    if item_type == "device":
        payload = {
            "className": item.get_correlating_dev_snow_ci(),
            "values": {
                "sys_id": item.get_correlating_dev_snow_id(),
                "sys_domain": item.get_correlating_dev_domain(),
                "company": item.get_correlating_dev_company(),
                "x_sclo_scilogic_id": item_id,
            },
        }
    elif item_type == "DCMR":
        if item.merged_device:
            merge_info = item.get_correlating_dev_merged_info()
            class_name = merge_info["class"]
            sys_id = merge_info["sys_id"]
            sl1_id = None
        else:
            class_name = item.get_correlating_dev_snow_ci()
            sys_id = item.get_correlating_dev_snow_id()
            sl1_id = item_id
        payload = {
            "className": class_name,
            "values": {
                "sys_id": sys_id,
                "sys_domain": item.get_correlating_dev_domain(),
                "company": item.get_correlating_dev_company(),
            },
        }
        if sl1_id:
            payload["values"]["x_sclo_scilogic_id"] = item_id
    else:
        payload = {
            "className": "cmdb_ci_network_adapter",
            "values": {
                "sys_id": item.get_correlating_dev_interface(item_id),
                "sys_domain": item.get_correlating_dev_domain(),
                "company": item.get_correlating_dev_company(),
                "x_sclo_scilogic_id": item_id,
            },
        }

    return payload
