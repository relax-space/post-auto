
import logging
import os

logging.basicConfig(level=os.getenv('log_level', logging.INFO),
                    format="%(asctime)s - %(levelname)s - %(message)s")
