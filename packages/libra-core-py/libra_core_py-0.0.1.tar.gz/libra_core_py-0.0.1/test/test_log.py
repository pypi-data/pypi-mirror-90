from libra_core.log import *


def test_log_info():
    log_init_config("/tmp", "spider")
    log_info("test log info")


def test_log_warn():
    log_init_config("/tmp", "spider")
    log_warn("test log warn")


def test_log_error():
    log_init_config("/tmp", "spider")
    log_error("test log error")


def test_log_debug():
    log_init_config("/tmp", "spider")
    log_debug("test log debug")


def test_log_exception():
    log_init_config("/tmp", "spider")
    try:
        print(1 / 0)
    except Exception as ex:
        log_exception(ex, "print failed")
