# -*- coding: utf-8 -*-
import copy


def _replace_list(source, target, by, dict_replacer):
    for i in range(len(source)):
        if source[i] == target:
            source[i] = by
        if isinstance(source[i], dict):
            dict_replacer(source[i], target=target, by=by, deep_copy=False)
        if isinstance(source[i], list):
            _replace_list(source[i], target, by, dict_replacer)


def replace(source, target='', by=None, deep_copy=True):

    result = source
    if deep_copy:
        result = copy.deepcopy(source)

    for k, v in result.items():
        if isinstance(v, dict):
            replace(v, target=target, by=by, deep_copy=False)

        if isinstance(v, list):
            _replace_list(v, target, by, replace)

        if v == target:
            result[k] = by

    return result

