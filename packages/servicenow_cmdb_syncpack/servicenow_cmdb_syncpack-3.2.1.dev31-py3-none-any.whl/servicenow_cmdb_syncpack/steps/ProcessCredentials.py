from future.utils import iteritems

from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.snow_parameters import region_param


class ProcessCredentials(BaseStep):

    def __init__(self):
        self.friendly_name = "Process Credentials"
        self.description = "Parse pulled Credential data from SL1."
        self.version = "2.0.1"

        self.add_step_parameter_from_object(region_param)

    def execute(self):
        region = self.get_parameter(region_param.name)
        sl1_creds = self.get_data_from_step_by_name(
            'Pull Credentials from SL1 (GQL)')
        sl1_cred_ids = self.get_data_from_step_by_name(
            "Pull Credential IDs from SL1 (MySQL)")

        self.logger.debug("sl1_creds: {}".format(sl1_creds))
        self.logger.debug("sl1_cred_ids: {}".format(sl1_cred_ids))

        snow_creates = []

        for category, v in iteritems(sl1_creds):
            credentials = v['edges']
            self.logger.debug("Category: {}".format(category))
            for credGQL in credentials:
                if credGQL['node']:
                    cred = credGQL['node']
                    self.logger.debug("Cred: {}".format(cred))
                    slid = [
                        x['cred_id'] for x in sl1_cred_ids
                        if x['cred_guid'] == cred['id']]
                    snow_dict = {
                        "category": category,
                        "name": cred['name'],
                        "id": str(slid[0]),
                        "region": region,
                        "record_type": "credential"
                    }
                    if cred['host']:
                        snow_dict["hostname"] = cred['host']
                    snow_creates.append(snow_dict)
                else:
                    continue
        if snow_creates:
            self.logger.flow(
                "Sending {} Credentials.".format(len(snow_creates)))
            self.logger.debug("snow_creates: {}".format(snow_creates))
            self.save_data_for_next_step(snow_creates)
        else:
            self.logger.flow("No Credentials to send.")
            self.save_data_for_next_step([])
