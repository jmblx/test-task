import json
import typing
from typing import TypedDict

from settings import has_grouping


class ColumnConfig(TypedDict, total=False):
    name: str
    title: str
    grouping: bool
    summarize: bool
    format: str
    calculate: typing.Callable


class GroupDict(TypedDict):
    name: str
    rows: list[dict[str, str]]
    totals: dict[str, str]


class ReportDict(TypedDict):
    columns: list[ColumnConfig]
    widths: dict[str, int]
    groups: list[GroupDict]


class ReportPresenter:
    def present(self, report: ReportDict, report_name: typing.Literal["payout"]) -> None:
        raise NotImplementedError


class ConsolePresenter(ReportPresenter):
    def present(
        self,
        report: ReportDict,
        report_name: typing.Literal["payout"]
    ) -> None:

        columns = report["columns"]
        widths = report["widths"]

        header = [col["title"].ljust(widths[col["name"]] + 2) for col in columns]
        print("".join(header))

        for group in report["groups"]:
            if has_grouping(report_name):
                group_line = []
                for col in columns:
                    width = widths[col["name"]] + 2
                    if col.get("grouping"):
                        group_line.append(group["name"].ljust(width))
                    else:
                        group_line.append("".ljust(width))
                print("".join(group_line))

            for row in group["rows"]:
                line = []
                for col in columns:
                    width = widths[col["name"]] + 2
                    if col.get("grouping"):
                        line.append(("—" * (width - 1)) + " ")
                    else:
                        line.append(row[col["name"]].ljust(width))
                print("".join(line))

            if group["totals"]:
                totals_line = []
                for col in columns:
                    width = widths[col["name"]] + 2
                    totals_line.append(group["totals"].get(col["name"], "").ljust(width))
                print("".join(totals_line))


class JSONPresenter(ReportPresenter):
    def present(self, report: ReportDict, report_name: typing.Literal["payout"]) -> None:
        output = report["groups"]
        print(json.dumps(output, indent=2))
