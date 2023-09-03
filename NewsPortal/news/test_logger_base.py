import logging

django_logger = logging.getLogger("django")
django_request_logger = logging.getLogger("django.request")
django_server_logger = logging.getLogger("django.server")
django_template_logger = logging.getLogger("django.template")
django_db_backends_logger = logging.getLogger("django.db.backends")
django_security_logger = logging.getLogger("django.security")

loggers = [
    django_logger,
    django_request_logger,
    django_server_logger,
    django_template_logger,
    django_db_backends_logger,
    django_security_logger,
]


def check_logger(logger):
    logger.debug(f"{logger.name} : DEBUG")
    logger.info(f"{logger.name} : INFO")
    logger.warning(f"{logger.name} : WARNING")
    logger.error(f"{logger.name} : ERROR")
    logger.critical(f"{logger.name} : CRITICAL")

def check_loggers():
    for curr_logger in loggers:
        check_logger(curr_logger)