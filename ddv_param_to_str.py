#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict


def arg_to_str(user_data: Dict[str, str]) -> str:
    """
    Takes the user_data object, strips context into a list
    :param user_data:
    :return: Formated key-pair
    """
    arg = list()

    for key, value in user_data.items():
        arg.append(f'{key} = {value}')

    return "\n".join(arg).join(['\n', '\n'])
