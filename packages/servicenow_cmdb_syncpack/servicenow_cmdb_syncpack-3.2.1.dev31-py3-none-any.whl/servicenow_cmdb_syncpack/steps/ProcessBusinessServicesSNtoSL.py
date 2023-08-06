import pickle
import codecs
from business_service_utils import (
    BusinessServiceReferenceList,
    identify_delete_ids
)
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore.BaseStep import BaseStep
from ipaascore.parameter_types import (
    MappingParameterStaticOneToOne
)
from servicenow_base_syncpack.util.snow_parameters import (
    domain_sep_param,
    region_param
)


class ProcessBusinessServicesSNtoSL(BaseStep):

    def __init__(self):
        self.friendly_name = "Process Business Services to SL1"
        self.description = (
            "Processes ServiceNow services and transforms to SL1 services"
        )
        self.version = "0.0.1"
        self.add_step_parameter_from_object(region_param)
        self.new_step_parameter(name="attribute_map",
                                description="Mapping overrides to set. "
                                            "The left side key will be"
                                            " retrieved from SNOW value and"
                                            " inserted into SL1 payload as"
                                            " the specified right side value ",
                                param_type=MappingParameterStaticOneToOne(
                                    [],[], "ServiceNow Key",
                                    "SL1 Payload Attribute", custom=True),
                                default_value={}, required=False)
        self.add_step_parameter_from_object(domain_sep_param)

    def execute(self):
        region = "ServiceNow+{}".format(self.get_parameter(region_param.name))
        overrides = self.get_parameter("attribute_map")
        snow_bservice_data = self.get_data_from_step_by_name(
            "Pull Business Services from ServiceNow"
        )
        sl1_service_data = self.get_data_from_step_by_name(
            "Fetch Business Services from SL1")
        org_data = pickle.loads(
            self.get_data_from_step_by_name("Fetch Orgs from SL1")
        )

        brl = BusinessServiceReferenceList(self.logger, overrides=overrides)
        brl.populate_with_sl1_data(sl1_service_data)
        brl.populate_with_snow_data(snow_bservice_data)
        brl.populate_with_org_data(org_data)
        brl.populate_regions(region)

        create_payloads, update_payloads, in_sl1_not_in_this_snow = \
            brl.get_all_payloads()

        delete_payloads = identify_delete_ids(in_sl1_not_in_this_snow, region)

        self.logger.flow("{} Services to be created. {} Services to be updated."
                         " {} Services to be deleted"
                         .format(len(create_payloads),
                                 len(update_payloads),
                                 len(delete_payloads)))

        base64_encoded_pickle_bytes = codecs.encode(pickle.dumps(brl),
                                                    "base64").decode()
        save_data = {"creates": {"definition": create_payloads},
                     "existing_data": base64_encoded_pickle_bytes,
                     "deletes": {"ids": delete_payloads}}
        self.save_data_for_next_step(save_data)


