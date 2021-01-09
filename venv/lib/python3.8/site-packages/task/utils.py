import sqlite3
import os
import datetime
from dateutil.parser import parse
from typing import Tuple, List
from pathlib import Path

database = "task.db"


def format_current_time() -> str:
    date = str(datetime.datetime.now())
    return date.split(".")[0]


def does_db_exist() -> Tuple[bool, bool]:
    """Check if database exists."""
    global database
    prod_path = f"{os.getenv('HOME')}/.task.db"

    if Path("task.db").exists():
        db = True
        is_prod = False
    elif Path(prod_path).exists():
        db, is_prod = True, True
        database = prod_path
    else:
        db, is_prod = False, False
    return db, is_prod


def create_db():
    """Create SQlite3 database."""
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE todo (
                 id INTEGER PRIMARY KEY,
                 project TEXT,
                 task TEXT NOT NULL,
                 urgency INT NOT NULL,
                 due DATE,
                 done BOOLEAN DEFAULT FALSE,
                 created_at TEXT NOT NULL,
                 updated_at TEXT NOT NULL)
        """
    )
    conn.commit()
    conn.close()


def insert_to_db(task_data: dict):
    """Insert task into DB."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    for data in task_data:
        if task_data[data] is None:
            task_data[data] = ""

    if task_data["urgency"] == "":
        task_data["urgency"] = 0

    """Workaround until I find a way
    to espace the quote character.
    """
    if "'" in task_data["task"]:
        task_data["task"] = task_data["task"].replace("'", " ")

    query = "INSERT INTO todo (project, task, urgency, due, created_at, updated_at) \
             VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
        task_data["project"],
        task_data["task"],
        task_data["urgency"],
        task_data["due"],
        task_data["created_at"],
        task_data["updated_at"],
    )
    cursor.execute(query)
    conn.commit()
    conn.close()


def list_tasks(what: str = None) -> List:
    """Select all tasks."""
    task_list = list()
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if what == "done":
        query = "SELECT id, project, task, urgency, due, created_at \
                 FROM todo WHERE done = True ORDER by id"
    elif what == "all":
        query = "SELECT id, project, task, urgency, due, created_at \
                 FROM todo ORDER by id"
    else:
        query = "SELECT id, project, task, urgency, due, created_at \
                 FROM todo WHERE done = False ORDER by id"
    out = cursor.execute(query)
    for task in out:
        task_list.append(task)
    return task_list


def get_one_task(task_id: int = None) -> List:
    """Grab one task."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if task_id is None:
        query = "SELECT * FROM todo where id = (select MAX(id) from TODO);"
    else:
        query = f"SELECT * FROM todo WHERE id = {task_id}"
    out = cursor.execute(query).fetchall()
    if len(out) == 0:
        return None
    return out


def remove_entry(task_id: int):
    """Remove row."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = f"DELETE FROM todo WHERE id={task_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()


def update_task(task_id: int = 0):
    """Updated task date."""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = f"UPDATE TODO SET updated_at='{format_current_time()}' \
              WHERE id={task_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()


def set_task_done(task_id: int = 0, project: str = None):
    """Set task to done."""
    # TODO : if 0 move latest task
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if task_id == 0:
        query = "UPDATE TODO SET done = True WHERE id > 0"
    else:
        query = f"UPDATE TODO SET done = True WHERE id={task_id}"

    cursor.execute(query)
    conn.commit()
    conn.close()

    return task_id


def parse_due(due: str = None) -> str:
    if due is None:
        return None

    today = datetime.date.today()
    when = due.lower()
    due_date = None

    # check if it's a date format
    try:
        due_date = parse(when)
    except ValueError:
        pass

    if when == "tomorrow":
        due_date = today + datetime.timedelta(days=1)
    elif when.find("day") != -1:
        number = int(when.split()[0])
        due_date = today + datetime.timedelta(days=number)
    elif when.find("month") != 1:
        number = int(when.split()[0])
        due_date = today + datetime.timedelta(days=(number * 31))
    elif when.find("year") != 1:
        number = int(when.split()[0])
        due_date = today + datetime.timedelta(days=(number * 365))
    else:
        pass
    return str(due_date)
