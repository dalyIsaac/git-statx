#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
from calendar import month_abbr
import time
import csv


DATETIME_FORMAT = "%c %z"


def main():
    start = time.time()
    print("Current working directory: " + os.getcwd())
    log_path = input("Enter the log path: ")

    with open(log_path) as file:
        pass

    print("\nReading git log:")

    first_commit_date = get_first_commit_date()
    last_commit_date = get_last_commit_date()
    length = diff_month(last_commit_date, first_commit_date) + 1

    lines_added = {}
    lines_deleted = {}
    num_commits = {}

    get_git_log(length, lines_added, lines_deleted, num_commits)
    end = time.time()

    print("\nWriting to " + log_path)
    write_to_csv(
        log_path,
        first_commit_date,
        last_commit_date,
        lines_added,
        lines_deleted,
        num_commits,
    )
    print("\nTime taken: {0:.2f} seconds".format(end - start), end="\n\n")


def get_git_log(length, lines_added, lines_deleted, num_commits):
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

        if not line_b and date:
            print("{} {}".format(date.year, month_abbr[date.month]))
            return
        elif not line_b:
            return

        line = line_b.decode("utf-8").strip()

        if line == "":
            pass
        elif line[0] == "[":
            date = datetime.strptime(line[1:-1], DATETIME_FORMAT)
            date = datetime(year=date.year, month=date.month, day=1)
            if prev_date and prev_date < date:
                print("{}-{}".format(month_abbr[prev_date.month], prev_date.year))
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


def get_first_commit_date():
    proc = Popen(
        ["git", "log", "--reverse", "--pretty=format:%cd"], stdout=PIPE, stderr=PIPE
    )
    date_byte_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = datetime.strptime(date_byte_str.strip(), DATETIME_FORMAT)
    date = datetime(year=date.year, month=date.month, day=1)
    return date


def get_last_commit_date():
    proc = Popen(["git", "log", "--pretty=format:%cd"], stdout=PIPE, stderr=PIPE)
    date_byte_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = datetime.strptime(date_byte_str.strip(), DATETIME_FORMAT)
    date = datetime(year=date.year, month=date.month, day=1)
    return date


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def write_to_csv(
    log_path,
    first_commit_date,
    last_commit_date,
    lines_added,
    lines_deleted,
    num_commits,
):
    with open(log_path, "w", encoding="utf-8", newline="") as file:
        filewriter = csv.writer(file, dialect="excel")

        header = ["File", "Statistic"]
        while first_commit_date <= last_commit_date:
            header.append(
                "{}-{}".format(
                    month_abbr[first_commit_date.month], first_commit_date.year
                )
            )
            first_commit_date = first_commit_date + timedelta(weeks=4)
        filewriter.writerow(header)

        for key in lines_added.keys():
            filewriter.writerow([key, "lines added"] + lines_added[key])
            filewriter.writerow([key, "lines deleted"] + lines_deleted[key])
            filewriter.writerow([key, "number commits"] + num_commits[key])


if __name__ == "__main__":
    main()
