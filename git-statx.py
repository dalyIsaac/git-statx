#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE

print("Current working directory: " + os.getcwd())
# log_path = input("Enter the log path: ")
log_path = "/mnt/c/Users/isaac/Source/Repos/log.csv"

with open(log_path, "w", encoding="utf-8") as file:
    proc = Popen(
        ["git", "log", "--pretty=format:[%cd]", "--numstat"], stdout=PIPE, stderr=PIPE
    )
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        else:
            print(line)
            file.writelines(line.decode("utf-8"))
