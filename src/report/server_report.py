from typing import Any, Union, Dict
from datetime import datetime
import re
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def _parse_memory_data(memory: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    if isinstance(memory, dict):
        return memory

    total_match = re.search(r"Total memory:\s*([\d\.]+)GB", str(memory))
    used_match = re.search(r"Used:\s*([\d\.]+)GB", str(memory))
    free_match = re.search(r"Free:\s*([\d\.]+)(?:MB|GB)", str(memory))
    aval_match = re.search(r"Available:\s*([\d\.]+)GB", str(memory))

    total_gb = float(total_match.group(1)) if total_match else 16.0
    used_gb = float(used_match.group(1)) if used_match else 8.0
    free_val = float(free_match.group(1)) if free_match else 1.0
    free_gb = free_val / 1024.0 if "MB" in str(memory) else free_val
    available_gb = float(aval_match.group(1)) if aval_match else max(0.0, total_gb - used_gb)

    buff_cache_gb = max(0.0, round(total_gb - (used_gb + free_gb), 2))

    return {
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "buff_cache_gb": buff_cache_gb,
        "available_gb": round(available_gb, 2),
        "used_pct": round((used_gb / total_gb) * 100, 1) if total_gb else 0.0,
        "free_pct": round((free_gb / total_gb) * 100, 1) if total_gb else 0.0,
    }


def _parse_users_data(users: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    if isinstance(users, dict):
        return users

    total_users_match = re.search(r"Total users logged:\s*(\d+)", str(users))
    total_users = int(total_users_match.group(1)) if total_users_match else 0
    uptime_match = re.search(r"Uptime:\s*([^|]+)", str(users))
    load_match = re.search(r"Load:\s*(.*)", str(users))

    return {
        "total_users": total_users,
        "uptime": uptime_match.group(1).strip() if uptime_match else "N/A",
        "load_average": load_match.group(1).strip() if load_match else "N/A",
        "headers": ["USER", "TTY", "FROM", "LOGIN@", "IDLE", "JCPU", "PCPU", "WHAT"],
        "sessions": [],
    }


# Dracula Theme Palette
DRACULA_BG = "#282A36"
DRACULA_CURRENT = "#44475A"
DRACULA_FG = "#F8F8F2"
DRACULA_COMMENT = "#6272A4"
DRACULA_CYAN = "#8BE9FD"
DRACULA_GREEN = "#50FA7B"
DRACULA_ORANGE = "#FFB86C"
DRACULA_PINK = "#FF79C6"
DRACULA_PURPLE = "#BD93F9"
DRACULA_RED = "#FF5555"


def generate_report(
    memory: Union[Dict[str, Any], str],
    users: Union[Dict[str, Any], str],
    output_path: str = "server_report.png",
    show: bool = False,
) -> str:
    logger.info("Preparing server status report visualization")
    mem_data = _parse_memory_data(memory)
    usr_data = _parse_users_data(users)

    fig = plt.figure(figsize=(14, 7), facecolor=DRACULA_BG)
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.25)

    ax_mem = fig.add_subplot(gs[0])
    ax_usr = fig.add_subplot(gs[1])

    # Header
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    fig.suptitle(
        "Server Status Report",
        fontsize=20,
        fontweight="bold",
        color=DRACULA_FG,
        y=0.97,
    )
    fig.text(
        0.5,
        0.91,
        f"Generated on {timestamp}",
        ha="center",
        fontsize=11,
        color=DRACULA_COMMENT,
    )

    # --- LEFT PANEL: Memory Distribution ---
    ax_mem.set_facecolor(DRACULA_BG)
    total_gb = mem_data.get("total_gb", 0)
    used_gb = mem_data.get("used_gb", 0)
    buff_cache_gb = mem_data.get("buff_cache_gb", mem_data.get("buff_cache_mb", 0) / 1024)
    free_gb = mem_data.get("free_gb", 0)
    avail_gb = mem_data.get("available_gb", 0)

    labels = ["Used", "Buffer / Cache", "Free"]
    values = [max(0.01, used_gb), max(0.01, buff_cache_gb), max(0.01, free_gb)]
    colors = [DRACULA_RED, DRACULA_PURPLE, DRACULA_GREEN]

    wedges, texts, autotexts = ax_mem.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=140,
        colors=colors,
        textprops={"fontsize": 10, "color": DRACULA_FG, "fontweight": 400},
        wedgeprops={"width": 0.38, "edgecolor": DRACULA_BG, "linewidth": 2.5},
    )

    for autotext in autotexts:
        autotext.set_color(DRACULA_BG)
        autotext.set_fontweight("bold")
        autotext.set_fontsize(10)

    ax_mem.text(
        0,
        0.05,
        f"{total_gb:.1f} GB",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
        color=DRACULA_FG,
    )
    ax_mem.text(
        0,
        -0.12,
        "Total RAM",
        ha="center",
        va="center",
        fontsize=10,
        color=DRACULA_COMMENT,
    )

    ax_mem.set_title("Memory Allocation", fontsize=14, fontweight="bold", color=DRACULA_CYAN, pad=14)

    mem_details = (
        f"Available: {avail_gb:.2f} GB   |   Used: {used_gb:.2f} GB   |   Free: {free_gb:.2f} GB"
    )
    ax_mem.text(
        0,
        -1.28,
        mem_details,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=DRACULA_FG,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=DRACULA_CURRENT, edgecolor=DRACULA_COMMENT, linewidth=1),
    )

    # --- RIGHT PANEL: Users & Host Activity ---
    ax_usr.set_facecolor(DRACULA_BG)
    ax_usr.axis("off")
    ax_usr.set_title("Active Users & Host Activity", fontsize=14, fontweight="bold", color=DRACULA_CYAN, pad=14)

    total_users = usr_data.get("total_users", 0)
    uptime = usr_data.get("uptime", "N/A")
    load_avg = usr_data.get("load_average", "N/A")
    sessions = usr_data.get("sessions", [])
    headers = usr_data.get("headers", [])

    kpi_y = 0.88
    ax_usr.text(
        0.02,
        kpi_y,
        f"Active Users\n{total_users}",
        ha="left",
        va="top",
        fontsize=11,
        fontweight="bold",
        color=DRACULA_FG,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=DRACULA_CURRENT, edgecolor=DRACULA_CYAN, linewidth=1.5),
    )
    ax_usr.text(
        0.40,
        kpi_y,
        f"Uptime\n{uptime}",
        ha="left",
        va="top",
        fontsize=11,
        fontweight="bold",
        color=DRACULA_FG,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=DRACULA_CURRENT, edgecolor=DRACULA_ORANGE, linewidth=1.5),
    )
    ax_usr.text(
        0.72,
        kpi_y,
        f"Load Average\n{load_avg}",
        ha="left",
        va="top",
        fontsize=11,
        fontweight="bold",
        color=DRACULA_FG,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=DRACULA_CURRENT, edgecolor=DRACULA_PINK, linewidth=1.5),
    )

    if sessions:
        cols_to_show = ["USER", "TTY", "FROM", "LOGIN@", "IDLE"]
        header_map = {h: i for i, h in enumerate(headers)}
        table_headers = [c for c in cols_to_show if c in header_map] or headers[:6]

        table_data = []
        for sess in sessions[:8]:
            row = []
            for col in table_headers:
                idx = header_map.get(col)
                if idx is not None and idx < len(sess):
                    val = sess[idx]
                    row.append(val)
                else:
                    row.append("")
            table_data.append(row)

        table = ax_usr.table(
            cellText=table_data,
            colLabels=table_headers,
            loc="center",
            bbox=[0.02, 0.05, 0.96, 0.65],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        for (row_idx, col_idx), cell in table.get_celld().items():
            cell.set_edgecolor(DRACULA_COMMENT)
            if row_idx == 0:
                cell.set_facecolor(DRACULA_PURPLE)
                cell.get_text().set_color(DRACULA_BG)
                cell.get_text().set_fontweight("bold")
                cell.set_height(0.12)
            else:
                cell.set_facecolor(DRACULA_CURRENT if row_idx % 2 == 0 else DRACULA_BG)
                cell.get_text().set_color(DRACULA_FG)
                cell.set_height(0.10)
    else:
        ax_usr.text(
            0.5,
            0.40,
            "No active interactive user sessions\n\nAll server resources are available",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=DRACULA_GREEN,
            bbox=dict(boxstyle="round,pad=1.0", facecolor=DRACULA_CURRENT, edgecolor=DRACULA_COMMENT, linewidth=1.5),
        )

    plt.subplots_adjust(top=0.85, bottom=0.1)

    logger.info("Saving status report image to %s", output_path)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())

    if show:
        plt.show()
    else:
        plt.close(fig)

    return output_path