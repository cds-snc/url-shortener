import os
import logzero


LOG_LEVEL = int(os.environ.get("LOG_LEVEL", logzero.INFO))


logzero.json()

log = logzero.logger
log.setLevel(LOG_LEVEL)
