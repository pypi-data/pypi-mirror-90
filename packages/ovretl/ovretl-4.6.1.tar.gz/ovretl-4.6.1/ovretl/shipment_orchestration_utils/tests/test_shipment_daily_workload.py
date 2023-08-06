import pandas as pd

from ovretl.shipment_orchestration_utils.shipment_daily_workload import (
    total_tasks_weight,
    shipment_total_workflows_weight,
    shipments_remaining_days,
    shipments_timelines,
    estimated_remaining_daily_workload,
    daily_tasks_total_weight_on_shipment,
    shipments_daily_workload_timelines,
)
import datetime

from ovretl.shipment_orchestration_utils.utils import datetime_to_date


def test_total_task_weight():
    tasks_df = pd.DataFrame(data={"shipment_id": ["1", "2", "2", "1"], "weight": [1, 2, 3, 5]})
    result_should_be = pd.DataFrame(data={"shipment_id": ["1", "2"], "total_tasks_weight": [6, 5]}).set_index(
        "shipment_id"
    )
    result = total_tasks_weight(tasks_df)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_daily_tasks_total_weight_on_shipment():
    today_date = datetime.date(2020, 12, 28)
    other_date = datetime.date(2001, 1, 1)
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "1", "2", "2", "1"],
            "status": ["done", "to_do", "to_do", "to_do", "to_do"],
            "due_date": [other_date, today_date, today_date, other_date, today_date],
            "updated_date": [today_date, today_date, today_date, other_date, today_date],
            "weight": [1, 2, 3, 4, 5],
        }
    )
    result_should_be = 8
    result = daily_tasks_total_weight_on_shipment("1", tasks_df, today_date)
    assert result_should_be == result


def test_shipment_total_workflows_weight():
    sh_df = pd.DataFrame(data={"shipment_id": ["1", "2"]})
    sh_wf_as_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "1", "2"],
            "workflow_id": ["1", "2", "3", "4"],
            "total_workflow_weight": [1, 2, 3, 4],
        }
    )
    result_should_be = pd.DataFrame(data={"shipment_id": ["1", "2"], "total_workflows_weight": [4, 6]})
    result = shipment_total_workflows_weight(sh_df, sh_wf_as_df)
    print(result_should_be)
    print(result)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_count_shipment_remaining_days():
    today = datetime.datetime(2020, 12, 28)
    day_before_1 = datetime.datetime(2020, 12, 27)
    day_before_2 = datetime.datetime(2020, 12, 26)

    sh_df = pd.DataFrame(data={"shipment_id": ["1", "2", "3"], "transit_time": [10, 10, 10]})
    sh_wf_as_df = pd.DataFrame(data={"shipment_id": ["1", "2", "3"], "created_at": [today, day_before_1, day_before_2]})
    result_should_be = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "3"],
            "transit_time": [10, 10, 10],
            "workflow_start_date": [today.date(), day_before_1.date(), day_before_2.date()],
            "remaining_days": [10, 9, 8],
        }
    )
    result = shipments_remaining_days(sh_df, sh_wf_as_df, today.date())
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipments_timelines():
    day_1 = datetime.datetime(2020, 12, 28)
    day_2 = datetime.datetime(2020, 12, 29)
    day_3 = datetime.datetime(2020, 12, 30)
    day_4 = datetime.datetime(2020, 12, 31)
    day_5 = datetime.datetime(2021, 1, 1)
    sh_df = pd.DataFrame(data={"shipment_id": ["1", "2"], "transit_time": [2, 3]})
    sh_as_wf_df = pd.DataFrame(
        data={"shipment_id": ["1", "2"], "workflow_id": ["1", "2"], "created_at": [day_1, day_3]}
    )
    result_should_be = pd.DataFrame(
        data={"shipment_id": ["1", "1", "2", "2", "2"], "dates": [day_1, day_2, day_3, day_4, day_5]}
    ).set_index("shipment_id")
    result_should_be.loc[:, ["dates"]] = result_should_be["dates"].apply(datetime_to_date)
    print(result_should_be)
    result = shipments_timelines(sh_df, shipment_associated_workflows=sh_as_wf_df).set_index("shipment_id")
    print(result)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_estimated_remaining_daily_workload():
    today = datetime.date(2020, 12, 28)
    sh_df = pd.DataFrame(data={"shipment_id": ["1", "2"], "transit_time": [10, 12]})
    sh_wf_as_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "2"],
            "workflow_id": ["1", "2", "3"],
            "created_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 26),
            ],
            "total_workflow_weight": [1, 10, 50],
        }
    )
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "2", "2", "2"],
            "status": ["to_do", "to_do", "to_do", "done", "to_do"],
            "due_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 30),
            ],
            "weight": [1, 1, 3, 3, 3],
        }
    )
    result_should_be = pd.DataFrame(
        data={
            "shipment_id": ["1", "2"],
            "transit_time": [10, 12],
            "total_workflows_weight": [1, 60],
            "workflow_start_date": [datetime.date(2020, 11, 15), datetime.date(2020, 12, 26)],
            "remaining_days": [0, 10],
            "total_tasks_weight": [1, 10],
            "estimated_remaining_daily_workload": [0.0, 5.0],
        }
    )
    result = estimated_remaining_daily_workload(sh_df, sh_wf_as_df, tasks_df, today)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipments_daily_workload_timelines():
    today = datetime.date(2020, 12, 28)
    sh_df = pd.DataFrame(data={"shipment_id": ["1", "2"], "transit_time": [10, 12]})
    sh_wf_as_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "2"],
            "workflow_id": ["1", "2", "3"],
            "created_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 26),
            ],
            "total_workflow_weight": [1, 10, 50],
        }
    )
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "2", "2", "2", "2", "2"],
            "status": ["to_do", "to_do", "to_do", "done", "to_do", "to_do", "done"],
            "due_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 27),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "updated_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "weight": [1, 1, 3, 3, 3, 10, 10],
        }
    )
    dates_sh_1 = pd.date_range(start=datetime.date(2020, 11, 15), periods=10)
    dates_sh_2 = pd.date_range(start=datetime.date(2020, 12, 26), periods=12)
    shipment_1_workload = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    shipment_2_workload = [3.0, 10.0, 4.0, 6.0, 16.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
    result_should_be_1 = pd.DataFrame(
        data={"shipment_id": "1", "dates": dates_sh_1, "daily_workload": shipment_1_workload,}
    )
    result_should_be_2 = pd.DataFrame(
        data={"shipment_id": "2", "dates": dates_sh_2, "daily_workload": shipment_2_workload,}
    )
    result_should_be = pd.concat([result_should_be_1, result_should_be_2], ignore_index=True)
    result_should_be["dates"] = result_should_be["dates"].apply(datetime_to_date)
    print(result_should_be)
    result = shipments_daily_workload_timelines(
        active_shipments_df=sh_df, tasks_df=tasks_df, shipment_associated_workflows_df=sh_wf_as_df, today=today,
    )
    print(result)
    pd.testing.assert_frame_equal(result, result_should_be)
