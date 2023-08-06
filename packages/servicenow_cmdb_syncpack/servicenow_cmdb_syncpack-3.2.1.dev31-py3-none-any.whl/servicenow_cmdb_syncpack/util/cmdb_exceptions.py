class MissingRelationsException(Exception):
    """
    MissingRelations Exception: Requested relationship between devices is missing from IS Cache.
    """

    def __init__(
        self, parent_did: str, parent_class: str, child_did: str, child_class: str
    ):
        error = (
            f"No ci match in cache for Parent DID: {parent_did} "
            f"Parent CI: {parent_class} Child DID: {child_did} Child CI: {child_class}"
        )
        super(MissingRelationsException, self).__init__(error)
