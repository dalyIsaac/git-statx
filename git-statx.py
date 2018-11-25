#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE
from datetime import datetime
from calendar import month_name
import time


DATETIME_FORMAT = "%c %z"


def main():
    start = time.time()
    print("Current working directory: " + os.getcwd())
    # log_path = input("Enter the log path: ")
    log_path = "c:/Users/isaac/Source/Repos/log.csv"
    length = diff_month(last_commit_date(), first_commit_date()) + 1

    lines_added = {}
    lines_deleted = {}
    num_commits = {}

    get_git_log(log_path, length, lines_added, lines_deleted, num_commits)
    end = time.time()
    print(end - start)


def get_git_log(log_path, length, lines_added, lines_deleted, num_commits):
    with open(log_path, "w", encoding="utf-8") as file:
        proc = Popen(
            ["git", "log", "--reverse", "--pretty=format:[%cd]", "--numstat"],
            stdout=PIPE,
            stderr=PIPE,
        )
        counter = 0
        date = None
        prev_date = None

        while True:
            line_b = proc.stdout.readline()

            if not line_b:
                return

            line = line_b.decode("utf-8").strip()

            if line == "":
                pass
            elif line[0] == "[":
                date = datetime.strptime(line[1:-1], DATETIME_FORMAT)
                date = datetime(year=date.year, month=date.month, day=1)
                if prev_date and prev_date < date:
                    print("{} {}".format(prev_date.year, month_name[prev_date.month]))
                    counter += 1
                    prev_date = date
                elif not prev_date:
                    prev_date = date
            else:
                added_str, deleted_str, filename = line.split("\t")
                filename = filename.strip()

                if filename not in lines_added:
                    lines_added[filename] = [0] * length
                    lines_deleted[filename] = [0] * length
                    num_commits[filename] = [0] * length

                lines_added[filename][counter] += (
                    int(added_str) if added_str.isdigit() else 1
                )
                lines_deleted[filename][counter] += (
                    int(deleted_str) if deleted_str.isdigit() else 1
                )
                num_commits[filename][counter] += 1


def first_commit_date():
    proc = Popen(
        ["git", "log", "--reverse", "--pretty=format:%cd"], stdout=PIPE, stderr=PIPE
    )
    date_byte_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = datetime.strptime(date_byte_str.strip(), DATETIME_FORMAT)
    date = datetime(year=date.year, month=date.month, day=1)
    return date


def last_commit_date():
    proc = Popen(["git", "log", "--pretty=format:%cd"], stdout=PIPE, stderr=PIPE)
    date_byte_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = datetime.strptime(date_byte_str.strip(), DATETIME_FORMAT)
    date = datetime(year=date.year, month=date.month, day=1)
    return date


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


if __name__ == "__main__":
    main()
