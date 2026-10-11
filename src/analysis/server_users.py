from typing import Dict, Any
import subprocess
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def check_users() -> Dict[str, Any]:
    result = subprocess.run(["w"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    first_line = lines[0] if lines else ""
    user_match = re.search(r"(\d+)\s+users?", first_line)
    uptime_match = re.search(r"up\s+(.*?),\s*\d+\s+user", first_line)
    load_match = re.search(r"load average:\s*(.*)", first_line)

    uptime = uptime_match.group(1).strip() if uptime_match else "N/A"
    load_avg = load_match.group(1).strip() if load_match else "N/A"

    header_line = lines[1] if len(lines) > 1 else ""
    raw_sessions = lines[2:] if len(lines) > 2 else []

    headers = []
    col_spans = []
    if header_line:
        matches = list(re.finditer(r"\S+", header_line))
        headers = [m.group() for m in matches]
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else None
            col_spans.append((m.group(), start, end))

    sessions = []
    for line in raw_sessions:
        if line.strip():
            if col_spans:
                cols = []
                for _, start, end in col_spans:
                    if start < len(line):
                        val = line[start:end].strip() if end else line[start:].strip()
                    else:
                        val = ""
                    cols.append(val)
                sessions.append(cols)
            else:
                sessions.append(line.split())

    total_users = int(user_match.group(1)) if user_match else len(sessions)

    summary = (
        f"{' '.join(headers)}\n"
        f"{sessions}\n"
        f"Total users logged: {total_users}\n"
        f"Uptime: {uptime} | Load: {load_avg}"
    )

    data = {
        "total_users": total_users,
        "uptime": uptime,
        "load_average": load_avg,
        "headers": headers,
        "sessions": sessions,
        "summary": summary,
    }
    return data
