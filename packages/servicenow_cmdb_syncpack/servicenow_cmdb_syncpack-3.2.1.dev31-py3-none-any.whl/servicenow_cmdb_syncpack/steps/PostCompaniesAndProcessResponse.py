from base_steps_syncpack.steps.QueryREST import QueryREST


class PostCompaniesAndProcessResponse(QueryREST):
    def __init__(self):
        super(PostCompaniesAndProcessResponse, self).__init__()
        self.friendly_name = "Process Company Table Response for SL1 Callback"
        self.description = (
            "Processes response from Company table post to " "send sys_id back to SL1."
        )
        self.version = "2.0.0"

        self.new_step_parameter(
            name="snow_data",
            default_value=None,
            required=True,
            description="Payload posted to ServiceNow in " "previous step.",
            param_type=None,
        )

    def execute(self):
        """
        All logic main logic for executing the step happens here
        :return:
        """
        super(PostCompaniesAndProcessResponse, self).execute()
        snow_response = self.get_current_saved_data().get("records", [])
        self.logger.debug("Snow Response: {}".format(snow_response))

        created = []
        updated = 0
        ignored = 0
        failed = 0

        for company in snow_response:
            state = company.get("sys_import_state")
            if state == "inserted" and company.get("__status") == "success":
                self.logger.flow(
                    "Company {} created with sys_id {}".format(
                        company.get("name"), company.get("sys_target_sys_id")
                    )
                )
                created.append(
                    {
                        "uri": "/api/organization/{}".format(company.get("id")),
                        "payload": {"crm_id": company.get("sys_target_sys_id")},
                    }
                )
            elif state == "updated":
                updated += 1
                self.logger.flow("Company {} updated.".format(company.get("name")))

            elif state == "ignored":
                ignored += 1
                self.logger.info(
                    "Company {} ignored. Reason: {}".format(
                        company.get("name"), company.get("sys_import_state_comment")
                    )
                )
            elif state == "error":
                failed += 1
                self.logger.error(
                    "Company {} failed. Reason: {}".format(
                        company.get("name"), company.get("sys_import_state_comment")
                    )
                )
                self.logger.debug("Company payload: {}".format(company))

        self.logger.flow(
            "Created: {}, Updated: {}, Ignored: {}, Failed {}".format(
                len(created), updated, ignored, failed
            )
        )

        self.save_data_for_next_step({"sl1Updates": created})
