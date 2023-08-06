import pandas as pd


def shipments_accepted_proposition_total_transit_time(shipments_all_propositions_df: pd.DataFrame) -> pd.DataFrame:
    active_shipments = shipments_all_propositions_df[
        ~shipments_all_propositions_df["shipment_status"].isin(["finished", "cancelled"])
    ]
    shipments_accepted_proposition = active_shipments[shipments_all_propositions_df["proposition_status"] == "accepted"]
    shipments_accepted_proposition.loc[:, "total_transit_time"] = (
        shipments_accepted_proposition["transit_time_door_to_port"]
        + shipments_accepted_proposition["transit_time"]
        + shipments_accepted_proposition["transit_time_port_to_door"]
    )
    return shipments_accepted_proposition
