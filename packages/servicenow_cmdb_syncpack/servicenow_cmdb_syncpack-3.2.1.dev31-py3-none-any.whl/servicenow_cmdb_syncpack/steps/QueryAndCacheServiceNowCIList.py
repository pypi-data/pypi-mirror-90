from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon import ipaas_exceptions
from ipaascommon.content_manger import IpaasContentManager
from ipaascommon.metadata_constants import SERVICENOW_DEFAULT_ID
from servicenow_cmdb_syncpack.util.device_utils import ci_list_cache_key


class QueryAndCacheServiceNowCIList(QueryREST):

    def __init__(self):
        super(QueryAndCacheServiceNowCIList, self).__init__()
        self.friendly_name = \
            "Query and ServiceNow CI info"
        self.description = "Queries a ServiceNow instance for all available" \
                           " CIs and saves the data to cache with the" \
                           "specified servicenow id",
        self.version = "1.1.2"

    def execute(self):
        """
        All logic main logic for executing the step happens here
        :return:
        """
        # Execute main query rest first
        super(QueryAndCacheServiceNowCIList, self).execute()
        ci_list = self.get_current_saved_data()
        if not ci_list:
            raise ipaas_exceptions.\
                StepFailedException("No CIs were returned when querying "
                                    "ServiceNow. Please validate the required "
                                    "scheduled job has been run to generate the"
                                    " tables, and the provided user has "
                                    "sufficient access")
        cmanager = IpaasContentManager()
        cmanager.save_to_cache(ci_list_cache_key(SERVICENOW_DEFAULT_ID),
                               ci_list)
        # This doesn't have data for a next step. Clean out whatever
        # may be there
        self.save_data_for_next_step({})
