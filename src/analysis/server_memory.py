from typing import Dict, Any
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def check_memory() -> Dict[str, Any]:
    result = subprocess.run(["free", "-t", "-m"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    mem_row = lines[1].split()
    values = list(map(int, mem_row[1:7]))
    tot_m, used_m, free_m, shared_m, buff_m, aval_m = values

    summary = (
        f"Total memory: {tot_m/1024:.2f}GB\n"
        f"Used: {used_m/1024:.2f}GB Free: {free_m}MB\n"
        f"Available: {aval_m/1024:.2f}GB"
    )

    data = {
        "total_mb": tot_m,
        "used_mb": used_m,
        "free_mb": free_m,
        "shared_mb": shared_m,
        "buff_cache_mb": buff_m,
        "available_mb": aval_m,
        "total_gb": round(tot_m / 1024, 2),
        "used_gb": round(used_m / 1024, 2),
        "free_gb": round(free_m / 1024, 2),
        "available_gb": round(aval_m / 1024, 2),
        "used_pct": round((used_m / tot_m) * 100, 1) if tot_m else 0.0,
        "free_pct": round((free_m / tot_m) * 100, 1) if tot_m else 0.0,
        "summary": summary,
    }
    return data