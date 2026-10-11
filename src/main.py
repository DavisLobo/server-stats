from analysis import check_users, check_memory
from report import generate_report
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s', datefmt='%d/%m/%Y', level=logging.INFO)

def main() -> None:
    logger.info("Pipeline started")
    memoryData = check_memory()
    logger.info("Memory checked")
    usersData = check_users()
    logger.info("Users checked")
    report_path = generate_report(memoryData, usersData)
    logger.info("Report generated at: %s", report_path)

if __name__ == "__main__":
    main()
