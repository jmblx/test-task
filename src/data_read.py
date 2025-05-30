from abc import ABC, abstractmethod
from dataclasses import dataclass

from settings import POSSIBLE_SALARY_NAMES


@dataclass
class RowData:
    rate: int
    hours_worked: int
    email: str
    name: str
    department: str


class DataReader(ABC):
    @abstractmethod
    def read_files(self, filenames: list[str]) -> dict[str, RowData]: ...


class CsvDataReader(DataReader):
    def read_files(self, filenames: list[str]) -> dict[str, RowData]:
        files_data = {}
        for filename in filenames:
            lines = self._read_csv(filename)
            header = self._normalize_header(lines[0])
            files_data.update(self._parse_rows(header, lines[1:]))
        return files_data

    def _read_csv(self, filename: str) -> list[list[str]]:
        try:
            with open(filename) as f:
                return [line.strip("\n").split(",") for line in f]
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")

    def _normalize_header(self, header: list[str]) -> list[str]:
        return [
            "rate" if field in POSSIBLE_SALARY_NAMES else field
            for field in header
        ]

    def _parse_rows(
        self,
        header: list[str],
        rows: list[list[str]]
    ) -> dict[str, RowData]:
        try:
            id_idx = header.index("id")
            email_idx = header.index("email")
            name_idx = header.index("name")
            dept_idx = header.index("department")
            hours_idx = header.index("hours_worked")
            rate_idx = header.index("rate")
        except ValueError as e:
            raise ValueError(f"Обязательная колонка не найдена: {e}") from None

        data = {}
        for row in rows:
            row_id = row[id_idx]
            data[row_id] = RowData(
                rate=int(row[rate_idx]),
                hours_worked=int(row[hours_idx]),
                email=row[email_idx],
                name=row[name_idx],
                department=row[dept_idx],
            )
        return data
