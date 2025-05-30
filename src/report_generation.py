from abc import ABC, abstractmethod
from collections import defaultdict

from data_read import RowData
from presenters import ReportDict


class ReportGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        report_name: str,
        report_data: dict[str, RowData]
    ) -> ReportDict: ...


class ReportGeneratorImpl(ReportGenerator):
    def __init__(self, report_configs: dict):
        self._report_configs = report_configs

    def generate(
        self,
        report_name: str,
        report_data: dict[str, RowData]
    ) -> ReportDict:
        if report_name not in self._report_configs:
            raise ValueError(f"Отчёт '{report_name}' не поддерживается.")

        config = self._report_configs[report_name]
        rows = list(report_data.values())

        group_col = next(
            (col for col in config["display_columns"] if col.get("grouping")),
            None
        )
        has_grouping = group_col is not None

        grouped_data = self._group_rows(
            rows, group_col["name"]
        ) if has_grouping else {"All": rows}
        return self._prepare_report_data(grouped_data, config)

    def _group_rows(
        self,
        rows: list[RowData],
        group_by: str
    ) -> dict[str, list[RowData]]:
        grouped = defaultdict(list)
        for row in rows:
            grouped[getattr(row, group_by)].append(row)
        return grouped

    def _prepare_report_data(
        self,
        grouped_data: dict[str, list[RowData]],
        config: dict
    ) -> ReportDict:
        display_columns = config["display_columns"]
        group_by_col = next(
            (col for col in display_columns if col.get("grouping")),
            None
        )
        group_by_name = group_by_col["name"] if group_by_col else None

        report: ReportDict = {
            "groups": [],
            "columns": display_columns,
            "widths": {
                col["name"]: (
                    max(len(name) for name in grouped_data.keys()) if col.get("grouping")
                    else len(col["title"])
                )
                for col in display_columns
            },
        }

        for group_name, rows in grouped_data.items():
            group = {"name": group_name, "rows": [], "totals": {}}

            for row in rows:
                row_data = {}
                for col in display_columns:
                    if col["name"] == group_by_name:
                        continue

                    value = col["calculate"](row) if "calculate" in col\
                        else getattr(row, col["name"])
                    formatted = col.get("format", "{}").format(value)
                    row_data[col["name"]] = formatted
                    report["widths"][col["name"]] = max(
                        report["widths"][col["name"]],
                        len(formatted)
                    )
                group["rows"].append(row_data)

            for col in display_columns:
                if col.get("summarize"):
                    values = [
                        col["calculate"](row) if "calculate" in col
                        else getattr(row, col["name"]) for row in rows
                    ]
                    total = sum(values)
                    formatted = col.get("format", "{}").format(total)
                    group["totals"][col["name"]] = formatted
                    report["widths"][col["name"]] = max(
                        report["widths"][col["name"]], len(formatted)
                    )

            report["groups"].append(group)

        return report
