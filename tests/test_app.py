import pytest

from data_read import CsvDataReader
from presenters import ConsolePresenter, JSONPresenter
from report_generation import ReportGeneratorImpl
from settings import REPORT_CONFIGS


def test_csv_reader(sample_csv):
    reader = CsvDataReader()
    data = reader.read_files([sample_csv])

    assert len(data) == 4
    assert data["1"].name == "Alice Johnson"
    assert data["3"].rate == 60


def test_report_generator_grouping(sample_csv):
    reader = CsvDataReader()
    data = reader.read_files([sample_csv])

    generator = ReportGeneratorImpl(REPORT_CONFIGS)
    report = generator.generate("payout", data)

    assert "groups" in report
    assert any(g["name"] == "Design" for g in report["groups"])
    design_group = next(g for g in report["groups"] if g["name"] == "Design")
    assert len(design_group["rows"]) == 2

    payouts = [int(row["payout"].replace("$", "")) for row in design_group["rows"]]
    assert payouts == [6000, 10200]

    totals = design_group["totals"]
    assert totals["payout"] == "$16200"
    assert totals["hours_worked"] == "320"


def test_json_presenter_output(sample_csv, capsys):
    reader = CsvDataReader()
    data = reader.read_files([sample_csv])
    generator = ReportGeneratorImpl(REPORT_CONFIGS)
    report = generator.generate("payout", data)

    presenter = JSONPresenter()
    presenter.present(report, "payout")
    output = capsys.readouterr().out
    assert "Design" in output
    assert "payout" in output
    assert output.startswith("[") or output.startswith("{")


def test_console_presenter_output(sample_csv, capsys):
    reader = CsvDataReader()
    data = reader.read_files([sample_csv])
    generator = ReportGeneratorImpl(REPORT_CONFIGS)
    report = generator.generate("payout", data)

    presenter = ConsolePresenter()
    presenter.present(report, "payout")
    output = capsys.readouterr().out
    assert "Design" in output
    assert "Alice Johnson" in output
    assert "$" in output


def test_invalid_report_name():
    generator = ReportGeneratorImpl(REPORT_CONFIGS)
    with pytest.raises(ValueError, match="не поддерживается"):
        generator.generate("unknown", {})


def test_missing_file():
    reader = CsvDataReader()
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        reader._read_csv("non_existing_file.csv")


def test_custom_column_names(tmp_path):
    file_path = tmp_path / "custom.csv"
    file_path.write_text(
        """
id,email,name,department,hours_worked,salary
1,john@example.com,John Smith,Sales,100,10
        """.strip()
    )
    reader = CsvDataReader()
    data = reader.read_files([str(file_path)])
    assert data["1"].rate == 10


def test_override_format_and_formula_with_custom_configs(sample_csv):
    custom_report_configs = {
        "payout": {
            "display_columns": [
                {"name": "department", "title": "", "grouping": True},
                {"name": "name", "title": "Employee"},
                {"name": "hours_worked", "title": "H", "summarize": True},
                {"name": "rate", "title": "R"},
                {"name": "payout", "title": "P",
                 "calculate": lambda row: (row.rate + 1) * row.hours_worked,
                 "format": "USD {0}",
                 "summarize": True}
            ]
        }
    }

    reader = CsvDataReader()
    data = reader.read_files([sample_csv])
    generator = ReportGeneratorImpl(custom_report_configs)
    report = generator.generate("payout", data)

    design_group = next(g for g in report["groups"] if g["name"] == "Design")
    assert "USD" in design_group["rows"][0]["payout"]
    assert report["columns"][1]["title"] == "Employee"

