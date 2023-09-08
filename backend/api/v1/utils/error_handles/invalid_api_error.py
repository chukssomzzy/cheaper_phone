#!/usr/bin/env vevn/bin/activate
"""Defines class to handle all error request error"""


class InvalidApiUsage(Exception):
    """InvalidApiUsage class definition"""
    status_code = 400
    payload = None

    def __init__(self, message, status_code=None, payload=None):
        """Initialize InvalidApiUsage"""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Get serializable error message"""
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv
