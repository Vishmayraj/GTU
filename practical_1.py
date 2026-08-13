#  To Load and Explore the Unstructured Access Log Data
#  Objective: Learn how to import and explore raw server access logs (Apache/Nginx 
#  format).
#  ● Load a sample access.log file using Python (e.g., with open() or pandas + regex).
#  ● Understand the typical log structure (IP, timestamp, request, status, size, user
#    agent,etc.).
#  ● Extract 5–10 random lines to manually inspect the pattern.
#  ● Identify useful fields for analysis.

import random


with open('access.log', 'r') as file:
    log_lines = file.readlines()

print("Total number of log lines:", len(log_lines))

print("\nFirst Log Entry:")
print(log_lines[0])

# Display useful fields
print("\nUseful Fields in Access Logs:")
print("1. IP Address         TimeStamp                 HTTP Request             HTTP Status Code         Response Size         Referrer         User Agent")

# Printing 5 random log entries to inspect the pattern
random_logs = random.sample(log_lines, 5)
print("\nRandom Log Entries:")
for log_lines in random_logs:
    print(log_lines.strip()) #strip removes unecessary whitespace characters from the beginning and end of the string