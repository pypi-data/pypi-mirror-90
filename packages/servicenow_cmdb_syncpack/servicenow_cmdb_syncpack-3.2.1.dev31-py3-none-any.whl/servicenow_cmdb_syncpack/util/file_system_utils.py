from servicenow_base_syncpack.util.correlators import DeviceCorrelation


def servicenow_ci_from_snow_data(snow_file_system):
    """
    Transform SNOW File System result into ServiceNowFileSystem object.
    Args:
        snow_file_system (dict): File System Result from SNOW.

    Returns: ServiceNowFileSystem object.

    """
    fs_id = snow_file_system.get('x_sclo_scilogic_id')
    name = snow_file_system.get('name')
    region = snow_file_system.get('x_sclo_scilogic_region')
    company = snow_file_system.get('company', u'')
    sys_id = snow_file_system.get('sys_id')
    short_description = snow_file_system.get('short_description')
    snow_device_id = snow_file_system.get('computer', '')
    domain = snow_file_system.get('sys_domain', None)
    media_type = snow_file_system.get('media_type', '')
    size_bytes = snow_file_system.get('size_bytes', 0)
    free_space_bytes = snow_file_system.get('free_space_bytes', 0)
    mount_point = snow_file_system.get('mount_point', '')
    label = snow_file_system.get('label', '')

    return ServiceNowFileSystem(
        region, short_description, name, fs_id, company=company,
        sys_id=sys_id, snow_device_id=snow_device_id, domain=domain,
        media_type=media_type, size_bytes=size_bytes,
        free_space_bytes=free_space_bytes, mount_point=mount_point, label=label
    )


def servicenow_ci_from_sl1_fs_data(
        sl1_file_system, region, cmanager=None, prepopulated_lookups=None):
    """
    Transforms SL1 File System result into ServiceNowFileSystem object.

    Args:
        sl1_file_system (dict): SL1 data from /api/interface.
        region (str): Unique Ident for IS/SL1 stack.
        cmanager (ipaascommon.content_manger.IpaasContentManager): Content
        Manager Object.
        prepopulated_lookups (dict): Prepopulated_lookups.

    Returns: ServiceNowFileSystem object.

    """
    media_types = {"FixedDisk": "fixed"}
    fs_id = sl1_file_system.get('fs_id')
    device_id = sl1_file_system.get("did")
    correlation = DeviceCorrelation(
        region, device_id, cmanager=cmanager,
        prepopulated_lookups=prepopulated_lookups)
    region = region
    short_description = sl1_file_system.get("description", "")
    name = sl1_file_system.get("fs_name", "")
    media_type = media_types.get(short_description)
    try:
        size_bytes = int(sl1_file_system.get('fs_size', 0)) * 1024
    except (ValueError, TypeError):
        size_bytes = 0
    try:
        used_space = int(sl1_file_system.get('fs_used', 0)) * 1024
    except (ValueError, TypeError):
        used_space = 0

    free_space_bytes = size_bytes - used_space
    if free_space_bytes < 0:
        free_space_bytes = 0

    return ServiceNowFileSystem(
        region, short_description, name, fs_id, media_type=media_type,
        size_bytes=size_bytes, free_space_bytes=free_space_bytes,
        correlation=correlation)


def file_system_changed(sl1_file_system, snow_file_system):
    """
    Checks to see if a file system has changed.
    Args:
        sl1_file_system (ServiceNowFileSystem): SL1 FS object.
        snow_file_system (ServiceNowFileSystem): ServiceNow FS object.

    Returns:

    """
    if sl1_file_system.name != snow_file_system.name:
        return True
    if sl1_file_system.mount_point != snow_file_system.mount_point:
        return True
    if snow_file_system.short_description != snow_file_system.short_description:
        return True
    if snow_file_system.label != sl1_file_system.label:
        return True
    if sl1_file_system.media_type != snow_file_system.media_type:
        return True
    if sl1_file_system.size_bytes != snow_file_system.size_bytes:
        return True
    if sl1_file_system.free_space_bytes != snow_file_system.free_space_bytes:
        return True

    return False


class ServiceNowFileSystem(object):

    def __init__(
            self, region, short_description, name, sl1_fs_id, mount_point="",
            label="", company="", media_type=None, size_bytes=0,
            free_space_bytes=0, sys_id=None, snow_device_id=None,
            correlation=None, domain=None):
        """
        ServiceNow File System Object.
        Args:
            region (str): Unique Identifier for SL1/IS instance.
            short_description (str): File System Description.
            name (str): File System Name.
            sl1_fs_id (str): SL1 File System ID.
            mount_point (str): File System Mount Point.
            label (str): File System Label.
            media_type (str): File System Media Type.
            size_bytes (int): File System Size in bytes.
            free_space_bytes (int): File System Free Space in bytes.
            company (str): sys_id of ServiceNow company.
            sys_id (str): sys_id of File System.
            snow_device_id (str): sys_id of ServiceNow Device.
            correlation (DeviceCorrelation): Device Correlation Object.
            domain (str): sys_id of ServiceNow Domain
        """

        self.correlation = correlation
        self.region = region
        self.short_description = short_description
        self.name = name
        self.sl1_fs_id = sl1_fs_id
        self.sys_id = sys_id

        if mount_point:
            self.mount_point = mount_point
        else:
            self.mount_point = self.name
        if label:
            self.label = label
        else:
            self.label = self.name
        if media_type:
            self.media_type = media_type
        else:
            self.media_type = None
        if size_bytes:
            self.size_bytes = size_bytes
        else:
            self.size_bytes = 0
        if free_space_bytes:
            self.free_space_bytes = free_space_bytes
        else:
            self.free_space_bytes = 0
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
                    "values": {
                        "sys_id": self.snow_device_id
                    }
                }
            ],
            "relations": [
                {
                    "child": 1,
                    "parent": 0,
                    "type": "Contains::Contained by"
                }
            ]
        }

        file_system_info = {
            "className": "cmdb_ci_file_system",
            "values": {
                "x_sclo_scilogic_region": self.region,
                "x_sclo_scilogic_id": self.sl1_fs_id,
                "x_sclo_scilogic_monitored": True,
                "name": self.name,
                "label": self.label,
                "mount_point": self.mount_point,
                "media_type": self.media_type,
                "size_bytes": self.size_bytes,
                "free_space_bytes": self.free_space_bytes,
                "short_description": self.short_description,
                "operational_status": 1,
                "install_status": 1
            }
        }
        if self.company:
            info['items'][0]['values'].update({'company': self.company})
            file_system_info['values'].update({'company': self.company})
        if self.sys_id:
            file_system_info['values'].update({"sys_id": self.sys_id})
        if self.snow_device_id:
            file_system_info['values'].update({"computer": self.snow_device_id})
        if self.domain and self.domain != "global":
            info['items'][0]['values'].update({'sys_domain': self.domain})
            file_system_info['values'].update({'sys_domain': self.domain})

        info['items'].append(file_system_info)

        return info
