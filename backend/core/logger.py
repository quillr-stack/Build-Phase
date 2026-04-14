import logging
import json
import sys
import os
from datetime import datetime
from backend.core import config

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "layer": getattr(record, "layer", "unknown"),
            "run_id": getattr(record, "run_id", "none"),
            "event": record.msg,
            "data": getattr(record, "data", {})
        }
        return json.dumps(log_entry)

def setup_logger():
    logger = logging.getLogger("sattva")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(JSONFormatter())
    logger.addHandler(ch)

    return logger

logger = setup_logger()

def log(run_id, layer, event, data=None):
    extra = {"run_id": run_id, "layer": layer, "data": data or {}}
    logger.info(event, extra=extra)

    # Also append to ./data/logs/{run_id}.jsonl if run_id is provided
    if run_id and run_id != "none":
        log_dir = "/data/logs" if os.path.exists("/data/logs") else "./data/logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{run_id}.jsonl")
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "layer": layer,
            "event": event,
            "data": data or {}
        }
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            # Fallback if file writing fails
            logger.error(f"Failed to write to log file: {e}")
