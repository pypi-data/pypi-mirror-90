# -*- coding: utf-8 -*-
# Copyright (C) 2020 N. Malkin
# SPDX-License-Identifier: BSD-3-Clause

import logging

try:
    import colorlog

    use_colors = True

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt="%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

except ModuleNotFoundError:
    use_colors = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

handler.setLevel(logging.DEBUG)


def getLogger(name) -> logging.Logger:
    if use_colors:
        logger = colorlog.getLogger(name)
    else:
        logger = logging.getLogger(name)

    logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)

    return logger
