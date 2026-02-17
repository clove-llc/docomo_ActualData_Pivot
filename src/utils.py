from pathlib import Path


def load_sql(file_name: str) -> str:
    sql_path = Path(__file__).parent / "sql" / file_name
    return sql_path.read_text(encoding="utf-8")
