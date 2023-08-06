# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
#
# This file is part of SALOME ADAO module
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

# print "import convert_adao"

import convert.parseur_python
from convert.convert_python import *

def entryPoint():
    """
    Retourne les informations nécessaires pour le chargeur de plugins
    Ces informations sont retournées dans un dictionnaire
    """
    return {
        # Le nom du plugin
        'name' : 'ADAO',
        # La factory pour créer une instance du plugin
        'factory' : PythonParser,
        }


