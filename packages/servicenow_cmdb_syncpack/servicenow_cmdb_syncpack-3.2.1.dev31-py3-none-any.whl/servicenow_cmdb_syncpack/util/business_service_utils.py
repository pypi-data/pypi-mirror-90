import copy
from ipaascommon.serializer import Serializable
from ipaascommon import ipaas_exceptions


class BusinessServiceReferenceList(Serializable):
    """
    Class seeks to maintain a single representation of services as they exist
    in both SL1 and ServiceNow. If a service in SL1 and a service in Snow are
    identified as being matched (using sys_id/externalId). The data from each
    side is combined, to provide a full overview of the service from a single
    object

    Also maintains the list of services that exist in SL1, which weren't
    created by SNOW
    """

    def __init__(self, logger, overrides={}):
        self.service_mapping = {}
        self.logger = logger
        self.overrides = overrides
        self.services_in_sl1_not_from_snow = []

        """
         TODO: Support merging (Identify like services without externalId)
         If service was found in sl1 without externalId, We can
         merge that into an existing service (and merely update an externalId)
         would need to build sl1 mapping, and cross reference as snow data added
         special flag in object set to indicate merge, and change payload
         accordingly
        """

    def process_raw_data_from_snow(self, service_data):
        """
        Turns singular raw service_data as returned from SNOW into
        a business Service obj. And reconciles with the rest of the known
        services in this class
        Args:
            service_data (dict):
        Returns:
            BusinessServiceForSL1
        """
        bservice = BusinessServiceForSL1(snow_raw_data=service_data)
        return self.reconcile_bservice(bservice)

    def process_raw_data_from_sl1(self, service_data):
        """
        Turns singular raw service_data from sl1 into a business service and
        reconciles
        Args:
            service_data:
        Returns:
            BusinessServiceForSL1
        """
        bservice = BusinessServiceForSL1(sl1_raw_data=service_data)
        return self.reconcile_bservice(bservice)

    def reconcile_bservice(self, bservice):
        """
        Process recent data found about a known service (from sl1 or snow)
        combine data if this service was previously found. Updates
        master class reference mapping.
        Args:
            bservice (BusinessServiceForSL1):
        Returns:
            BusinessServiceForSL1
        """
        ref_id = copy.copy(bservice.external_id)
        existing_bservice = copy.deepcopy(self.service_mapping.get(ref_id))
        if existing_bservice:
            existing_bservice.update_raw_data(bservice)
            existing_bservice.is_root = bservice.is_root
            bservice = existing_bservice
        if bservice.external_id:
            self.service_mapping[ref_id] = bservice
        else:
            self.services_in_sl1_not_from_snow.append(bservice)
        return bservice

    def populate_regions(self, region):
        """
        Populate all known services with this region
        (used as dataSource by default)
        Args:
            region:
        Returns:

        """
        for bs in self.service_mapping.values():
            bs.region = region

    def populate_with_org_data(self, sl1_orgs):
        """
        Updates all known SL1BusinessService objects with accurate
        org ids, with ServiceNow as source of truth
        Args:
            snow_companies:
            sl1_orgs:
        Returns:
        """
        errors = []
        for bs in self.service_mapping.values():
            ### ORG data currently not sent from SNOW.
            sys_id = bs.company_sys_id
            if not sys_id:
                bs.organization = '0'
                errors.append("Snow Service with id: {}"
                              " not defined with a company. "
                              "Will Default to System".format(bs.external_id))
                continue

            for oid, org in sl1_orgs.items():
                if org.crm_id == sys_id:
                    bs.organization = oid
                    break
            if not bs.organization:
                errors.append("Snow service with id: {} "
                              "defined with company: {} "
                              "not yet synced to ServiceNow. "
                              "Will default to System"
                              .format(bs.external_id,
                                      bs.company_sys_id))
                bs.organization = '0'

        if errors:
            self.logger.warn("Identified some warnings when "
                             "resolving companies/organizations: "
                             "{}".format(errors))

    def populate_with_snow_data(self, service_data_list):
        """
        Populate reference list with snow data, and reconcile with existing data
        Args:
            service_data_list (list):
        Returns:
            None
        """
        for service_data in service_data_list:
            service_obj = self.process_raw_data_from_snow(service_data)
            for child_obj in service_obj.get_list_of_children_services_from_snow():
                self.reconcile_bservice(child_obj)

    def populate_with_sl1_data(self, service_data_list):
        """
        Populates reference list with sl1 data and reconciles with existing data
        Args:
            service_data_list (list)
        Returns:
            None
        """
        for service_data in service_data_list:
            service_obj = self.process_raw_data_from_sl1(service_data)
            # TODO When identifying merges, may have to handle children similar to snow

    def reconcile_relationships(self):
        """
        If a relationship is newly created in SNOW, but the matching services
        already exist in SL1, we must convert the SNOW relationship
        (using externalids) to their corresponding sl1 ids
        if those services already exist in sl1. Children services can only
        be added with internal SL id

        If the child does not already exist in SL1, then it must first
        be created. This method identifies and logs those as well
        Returns:
        """
        for svc in self.service_mapping.values():
            children_not_yet_created = []
            relationships_in_existing_sl1_services = []
            for id in svc.required_child_external_ids():
                bservice = self.service_mapping.get(id)
                if not bservice:
                    raise ipaas_exceptions.StepFailedException(
                        "Encountered an error. Child from servicenow is needed "
                        "to lookup, but wasn't added to the service "
                        "list previously{}".format(id))
                if bservice.exists_in_sl1():
                    relationships_in_existing_sl1_services.append(
                        bservice.sl1_id)
                else:
                    children_not_yet_created.append(bservice.external_id)
            svc.children_not_yet_created = children_not_yet_created
            svc.relationships_in_existing_sl1_services = \
                relationships_in_existing_sl1_services
            if svc.children_not_yet_created or \
                    svc.relationships_in_existing_sl1_services:
                if self.logger:
                    self.logger.info("Service with externalId {} requires these"
                                     " new services created as constituents: {}. "
                                     "Existing services identified as "
                                     "constituents: {}"
                                     .format(svc.external_id,
                                             svc.children_not_yet_created,
                                             svc.
                                             relationships_in_existing_sl1_services
                                             ))

    def get_all_payloads(self):
        """
        Generates and returns create, update, and possibly delete payloads
        with current information in list
        Returns:
            (create_payloads, update_payloads, in_sl1_not_in_this_snow)
        """
        self.reconcile_relationships()
        create_payloads = []
        update_payloads = []
        in_sl1_not_in_this_snow = []
        for bservice in self.service_mapping.values():
            if bservice.exists_in_sl1():
                if bservice.exists_in_snow():
                    # TODO: This currently just puts all payloads that aren't
                    # create to be updated. May be unnecessary updates pushed
                    # should we identify based on specific properties?
                    update_payloads.append(bservice.generate_update_payload(
                        overrides=self.overrides))
                else:
                    in_sl1_not_in_this_snow.append(bservice)

            else:
                """
                TODO: Implementing Merging 
                Can check if this bservice can be merged with one of
                those "not from snow" bservices
                """

                create_payloads.append(bservice.generate_create_payload(
                    overrides=self.overrides))
        """
        TODO: Better logging around services found in SL1 seemingly created
        from another SNOW instance. This list is in_sl1_not_in_this_snow
        """
        return create_payloads, update_payloads, in_sl1_not_in_this_snow



class BusinessServiceForSL1(object):
    """
    Representation of all provided data of a business service.
    contains raw data form sl1 and snow. properties are derived from
    that raw data.
    """
    def __init__(self, snow_raw_data={}, sl1_raw_data={}, is_root=True):
        self.snow_raw_data = snow_raw_data
        self.sl1_raw_data = sl1_raw_data
        self.relationships_in_existing_sl1_services = []
        self.children_not_yet_created = []
        self.organization = None
        self.is_root = is_root # True by default, until known not to be
        self._external_id = ''
        self.region = "ServiceNow+NoRegion"

    def set_logger(self, logger):
        # avoids serialization issues when passing data through
        self.logger = logger

    def exists_in_sl1(self):
        if self.sl1_raw_data:
            return True
        return False

    def exists_in_snow(self):
        if self.snow_raw_data:
            return True
        return False

    @property
    def sl1_id(self):
        """
        SL1 id can come from either snow or sl1. It may not always be
        unique between systems.
        (TODO: currently unique SL1 id, but would this get mixed with device_id)
        (Maybe we need a new device_id property in snow?)
        Returns:
            str
        """
        snow_sl1_id = self.snow_raw_data.get('id')
        sl1_service_def = self.sl1_raw_data.get('service')
        if sl1_service_def:
            sl1_sl1_id = sl1_service_def.get('id')
        else:
            sl1_sl1_id = None

        if sl1_sl1_id and snow_sl1_id:
            if sl1_sl1_id != snow_sl1_id:
              # TODO how to handle
               print("The sl1_id synced to ServiceNow "
                     "ci sys_id is different than the id "
                     "of the service on this system. "
                     "Mixing data between systems is "
                     "not currently supported. "
                     "snow know dev id:{} device_id: {}"
                     .format(snow_sl1_id, sl1_sl1_id))

        return sl1_sl1_id

    @property
    def snow_short_description(self):
        return self.snow_raw_data.get('short_description', '')

    @property
    def search_filter(self):
        """
        Create search filter for this service. Only create search_filters with
        device services. SNOW device connections are 1 to 1 with the service
        Returns:
        """
        service_type, policy = self.sl1_service_type_and_policy
        filter_search = {"filter": "",
                         "search": {},
                         "userSearch": "",
                         "basicSearch": [],
                         "searchJson": {}}
        if service_type == "deviceService":
            # TODO: Maybe this is more efficient to search by id instead of name?
            filter_search["search"] = {"name": {"equals": self.name}}
            filter_search["userSearch"] = "name equals \"{}\"".format(self.name)

        return filter_search

    @property
    def external_id(self):
        """
        External id can come from either sl1 or snow (sys_id) should always
        match. It is always unique, even between systems
        Returns:
        """
        if not self._external_id:
            self._external_id = self.snow_raw_data.get('sys_id')
        if not self._external_id:
            sl1_serv_def = self.sl1_raw_data.get('service')
            if sl1_serv_def:
                self._external_id = sl1_serv_def.get('externalId')
        return self._external_id

    @property
    def name(self):
        return self.snow_raw_data.get('name')

    def snow_child_devices(self):
        return self.snow_raw_data.get('child_devices', [])

    def sl1_child_devices(self):
        constituents = self.sl1_raw_data.get('service', {}).get('constituents', {}).get('edges', [])
        return constituents

    @property
    def description(self):
        attrs_with_labels_from_payload = ["used_for", "business_criticality",
                                          "sys_class_name", "install_status",
                                          "price_model", "model_id", "cost_cc",
                                          "service_classification"]
        desc_text = "{}".format(self.snow_short_description)
        for attr in attrs_with_labels_from_payload:
            attr_label = "{}_label".format(attr)
            attr_label_val = self.snow_raw_data.get(attr_label)
            attr_val = self.snow_raw_data.get(attr)
            if attr_label_val and attr_val:
                desc_text += "{}: {} ".format(
                    attr_label_val, attr_val)

        if self.domain:
            desc_text += "domain: {}".format(self.domain)
        return desc_text

    @property
    def label(self):
        return self.snow_raw_data.get("name", '')

    @property
    def company_sys_id(self):
        """
        Company sys_id as known by ServiceNow
        Returns:
        """
        return self.snow_raw_data.get("company")

    @property
    def data_source(self):
        """
        Pulled from SL1 exclusively
        Returns:
        """
        return self.sl1_raw_data.get('service', {}).get("dataSource")

    @property
    def domain(self):
        """
        Capture domain if it exists
        Returns:
        """
        return self.snow_raw_data.get("domain")

    @property
    def sl1_service_type_and_policy(self):
        """
        Only either aggregate service or device service at this point.
        can be updated. Can make each service different class with
        specific payloads generated for each
        TODO: Need to expose param for users to set/override these?
        Returns:

        """
        snow_service_classification = self.snow_raw_data.get('service_classification')
        if not snow_service_classification:
            return "deviceService", "cjfcxzgdx002e1byxzwlx04a2"
        else:
            return "aggregateService", "cka3a9m700000xdq4di0ta666"

    def update_raw_data(self, bservice):
        self.snow_raw_data.update(bservice.snow_raw_data)
        self.sl1_raw_data.update(bservice.sl1_raw_data)

    def get_list_of_children_services_from_sl1(self):
        """
        Gets list of children Business Service objects as known by sl1
        Args:
            service_reference_list:
        Returns:
            [BusinessServiceForSL1]
        """
        child_list = []
        for cd in self.sl1_child_devices():
            reconciled = BusinessServiceForSL1(sl1_raw_data=cd, is_root=False)
            child_list.append(reconciled)
        return child_list

    def get_list_of_children_services_from_snow(self):
        """
        Gets list of children business service objects as represented
        by the parent. Does not reconcile children into any master mapping
        Args:
        Returns:
            [BusinessServiceForSl1]
        """
        child_list = []
        for cd in self.snow_child_devices():
            bs = BusinessServiceForSL1(snow_raw_data=cd, is_root=False)
            child_list.append(bs)
        return child_list

    def generate_create_payload(self, tempid=True, overrides={}):
        """
        Generate payload for use if creating this service from scratch
        Args:
            tempid (bool): Whether or not to include tempId in payload
        Returns:
            dict
        """
        payload = {}
        service_type, policy = self.sl1_service_type_and_policy
        if tempid:
            payload['tempId'] = self.external_id
        payload['externalId'] = self.external_id
        payload['name'] = self.name
        payload['label'] = self.label
        payload['dataSource'] = self.region
        payload['type'] = service_type
        payload['description'] = self.description
        payload['organization'] = self.organization
        payload['contactOrganization'] = self.organization
        payload['policy'] = policy # TODO
        payload["rootCauseAnalysisMode"] = "disabled"
        payload['enabled'] = True # TODO
        payload["rootService"] = self.is_root
        payload['filterSearch'] = self.search_filter
        # for creates, externalIds always match the tempId
        tmp_list_of_constituents = copy.copy(self.children_not_yet_created)
        tmp_list_of_constituents += self.relationships_in_existing_sl1_services
        payload['constituentIds'] = tmp_list_of_constituents
        payload = self.update_payload_with_overrides(payload, overrides)
        return payload

    def update_payload_with_overrides(self, payload, override_dict):
        """
        Updates a payload properties with whatever overrides are specified by
        the user. Override values are taken using the matching keys from the
        snow business service raw_data
        Args:
            payload (dict):
            override_dict (dict): mapping of attribute overrides
        Returns:
            dict
        """
        dropped_overrides = []
        for k,v in override_dict.items():
            snow_val_for_key = self.snow_raw_data.get(k)
            if snow_val_for_key is None:
                dropped_overrides.append(
                    "Override specified property: "
                    "{} does not exist in snow data. "
                    "Removing from payload".format(v))
                continue
            payload[v[0]] = snow_val_for_key
        return payload

    def generate_update_payload(self, overrides={}):
        """
        Generates payload if this service were to be updated. Pushes
        everything known by SNOW
        Returns:
        """
        payload = {}
        payload["name"] = self.name
        if self.label:
            payload['label'] = self.label
        payload["dataSource"] = self.region
        payload["externalId"] = self.external_id
        payload["organization"] = self.organization
        payload["contactOrganization"] = self.organization
        payload['description'] = self.description
        payload['filterSearch'] = self.search_filter
        payload["constituentIds"] = self.relationships_in_existing_sl1_services
        payload = self.update_payload_with_overrides(payload, overrides)

        return payload

    def required_child_external_ids(self):
        """
        Required children ids that must be created, and referenced
        in the same payload request this service is created
        Returns:
            [BusinessServiceForSL1]
        """
        return [c.external_id for c in
                self.get_list_of_children_services_from_snow()]

    def required_child_sl1_ids(self):
        """
        List of required children by based on their SL1 ids. Note that
        this list may be incomplete if not populated after an initial round
        of creates
        Returns:
        """
        pls = [c.sl1_id for c in
                self.get_list_of_children_services_from_sl1()]
        return pls


def identify_delete_ids(bservices_in_sl1_not_in_snow, this_region):
    """
    Iterates through all bservices previously synced to SL1 by SNOW
    if the region matches this current sync, it indicates the service
    no longer exists in SNOW, and will be deleted
    Args:
        bservices_in_sl1_not_in_snow (BusinessServiceForSL1):
        this_region (str): region to match to
    Returns:
    """
    delete_payloads = []
    for bservice in bservices_in_sl1_not_in_snow:
        if bservice.data_source == this_region:
            delete_payloads.append(bservice.sl1_id)
    return delete_payloads