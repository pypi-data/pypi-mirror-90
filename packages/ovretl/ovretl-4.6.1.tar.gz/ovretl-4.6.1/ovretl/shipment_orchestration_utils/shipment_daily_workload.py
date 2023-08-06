import pandas as pd
import datetime

from ovretl.shipment_orchestration_utils.utils import datetime_to_date


def total_tasks_weight(tasks_df: pd.DataFrame) -> pd.DataFrame:
    tasks_df = tasks_df.loc[:, ["shipment_id", "weight"]].groupby("shipment_id").sum()
    return tasks_df.rename(columns={"weight": "total_tasks_weight"})


def daily_tasks_total_weight_on_shipment(shipment_id: any, tasks_df: pd.DataFrame, date: datetime.date) -> int:
    is_shipment_tasks = tasks_df["shipment_id"] == shipment_id
    is_todo_task_due_date = (tasks_df["status"] == "to_do") & (tasks_df["due_date"] == date)
    is_done_task_done_date = (tasks_df["status"] == "done") & (tasks_df["updated_date"] == date)
    tasks_todo_today_on_shipment_df = tasks_df[is_shipment_tasks & (is_todo_task_due_date | is_done_task_done_date)]
    if len(tasks_todo_today_on_shipment_df["shipment_id"]) == 0:
        return 0
    daily_tasks_todo_total_weight_df = (
        tasks_todo_today_on_shipment_df.loc[:, ["shipment_id", "weight"]].groupby("shipment_id").sum()
    )
    return daily_tasks_todo_total_weight_df.at[shipment_id, "weight"]


def shipment_total_workflows_weight(
    active_shipments_df: pd.DataFrame, shipment_associated_workflows_df: pd.DataFrame
) -> pd.DataFrame:
    shipment_associated_workflows_df.rename(columns={"created_at": "association_created_at"})
    shipments_with_workflows_df = pd.merge(
        active_shipments_df[["shipment_id"]],
        shipment_associated_workflows_df[["shipment_id", "total_workflow_weight"]],
        how="left",
        on="shipment_id",
    )
    shipment_total_workflows_weight_df: pd.DataFrame = shipments_with_workflows_df.loc[
        :, ["shipment_id", "total_workflow_weight"]
    ].groupby("shipment_id").sum()
    shipment_total_workflows_weight_df = shipment_total_workflows_weight_df.rename(
        columns={"total_workflow_weight": "total_workflows_weight"}
    )
    shipment_total_workflows_weight_df = pd.merge(
        active_shipments_df, shipment_total_workflows_weight_df, how="left", on="shipment_id"
    )
    return shipment_total_workflows_weight_df


def find_shipment_workflow_start_date(
    shipment_id: str, shipment_associated_workflows_df: pd.DataFrame
) -> datetime.date:
    shipment_workflow_start_datetime = shipment_associated_workflows_df[
        shipment_associated_workflows_df["shipment_id"] == shipment_id
    ]["created_at"].iloc[0]
    return shipment_workflow_start_datetime.date()


def shipments_remaining_days(
    shipment_df: pd.DataFrame, shipment_associated_workflows_df: pd.DataFrame, today: datetime.date
) -> pd.DataFrame:
    workflow_start_dates = [
        find_shipment_workflow_start_date(shipment_id, shipment_associated_workflows_df)
        for shipment_id in shipment_df["shipment_id"]
    ]
    shipment_df.loc[:, "workflow_start_date"] = workflow_start_dates
    shipment_df.loc[:, "remaining_days"] = shipment_df["transit_time"] - (
        today - shipment_df["workflow_start_date"]
    ).apply(lambda delta: delta.days)
    shipment_df.loc[:, "remaining_days"] = shipment_df["remaining_days"].clip(lower=0)
    return shipment_df


def shipments_timelines(active_shipments_df: pd.DataFrame, shipment_associated_workflows: pd.DataFrame) -> pd.DataFrame:
    shipments_timelines_list = []
    for index, row in active_shipments_df.iterrows():
        shipment_timeline_df = pd.DataFrame(data={"shipment_id": [], "dates": []})
        start_date = find_shipment_workflow_start_date(
            shipment_id=row["shipment_id"], shipment_associated_workflows_df=shipment_associated_workflows
        )
        transit_time = row["transit_time"]
        dates = pd.date_range(start=start_date, periods=transit_time)
        shipment_timeline_df["dates"] = dates
        shipment_timeline_df["shipment_id"] = row["shipment_id"]
        shipments_timelines_list.append(shipment_timeline_df)
    shipments_timelines_df = pd.concat(shipments_timelines_list)
    shipments_timelines_df.loc[:, "dates"] = shipments_timelines_df["dates"].apply(datetime_to_date)
    return shipments_timelines_df


def estimated_remaining_daily_workload(
    active_shipments_df: pd.DataFrame,
    shipment_associated_workflows_df: pd.DataFrame,
    tasks_df: pd.DataFrame,
    today: datetime.date,
) -> pd.DataFrame:
    active_shipments_df = shipment_total_workflows_weight(
        active_shipments_df=active_shipments_df, shipment_associated_workflows_df=shipment_associated_workflows_df,
    )
    active_shipments_df = shipments_remaining_days(active_shipments_df, shipment_associated_workflows_df, today)
    total_tasks_weight_df = total_tasks_weight(tasks_df=tasks_df)
    active_shipments_df = pd.merge(active_shipments_df, total_tasks_weight_df, on="shipment_id", how="left")
    active_shipments_df.loc[:, "estimated_remaining_daily_workload"] = (
        active_shipments_df["total_workflows_weight"] - active_shipments_df["total_tasks_weight"]
    ) / active_shipments_df["remaining_days"]
    active_shipments_df["estimated_remaining_daily_workload"] = active_shipments_df[
        "estimated_remaining_daily_workload"
    ].fillna(0)
    return active_shipments_df


def daily_workload_calculation(shipments_timelines_df: pd.DataFrame, tasks_df: pd.DataFrame) -> pd.DataFrame:
    tasks_df.loc[:, "due_date"] = tasks_df["due_date"].apply(datetime_to_date)
    tasks_df.loc[:, "updated_date"] = tasks_df["updated_date"].apply(datetime_to_date)
    shipments_timelines_df.loc[:, "created_tasks_weight"] = shipments_timelines_df.apply(
        lambda row: daily_tasks_total_weight_on_shipment(
            shipment_id=row["shipment_id"], tasks_df=tasks_df, date=row["dates"]
        ),
        axis=1,
    )
    shipments_timelines_df.loc[:, "daily_workload"] = (
        shipments_timelines_df["created_tasks_weight"] + shipments_timelines_df["estimated_remaining_daily_workload"]
    )
    return shipments_timelines_df


def shipments_daily_workload_timelines(
    active_shipments_df: pd.DataFrame,
    tasks_df: pd.DataFrame,
    shipment_associated_workflows_df: pd.DataFrame,
    today: datetime.date,
) -> pd.DataFrame:
    tasks_df = tasks_df.loc[:, ["shipment_id", "due_date", "status", "weight", "updated_date"]]
    active_shipments_df = estimated_remaining_daily_workload(
        active_shipments_df=active_shipments_df,
        shipment_associated_workflows_df=shipment_associated_workflows_df,
        tasks_df=tasks_df,
        today=today,
    )
    shipments_timelines_df = shipments_timelines(
        active_shipments_df, shipment_associated_workflows=shipment_associated_workflows_df
    )
    shipments_timelines_df = pd.merge(shipments_timelines_df, active_shipments_df, how="left", on="shipment_id")
    shipments_timelines_df.loc[shipments_timelines_df["dates"] < today, "estimated_remaining_daily_workload"] = 0.0
    shipments_timelines_df = daily_workload_calculation(
        shipments_timelines_df=shipments_timelines_df, tasks_df=tasks_df
    )
    return shipments_timelines_df[["shipment_id", "dates", "daily_workload"]]
