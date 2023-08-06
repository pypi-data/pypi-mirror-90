# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Text markup for the SubViewer 2.0 format."""

import aeidon

__all__ = ("SubViewer2",)


class SubViewer2(aeidon.markups.SubRip):

    """
    Text markup for the SubViewer 2.0 format.

    SubViewer 2.0 format is assumed to contain the same markup as SubRip.
    """

    format = aeidon.formats.SUBVIEWER2
