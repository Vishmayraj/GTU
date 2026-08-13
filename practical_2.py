import re
import pandas as pd

# Step 1: Open the access log file
with open("access.log", "r") as file:
    log_lines = file.readlines()

print("Total log entries:", len(log_lines))


# | Regex   | Meaning               |
# | ------- | --------------------- |
# | `.`     | Any character         |
# | `\d`    | Any digit             |
# | `\D`    | Any non-digit         |
# | `\w`    | Word character        |
# | `\W`    | Non-word character    |
# | `\s`    | Whitespace            |
# | `\S`    | Non-whitespace        |
# | `+`     | One or more           |
# | `*`     | Zero or more          |
# | `?`     | Zero or one           |
# | `{n}`   | Exactly n times       |
# | `{n,m}` | Between n and m times |
# | `[]`    | Character set         |
# | `[^]`   | Not these characters  |
# | `()`    | Capturing group       |
# | `^`     | Beginning             |
# | `$`     | End                   |
# | `\.`    | Literal dot           |
# | `\[`    | Literal `[`           |
# | `\]`    | Literal `]`           |


# Step 2: Define the regular expression
pattern = r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) ([^"]+)" (\d+) (\d+) "([^"]*)" "([^"]*)"'

# Step 3: Create an empty list to store structured records
data = []

# Step 4: Parse each log line
for line in log_lines:

    match = re.search(pattern, line)

    if match:
        data.append({
            "IP Address": match.group(1),
            "Date/Time": match.group(2),
            "Request Type": match.group(3),
            "Resource": match.group(4),
            "Protocol": match.group(5),
            "Status Code": int(match.group(6)),
            "Bytes Sent": int(match.group(7)),
            "Referrer": match.group(8),
            "User Agent": match.group(9)
        })

# Step 5: Convert the structured data into a DataFrame
df = pd.DataFrame(data)

# Step 6: Display the DataFrame
print("\nStructured Dataset:\n")
print(df)

# Step 7: Display basic information
print("\nDataFrame Information:\n")
print(df.info())