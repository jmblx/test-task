import pytest

@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / "data.csv"
    file_path.write_text(
        """
id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60
4,grace@example.com,Grace Lee,HR,160,45
        """.strip()
    )
    return str(file_path)
