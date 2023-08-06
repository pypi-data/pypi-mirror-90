import string
from typing import Optional, Union


def byte_conv(val):  # noqa
    try:
        return parse_str(val.decode())
    except UnicodeDecodeError:
        return val
    # return val.decode('utf-8')


def parse_str(x: str):
    """
    Converts a string to either an int, float, or str depending on its value.
    :param x:   String to convert
    :return:    int, float, or str
    """
    if isinstance(x, str):
        return x.isalpha() and x or x.isdigit() and \
               int(x) or x.isalnum() and x or \
               len(set(string.punctuation).intersection(x)) == 1 and \
               x.count('.') == 1 and float(x) or x
    return x


# # TODO: UNTESTED
# def split_fullname(fullname: str, default: str = '',
#                    prefix: Optional[Union[str, list]] = None,
#                    suffix: Optional[Union[str, list]] = None):
#     """
#     Splits a fullname into their respective first_name and last_name fields.
#     If only one name is given, that becomes the first_name
#     :param fullname:    The name to split
#     :param default:     The value if only one name is given
#     :param prefix:      Custom prefixes to append to the default list
#     :param suffix:      Custom suffixes to append to the default list
#     :return:
#     """
#     if not isinstance(fullname, str):
#         raise TypeError(_('`fullname` must be of type str.'))
#
#     if prefix and not isinstance(prefix, (str, list)):
#         raise TypeError(_('`prefix` must be a list/str for multi/single values.'))
#
#     if suffix and not isinstance(suffix, (str, list)):
#         raise TypeError(_('`suffix` must be a list/str for multi/single values.'))
#
#     prefix = isinstance(prefix, str) and [prefix] or prefix
#     suffix = isinstance(suffix, str) and [suffix] or suffix
#     PREFIX_TO_NAMES = ['dos', 'de', 'delos', 'san', 'dela', 'dona'] + prefix
#     SUFFIX_TO_NAMES = ['phd', 'md'] + suffix
#
#     list_ = fullname.split()
#     lastname_idx = None
#     if len(list_) > 2:
#         for idx, val in enumerate(list_):
#             if val.lower() in PREFIX_TO_NAMES:
#                 lastname_idx = idx
#                 break
#             elif val.lower().replace('.', '') in SUFFIX_TO_NAMES:
#                 lastname_idx = idx - 1
#             else:
#                 if idx == len(list_) - 1:
#                     lastname_idx = idx
#                 else:
#                     continue
#         list_[:lastname_idx] = [' '.join(list_[:lastname_idx])]
#         list_[1:] = [' '.join(list_[1:])]
#     try:
#         first, last = list_
#     except ValueError:
#         first, last = [*list_, default]
#     return first, last