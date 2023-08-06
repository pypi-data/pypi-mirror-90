import datetime
import time
from typing import Optional

from jinja2 import Template

from servicenow_base_syncpack.util.helpers import datetime_to_snow_str


class CMDBObject:
    """Base Device class to provide common functions."""

    def __init__(self, sl1_id: str, region: str, sys_id: str = None):
        self.snow_sys_id = sys_id
        self.domain_sys_id = None
        self.region = region
        self.sl1_id = sl1_id

    def eval_template(self, template: str, obj_type: str = "device") -> (str, None):
        """
        Evaluate Attribute Template.

        Args:
            template: Template to evaluate.
            obj_type: device or company

        Returns:

        """
        t = Template(template)
        if obj_type == "device":
            value = t.render(device=self)
        elif obj_type == "company":
            value = t.render(company=self)
        else:
            value = t.render(cmdb_object=self)
        return value

    def dict_to_properties(self, in_dict: dict):
        for key, value in in_dict.items():
            setattr(self, key, value)

    def set_domain_sys_id(self, sys_domain: Optional[str]):
        if sys_domain == "global":
            self.domain_sys_id = None
        else:
            self.domain_sys_id = sys_domain

    def is_usable_attribute(self, *args):
        raise NotImplementedError


def object_changed(sl1_object: CMDBObject, snow_object: CMDBObject, attr_mappings: dict, logger=None) -> bool:
    """
    Return true or false whether or not there's been a change in the device.

    Args:
        sl1_object: The SL1Device as
            instantiated from the SL1 query data
        snow_object: The ServiceNowDevice as
            instantiated from the ServiceNow CI query data
        attr_mappings: Mappings of sl1 attribute to snow attributes
            provided by the user
        logger: Logger instance from Step

    Returns:
        bool
    """
    for sl1_field, snow_fields in attr_mappings.items():
        if not sl1_object.is_usable_attribute(sl1_field):
            continue
        if "{{" in sl1_field:  # Template handling
            sl1_value = sl1_object.eval_template(sl1_field, logger)
        else:
            sl1_value = getattr(sl1_object, sl1_field, None)

        try:
            sl1_value = sl1_transform_to_snow(sl1_field, sl1_value)
        except (ValueError, TypeError):
            continue
        for snow_field in snow_fields:
            if "{{" in snow_field:
                snow_value = snow_object.eval_template(snow_field, logger)
            else:
                snow_value = getattr(snow_object, snow_field, None)
            if snow_value != sl1_value:
                return True

    return False


def chunk_cis(payloads, chunk_size, domain_sep=False, logger=None):
    """
    Chunk CI Objects into groups of CIs.

    Args:
        payloads: List of all device Objects.
        chunk_size (int): Number of objects per payload.
        domain_sep (bool): Enable domain enforcement.
        logger: Step Logger

    Returns:
        list: List of Lists of <chunk_size> CIs

    """
    loop_list = []
    chunked_payloads = []
    count = 0

    for payload in payloads:
        if domain_sep:
            if not validate_domains(payload, logger):
                continue
        if count + len(payload["items"]) <= int(chunk_size):
            loop_list.append(payload)
        else:
            chunked_payloads.append(loop_list)
            loop_list = []
            count = 0
            loop_list.append(payload)
        count += len(payload["items"])
    if loop_list:
        chunked_payloads.append(loop_list)
    return chunked_payloads


def validate_domains(payload: dict, logger=None) -> bool:
    """
    Validates that all sys_domains are the same in the payload.

    Args:
        payload: SNOW payload
        logger: SL1Logger

    Returns:

    """
    domains = set()
    for item in payload["items"]:
        try:
            domains.add(item["values"]["sys_domain"])
        except KeyError:
            logger.warning(
                "Item in payload is missing domain. Dropping.\n"
                "Item: {}\n"
                "Full Payload: {}".format(item, payload)
            )
            return False
    if len(domains) is not 1:
        logger.warning(
            "Items in payload are not all members of the same "
            "domain. Dropping.\n"
            "Payload: {}".format(payload)
        )
        return False

    return True


def sl1_transform_to_snow(attr_name, attr_value):
    """
    Accepts an attribute name, and its value. If the attribute name is identifed
    as one that requires a conversion (IE disk_space, the conversion will be
    performed and the transformed data will be returned. Another possible
    transformation is if the value is a datetime object, it will be transformed
    into the ServiceNow expected string. If no transformations are needed,
    the provided value will be returned unchanged
    Args:
        attr_name (str): name of the servicenow attribute this value pertains to
        attr_value (obj): the correlating servicenow value for the attribtue
    Returns:
        object: Some object transformed to ServiceNow's stipulation

    """
    byte_to_gb_conversion_needed = ["diskSize"]
    if attr_name in byte_to_gb_conversion_needed:
        if not attr_value:
            return attr_value
        try:
            return int(str(attr_value).replace(",", "")) >> 30
        except ValueError:
            return attr_value

    if isinstance(attr_value, datetime.date) or isinstance(
        attr_value, datetime.datetime
    ):
        try:
            date_val = datetime_to_snow_str(attr_value)
        except ValueError:  # Drop bad dates from SL
            date_val = ""
        return date_val
    if "date" in attr_name.lower():
        date_value = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(attr_value)))
        return date_value

    return attr_value
