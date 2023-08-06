from os.path import basename
from servicenow_base_syncpack.util.correlators import DeviceCorrelation


def service_now_interface_from_snow_data(snow_interface):
    """
    Transform SNOW Interface result into ServiceNowInterface object.
    Args:
        snow_interface (dict): Interface Result from SNOW.

    Returns: ServiceNowInterface object.

    """
    interface_id = snow_interface.get("u_sciencelogic_id")
    name = snow_interface.get("name")
    alias = snow_interface.get("alias")
    region = snow_interface.get("u_sciencelogic_region")
    company = snow_interface.get("company", {}).get("value")
    sys_id = snow_interface.get("sys_id")
    short_description = snow_interface.get("short_description")
    operational_status = snow_interface.get("operational_status")
    ip_address = snow_interface.get("ip_address")
    mac_address = snow_interface.get("mac_address")
    netmask = snow_interface.get("netmask")
    snow_device_id = snow_interface.get("cmdb_ci", {}).get("value")

    return ServiceNowInterface(
        region,
        short_description,
        name,
        alias,
        ip_address,
        mac_address,
        netmask,
        operational_status,
        interface_id,
        company=company,
        sys_id=sys_id,
        snow_device_id=snow_device_id,
    )


def scoped_service_now_interface_from_snow_data(
    snow_interface, cmanager=None, prepopulated_lookups=None
):
    """
    Transform SNOW Interface result into ServiceNowInterface object.
    Args:
        snow_interface (dict): Interface Result from SNOW.
        cmanager (ipaascommon.content_manger.IpaasContentManager): Content
            Manager Object.
        prepopulated_lookups (dict): Prepopulated_lookups.

    Returns: ServiceNowInterface object.

    """
    interface_id = snow_interface.get("x_sclo_scilogic_id")
    name = snow_interface.get("name")
    alias = snow_interface.get("alias")
    region = snow_interface.get("x_sclo_scilogic_region")
    company = snow_interface.get("company", u"")
    sys_id = snow_interface.get("sys_id")
    short_description = snow_interface.get("short_description")
    operational_status = snow_interface.get("operational_status")
    ip_address = snow_interface.get("ip_address")
    mac_address = snow_interface.get("mac_address")
    netmask = snow_interface.get("netmask")
    snow_device_id = snow_interface.get("cmdb_ci", "")
    domain = snow_interface.get("sys_domain", None)
    parent_device_id = snow_interface.get("parent_device_id", dict()).get("id", None)

    if parent_device_id:
        correlation = DeviceCorrelation.create_or_retrieve_correlation(
            region,
            parent_device_id,
            cmanager=cmanager,
            prepopulated_lookups=prepopulated_lookups,
            source="snow",
        )
    else:
        correlation = None

    return ScopedServiceNowInterface(
        region,
        short_description,
        name,
        alias,
        ip_address,
        mac_address,
        netmask,
        operational_status,
        interface_id,
        company=company,
        sys_id=sys_id,
        snow_device_id=snow_device_id,
        domain=domain,
        correlation=correlation,
    )


def service_now_interface_from_em7_interface_data(
    em7_interface,
    ip_info,
    unique_em7_id,
    region,
    cmanager=None,
    prepopulated_lookups=None,
    scoped=False,
):
    """
    Transforms SL1 interface result into ServiceNowInterface object.

    Args:
        em7_interface (dict): SL1 data from /api/interface.
        ip_info (dict): SL1 response from master_dev.device_ips.
        unique_em7_id (str): SL1 ident from device cache.
        region (str): Unique Ident for IS/SL1 stack.
        cmanager (ipaascommon.content_manger.IpaasContentManager): Content
        Manager Object.
        prepopulated_lookups (dict): Prepopulated_lookups.
        scoped (bool): Is scoped app.

    Returns: ServiceNowInterface object.

    """
    alias = em7_interface.get("alias", em7_interface.get("name"))
    interface_id = basename(em7_interface.get("AA__key_val__"))
    device_id = basename(em7_interface.get("device"))
    if scoped:
        correlation = DeviceCorrelation.create_or_retrieve_correlation(
            region,
            device_id,
            cmanager=cmanager,
            prepopulated_lookups=prepopulated_lookups,
            source="sl1",
        )
    else:
        correlation = DeviceCorrelation(
            unique_em7_id,
            device_id,
            cmanager=cmanager,
            prepopulated_lookups=prepopulated_lookups,
        )
    region = region
    short_description = em7_interface.get("ifDescr", "")
    name = em7_interface.get("name", "")
    mac_address = em7_interface.get("ifPhysAddress")
    operational_status = get_snow_operational_status(em7_interface.get("ifOperStatus"))
    ip_address = ip_info.get("ip", "")
    netmask = ip_info.get("netmask", "")

    if scoped:
        return ScopedServiceNowInterface(
            region,
            short_description,
            name,
            alias,
            ip_address,
            mac_address,
            netmask,
            operational_status,
            interface_id,
            correlation=correlation,
        )
    else:
        return ServiceNowInterface(
            region,
            short_description,
            name,
            alias,
            ip_address,
            mac_address,
            netmask,
            operational_status,
            interface_id,
            correlation=correlation,
        )


def interface_changed(em7_interface, snow_interface):
    if em7_interface.name != snow_interface.name:
        return True
    if em7_interface.ip_address != snow_interface.ip_address:
        return True
    if snow_interface.short_description != snow_interface.short_description:
        return True
    if snow_interface.mac_address != em7_interface.mac_address:
        return True
    if em7_interface.operational_status != snow_interface.operational_status:
        return True
    if em7_interface.alias != snow_interface.alias:
        return True
    if em7_interface.ip_netmask != snow_interface.ip_netmask:
        return True

    return False


class ServiceNowInterface(object):
    def __init__(
        self,
        region,
        short_description,
        name,
        alias,
        ip_address,
        mac_address,
        ip_netmask,
        operational_status,
        em7_interface_id,
        company="",
        sys_id=None,
        snow_device_id=None,
        correlation=None,
    ):
        """
        ServiceNow Interface Object.
        Args:
            region (str): Unique Identifier for SL1/IS instance.
            short_description (str): Interface Description.
            name (str): Interface Name.
            alias (str): Interface Alias.
            ip_address (str): Interface IP address.
            mac_address (str): Interface MAC Address.
            ip_netmask (str): Interface Netmask.
            operational_status (str): Interface Operational status.
            em7_interface_id (str): SL1 Interface ID.
            company (str): sys_id of ServiceNow company.
            sys_id (str): sys_id of interface.
            snow_device_id (str): sys_id of ServiceNow Device.
            correlation (InterfaceCorrelation): Interface Correlation Object.
        """
        self.correlation = correlation
        self.region = region
        self.short_description = short_description
        self.name = name
        self.alias = alias
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.operational_status = operational_status
        self.ip_netmask = ip_netmask
        self.em7_interface_id = em7_interface_id
        self.sys_id = sys_id

        if snow_device_id:
            self.snow_device_id = snow_device_id
        elif correlation:
            self.snow_device_id = correlation.get_correlating_dev_snow_id()
        else:
            self.snow_device_id = None
        if company:
            self.company = company
        elif correlation:
            self.company = correlation.get_correlating_dev_company()
        else:
            self.company = None

    def info_to_post(self):
        info = {
            "items": [
                {
                    "className": self.correlation.get_correlating_dev_snow_ci(),
                    "values": {"sys_id": self.snow_device_id, "company": self.company},
                }
            ],
            "relations": [{"child": 1, "parent": 0, "type": "Owns::Owned by"}],
        }

        interface_info = {
            "className": "cmdb_ci_network_adapter",
            "values": {
                "u_sciencelogic_region": self.region,
                "u_sciencelogic_id": self.em7_interface_id,
                "u_silo_monitored": True,
                "short_description": self.short_description,
                "name": self.name,
                "alias": self.alias,
                "ip_address": self.ip_address,
                "mac_address": self.mac_address,
                "netmask": self.ip_netmask,
                "operational_status": self.operational_status,
            },
        }
        if self.company:
            interface_info["values"].update({"company": self.company})
        if self.sys_id:
            interface_info["values"].update({"sys_id": self.sys_id})

        if self.snow_device_id:
            interface_info["values"].update({"cmdb_ci": self.snow_device_id})

        info["items"].append(interface_info)

        return info


class ScopedServiceNowInterface(ServiceNowInterface):
    def __init__(
        self,
        region,
        short_description,
        name,
        alias,
        ip_address,
        mac_address,
        ip_netmask,
        operational_status,
        em7_interface_id,
        company="",
        sys_id=None,
        snow_device_id=None,
        correlation=None,
        domain=None,
    ):
        """
        Scoped ServiceNow Interface Object.
        Args:
            region (str): Unique Identifier for SL1/IS instance.
            short_description (str): Interface Description.
            name (str): Interface Name.
            alias (str): Interface Alias.
            ip_address (str): Interface IP address.
            mac_address (str): Interface MAC Address.
            ip_netmask (str): Interface Netmask.
            operational_status (str): Interface Operational status.
            em7_interface_id (str): SL1 Interface ID.
            company (str): sys_id of ServiceNow company.
            sys_id (str): sys_id of interface.
            snow_device_id (str): sys_id of ServiceNow Device.
            correlation (InterfaceCorrelation): Interface Correlation Object.
            domain (str): sys_id of ServiceNow Domain
        """

        super(ScopedServiceNowInterface, self).__init__(
            region,
            short_description,
            name,
            alias,
            ip_address,
            mac_address,
            ip_netmask,
            operational_status,
            em7_interface_id,
            company=company,
            sys_id=sys_id,
            snow_device_id=snow_device_id,
            correlation=correlation,
        )

        if domain:
            self.domain = domain
        elif correlation:
            self.domain = correlation.get_correlating_dev_domain()
        else:
            self.domain = None

    def info_to_post(self):
        info = {
            "items": [
                {
                    "className": self.correlation.get_correlating_dev_snow_ci(),
                    "values": {"sys_id": self.snow_device_id, "company": self.company},
                }
            ],
            "relations": [{"child": 1, "parent": 0, "type": "Owns::Owned by"}],
        }

        interface_info = {
            "className": "cmdb_ci_network_adapter",
            "values": {
                "x_sclo_scilogic_region": self.region,
                "x_sclo_scilogic_id": self.em7_interface_id,
                "x_sclo_scilogic_monitored": True,
                "short_description": self.short_description,
                "name": self.name,
                "alias": self.alias,
                "ip_address": self.ip_address,
                "mac_address": self.mac_address,
                "netmask": self.ip_netmask,
                "operational_status": self.operational_status,
            },
        }
        if self.company:
            interface_info["values"].update({"company": self.company})
        if self.sys_id:
            interface_info["values"].update({"sys_id": self.sys_id})
        if self.snow_device_id:
            interface_info["values"].update({"cmdb_ci": self.snow_device_id})
        if self.domain:
            info["items"][0]["values"].update({"sys_domain": self.domain})
            interface_info["values"].update({"sys_domain": self.domain})

        info["items"].append(interface_info)

        return info


def get_snow_operational_status(sl1_status):
    """
    In service "1" indicates operational in CI field, a "2" indicates
    non-operational. In em7 database a 1 indicates an UP state anything else
    indicates a DOWN state.
    Args:
        sl1_status (str): SL1 Operational Status to test.

    Returns:

    """
    if str(sl1_status) == "1":
        return "1"
    else:
        return "2"
