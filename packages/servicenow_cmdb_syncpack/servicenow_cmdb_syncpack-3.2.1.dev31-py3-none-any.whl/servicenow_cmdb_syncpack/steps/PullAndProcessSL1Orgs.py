import pickle

from base_steps_syncpack.steps.QueryREST import OBJECT_KEY_VAL, QueryREST
from servicenow_base_syncpack.util.snow_parameters import region_param
from servicenow_cmdb_syncpack.util.org_utils import SL1Org


class PullAndProcessSL1Orgs(QueryREST):
    def __init__(self):
        super(PullAndProcessSL1Orgs, self).__init__()
        self.friendly_name = "Pull and Process SL1 Organizations"
        self.description = (
            "Pulls Organizations from SL1 and converts them into SL1Org objects."
        )
        self.version = "1.0.0"

        self.add_step_parameter_from_object(region_param)

    def execute(self):
        super(PullAndProcessSL1Orgs, self).execute()
        region = self.get_parameter(region_param.name)
        result = self.get_current_saved_data()
        self.logger.flow(f"Pulled {len(result)} Organizations from SL1.")
        self.logger.info(f"Pulled Orgs: {result}")
        processed_orgs = dict()
        for org in result:
            sl1_org = SL1Org(org.pop(OBJECT_KEY_VAL), org, region)
            processed_orgs[sl1_org.sl1_id] = sl1_org

        self.save_data_for_next_step(pickle.dumps(processed_orgs))
