from ipaascommon.ipaas_utils import str_to_bool
from ipaascore import parameter_types
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.correlators import DeviceCorrelation
from servicenow_base_syncpack.util.snow_parameters import region_param


class ProcessGroups(BaseStep):

    def __init__(self):
        self.friendly_name = "Process Device Groups"
        self.description = "Parse pulled group data from SL1 and ServiceNow"
        self.version = "2.0.1"
        self.new_step_parameter(
            name="Sync_Empty_Groups", default_value=False,
            description="Send Empty Device Groups to ServiceNow",
            required=False, param_type=parameter_types.BoolParameterCheckbox()
        )
        self.add_step_parameter_from_object(region_param)

    def execute(self):
        region = self.get_parameter(region_param.name)
        sl1_groups = self.get_data_from_step_by_name(
            'Pull Device Groups from SL1 (GQL)')
        sl1_group_ids = self.get_data_from_step_by_name(
            'Pull Group IDs from SL1 (MySQL)')
        send_empty = str_to_bool(self.get_parameter('Sync_Empty_Groups'))

        self.logger.debug(u"sl1_groups: {}".format(sl1_groups))
        self.logger.debug(u"sl1_group_ids: {}".format(sl1_group_ids))

        snow_creates = []

        for group_obj in sl1_groups:
            group = group_obj['deviceGroup']
            name = group['name']
            slid = str(
                [x['dgid'] for x in sl1_group_ids if x['dg_guid'] == group[
                    'id']][0])
            devices = [x['node']['id'] for x in group['devices']['edges']]
            self.logger.info(u"Group: {}, Devices: {}".format(name, devices))
            ci_list = []
            if not send_empty and not devices:
                self.logger.warning(
                    u"Group {} has no devices. Skipping.".format(name))
            for device in devices:
                dev_sys_id = DeviceCorrelation(
                    region, int(device)).get_correlating_dev_snow_id()
                if dev_sys_id:
                    ci_list.append(dev_sys_id)
            if not ci_list and devices and not send_empty:
                self.logger.warning(
                    u"No sys_ids found for devices in Group: {}. "
                    u"Skipping. "
                    u"Ensure Device Sync is scheduled and has run "
                    u"recently.".format(name))
                continue

            snow_creates.append(
                {
                    "items": [
                        {
                            "name": name,
                            "region": region,
                            "id": slid,
                            "manualCIList": ",".join(ci_list)
                        }
                    ]
                }
            )

        if snow_creates:
            self.logger.flow(
                u"Sending {} device groups.".format(len(snow_creates)))
            self.logger.debug(u"snow_creates: {}".format(snow_creates))

            payload = [snow_creates]

            self.save_data_for_next_step(payload)
        else:
            self.logger.flow(u"No Device Groups to send.")
            self.save_data_for_next_step([])
