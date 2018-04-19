# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from decimal import Decimal, getcontext, ROUND_DOWN

def decimal_split(decimal):
    #Splits a Decimal object into fractional and integer parts, returned as Decimal
    integer_part, fractional_part = getcontext().divmod(decimal, 1)

    return (fractional_part, integer_part)

def decimal_truncate(decimal, places):
    #https://stackoverflow.com/a/41523702
    return decimal.quantize(Decimal(10) ** -places, rounding=ROUND_DOWN)
