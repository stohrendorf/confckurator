import logging
from logging import StreamHandler

import sys
from flask import request

audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)
audit_logger.addHandler(StreamHandler(sys.stdout))


def audit_log(msg, *args, **kwargs):
    try:
        address = request.remote_addr
    except RuntimeError:
        address = '<unknown>'
    audit_logger.info('[remote {}] {}'.format(address, msg).format(*args), **kwargs)
