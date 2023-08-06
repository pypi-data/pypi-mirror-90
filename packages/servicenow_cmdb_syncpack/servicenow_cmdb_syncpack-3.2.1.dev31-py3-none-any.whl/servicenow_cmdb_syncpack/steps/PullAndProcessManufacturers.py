from base_steps_syncpack.steps.MySqlSelect import MySqlSelect


class PullAndProcessManufacturers(MySqlSelect):

    def __init__(self):
        super(PullAndProcessManufacturers, self).__init__()
        self.friendly_name = "Pull And Process Manufacturers"
        self.description = "Parse pulled asset data from SL1 and ServiceNow"
        self.version = "2.0.0"

    def execute(self):
        super(PullAndProcessManufacturers, self).execute()
        sl1_asset = self.get_current_saved_data()

        self.logger.debug(u"sl1_asset: {}".format(sl1_asset))

        manufacturers = []

        self.logger.info("Starting manufacturer search.")
        for asset in sl1_asset:
            if asset['make']:
                manufacturers.append(asset['make'])
            else:
                continue

        self.logger.flow(
            u"Sending {} Manufacturers to ServiceNow for Matching.".format(
                len(manufacturers)
            )
        )
        self.logger.debug(u"Manufacturers: {}".format(manufacturers))
        self.save_data_for_next_step(
            {
                "manufactures": manufacturers
            }
        )
