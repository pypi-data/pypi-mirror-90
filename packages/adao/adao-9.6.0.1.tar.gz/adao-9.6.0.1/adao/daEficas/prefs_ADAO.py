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

import os, sys

# print "import des prefs de Adao"
#
# Configuration de Eficas
# =======================
#
# INSTALLDIR, repIni est obligatoire
INSTALLDIR = ""
sys.path.insert(0,INSTALLDIR)
#
# Positionnee a repin au debut, mise a jour dans configuration
repIni=os.path.dirname(os.path.abspath(__file__))
#
# Sert comme directory initial des QFileDialog
initialdir = os.getcwd()
#
# Traductions et codages
#
# Codage des strings qui accepte les accents (en remplacement de 'ascii')
# encoding='utf-8'
#
# ===== Specifique : pour la 8_3_0 et suivantes 8_x ! Enlever pour les 9_x ! JPA
if sys.version.split()[0] < '3':
    # ===== Specifique : redefinition de l'encoding avant le Python 3 ! JPA
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # ===== Specifique : pour les suivantes 8_x ! Enlever pour les 9_x ! JPA
    # 19/05/2017 : Redefinition du hook de "sys" present dans <GUI/src/SUITApp/SUITApp_init_python.cxx>
    def _custom_except_hook(exc_type, exc_value, exc_traceback):
        import sys
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        pass
    sys.excepthook = _custom_except_hook
    del _custom_except_hook, sys
# ===== Fin specifique ===================================================== JPA
#
# Indique la langue du catalogue utilisee pour les chaines d'aide : fr ou ang
# lang = 'fr'
# Traduction des labels de boutons ou autres
lookfor = os.path.abspath(os.path.join(os.path.dirname(__file__),"../resources"))
if os.path.exists(lookfor):
    translatorFichier = os.path.join(lookfor, "adao")
else:
    translatorFichier = os.environ["ADAO_ENGINE_ROOT_DIR"] + "/share/resources/adao/adao" # Ce nom sera complete par EFICAS avec _<LANG>.qm
#
# Pilotage des sous-fenetres d'EFICAS
closeAutreCommande = True
closeFrameRechercheCommande = True
closeEntete = True
closeArbre = True
taille = 800
nombreDeBoutonParLigne = 2

