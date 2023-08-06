from business_service_utils import BusinessServiceReferenceList
from ipaascore.BaseStep import BaseStep
import pickle
import codecs


class ProcessServiceUpdatesSNtoSL(BaseStep):

    def __init__(self):
        self.friendly_name = "Process Business Service Updates"
        self.description = (
            "Processes SL1 Business Service updates, "
            "using a previously generated"
            "reference list, and new data "
            "from a recent response of SL1 mutation creates"
        )
        self.version = "0.0.1"

    def execute(self):
        previous_data = self.get_data_from_step_by_name("Data Passthrough")
        raw_bserve_data = self.get_data_from_step_by_name("Create Business Services")
        # support old GQL which doesnt throw errors, and new gql which does
        if raw_bserve_data.get("data_out", None) is not None and\
                raw_bserve_data.get("errors", None) is not None:
            sl1_result = raw_bserve_data.get("data_out").get(
                "saveHarProviders", {}).get("definition", {}).get("result", [])
            sl1_errors = raw_bserve_data.get("errors", [])
        else:
            sl1_result = self.get_data_from_step_by_name(
                "Create Business Services"
            ).get("saveHarProviders", {}).get("definition", {}).get("result",
                                                                    [])
            sl1_errors = []

        if sl1_errors:
            pass
        """
        TODO Better handling of the errors, log to the user specific devices
        that failed and the repurcussions (missing child etc)
        """
        brl = pickle.loads(codecs.decode(previous_data.encode(), "base64"))
        # updates newly created services with their unique SL1 id
        brl.populate_with_sl1_data(sl1_result)
        create_payloads, update_payloads, in_sl1_not_in_snow = brl.get_all_payloads()
        self.logger.flow("{} Services to be updated".format(
            len(update_payloads)))
        save_data = {"updates": {"definition": update_payloads}}
        self.save_data_for_next_step(save_data)
