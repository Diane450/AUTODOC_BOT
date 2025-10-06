import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s %(name)s %(message)s %(lineno)d"
)

logger = logging.getLogger(__name__)
    