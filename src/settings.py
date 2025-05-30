POSSIBLE_SALARY_NAMES = ["hourly_rate", "rate", "salary"]

REPORT_CONFIGS = {
    "payout": {
        "display_columns": [
            {"name": "department", "title": "", "grouping": True},
            {"name": "name", "title": "name"},
            {"name": "hours_worked", "title": "hours",
             "summarize": True, "format": "{0}"
             },
            {"name": "rate", "title": "rate", "format": "{0}"},
            {"name": "payout", "title": "payout",
             "calculate": lambda row: row.rate * row.hours_worked,
             "format": "${0}",
             "summarize": True}
        ],
    }
}


def has_grouping(report_name: str) -> bool:
    config = REPORT_CONFIGS.get(report_name)
    return any(col["grouping"] for col in config["display_columns"])

