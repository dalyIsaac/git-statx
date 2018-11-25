#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE
from datetime import datetime


def main():
    print("Current working directory: " + os.getcwd())
    # log_path = input("Enter the log path: ")
    log_path = "c:/Users/isaac/Source/Repos/log.csv"
    length = diff_month(last_commit_date(), first_commit_date()) + 1
    stats = {}
    get_git_log(log_path, length, stats)


def get_git_log(log_path, length, stats):
    with open(log_path, "w", encoding="utf-8") as file:
        proc = Popen(
            ["git", "log", "--pretty=format:[%cd]", "--numstat"],
            stdout=PIPE,
            stderr=PIPE,
        )
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            else:
                print(line)
                file.writelines(line.decode("utf-8"))


def first_commit_date():
    proc = Popen(
        ["git", "log", "--reverse", "--pretty=format:%cd"], stdout=PIPE, stderr=PIPE
    )
    date_byte_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = datetime.strptime(date_byte_str.strip(), "%c %z")
    return date


def last_commit_date():
    proc = Popen(["git", "log", "--pretty=format:%cd"], stdout=PIPE, stderr=PIPE)
    date_byte_str = proc.stdout.readline().decode("utf-8")
    proc.kill()
    date = datetime.strptime(date_byte_str.strip(), "%c %z")
    return date


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


if __name__ == "__main__":
    main()
