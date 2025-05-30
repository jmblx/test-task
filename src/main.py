import argparse

from data_read import CsvDataReader
from presenters import ConsolePresenter, JSONPresenter
from report_generation import ReportGeneratorImpl
from settings import REPORT_CONFIGS

presenters_map = {"console": ConsolePresenter(), "json": JSONPresenter()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SalaryProcessor",
        description="Обрабатывает CSV-файлы с данными о зарплатах.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Пути к CSV-файлам (можно указать несколько)",
        type=str,
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчета (например, 'payout')",
    )
    parser.add_argument(
        "--output",
        help="Формат вывода отчета (например, 'json' или 'console')",
        required=True,
        default="console",
        type=str,
    )
    args = parser.parse_args()

    data = CsvDataReader().read_files(args.files)
    generator = ReportGeneratorImpl(REPORT_CONFIGS)
    report = generator.generate(args.report, data)
    presenter = presenters_map[args.output]
    presenter.present(report, args.report)
