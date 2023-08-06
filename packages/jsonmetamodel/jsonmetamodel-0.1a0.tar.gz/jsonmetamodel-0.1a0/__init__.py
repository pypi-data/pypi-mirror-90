# -*- coding: utf-8 -*-
# Diese __init__ ist dazu geschrieben worden, damit Module oder Pakete die
# nach dem disutils-layout gestaltet sind, in Umgebungen verwendet werden
# können, wo ein benutzerdefinierter Pfad auf zu verwendende Module oder
# Pakete zeigt. Das Problem dabei mit dem disutils-layout ist, dass Python
# solche Pakete nicht automatisch sauber einbindet. Für das Beispielpaket
# userdefinedpackage würde der Aufbau so aussehen:
#
#     ./userdefinedpackage/setup.py
#     ./userdefinedpackage/userdefinedpackage/__init__.py
#     ./userdefinedpackage/userdefinedpackage/custommodule.py
#
# Def Befehl:
#
#     import userdefinedpackage
#
# würde den Ordner ./userdefinedpackage/ im benutzerdefinierten Pfad als
# Namespace einbinden. Das Paket oder Module befindet sich jedoch im Pfad
# ./userdefinedpackage/userdefinedpackage.
#
# Dies wird hier dadurch gelöst, dass dieses Paketverzeichnis in die aktuelle
# Laufzeitumgebung vor den benutzerdefinierten Paketpfad eingebunden wird.
# Dadurch wird in der import Abfrage als erstes dieses Paket gefunden und
# importiert.
import os
import sys
from importlib import reload, import_module

_currentpackagepath = os.path.normpath(os.path.split(__file__)[0])
_currentpackagename = os.path.split(_currentpackagepath)[1]
if _currentpackagepath not in sys.path:
    print("Adding {} to current runtime paths".format(_currentpackagepath))
    sys.path.insert(0, _currentpackagepath)

    del sys.modules[_currentpackagename]
    import_module(_currentpackagename)
