#!/usr/bin/env python3
import sys
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
from calendar import month_abbr
import calendar
import time
import csv


try:
    input = raw_input
except Exception:
    pass


def main():
    start = time.time()
    log_path = input("Enter the log path: ").strip()

    with open(log_path, "w") as file:
        pass

    print("\nReading git log:")

    first_commit_date = get_first_or_last_commit_date()
    last_commit_date = get_first_or_last_commit_date(first=False)
    length = diff_month(last_commit_date, first_commit_date) + 1

    lines_added = {}
    lines_deleted = {}
    num_commits = {}

    max_dir_depth = get_git_log(length, lines_added, lines_deleted, num_commits)
    end = time.time()

    print("\nWriting to " + log_path)
    write_to_csv(
        log_path,
        first_commit_date,
        last_commit_date,
        lines_added,
        lines_deleted,
        num_commits,
        max_dir_depth,
    )
    print("\nTime taken: {0:.2f} seconds\n".format(end - start))


def get_git_log(length, lines_added, lines_deleted, num_commits):
    proc = Popen(
        ["git", "log", "--reverse", "--pretty=format:[%cd]", "--numstat"],
        stdout=PIPE,
        stderr=PIPE,
    )
    counter = 0
    date = None
    prev_date = None
    max_dir_depth = 0

    while True:
        line_b = proc.stdout.readline()

        if not line_b and date:
            print("{}-{}".format(month_abbr[date.month], date.year))
            return max_dir_depth
        elif not line_b:
            return max_dir_depth

        line = line_b.decode("utf-8").strip()

        if line == "":
            pass
        elif line[0] == "[":
            date = get_date(line[1:-1])
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
                dir_depth = len(filename.split("/"))
                if dir_depth > max_dir_depth:
                    max_dir_depth = dir_depth

            lines_added[filename][counter] += (
                int(added_str) if added_str.isdigit() else 1
            )
            lines_deleted[filename][counter] += (
                int(deleted_str) if deleted_str.isdigit() else 1
            )
            num_commits[filename][counter] += 1


def get_first_or_last_commit_date(first=True):
    args = []
    if first:
        args = ["git", "log", "--reverse", "--pretty=format:%cd"]
    else:
        args = ["git", "log", "--pretty=format:%cd"]
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    date_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = get_date(date_str)
    return date


def get_date(date_str):
    """Hard coded to en_US since Python 2 can't deal with dates well without importing other modules"""
    date_l = date_str.split(" ")
    date_u = " ".join(date_l[:-1])
    date_s = str(date_u)
    date = datetime.strptime(date_s, "%a %b %d %H:%M:%S %Y")
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
    max_dir_depth,
):
    log_file = None
    if sys.version_info[0] < 3:
        log_file = open(log_path, "wb")
    else:
        log_file = open(log_path, "w", newline="")

    filewriter = csv.writer(log_file, dialect="excel")

    header = ["File name", "File extension", "Statistic"]
    date = first_commit_date
    while date <= last_commit_date:
        header.append("{}-{}".format(month_abbr[date.month], date.year))
        date = add_months(date, 1)
    header += ["Dir{}".format(i) for i in range(max_dir_depth - 1)]
    filewriter.writerow(header)

    for key in lines_added.keys():
        path = key.split("/")
        dirs = path[:-1]
        file_ext = key.split(".")[-1]
        file_name = "".join(path[-1].split(".")[:-1])
        filewriter.writerow([file_name, file_ext, "lines added"] + lines_added[key] + dirs)
        filewriter.writerow(
            [file_name, file_ext, "lines deleted"] + lines_deleted[key] + dirs
        )
        filewriter.writerow([file_name, file_ext, "number commits"] + num_commits[key] + dirs)

    log_file.close()


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day)


if __name__ == "__main__":
    main()
