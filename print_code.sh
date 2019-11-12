#!/bin/bash

FNAMES=("bblist.py" "bbviz.py" "bitblox.py" "formulate.py" "schematic.py" "NMote.py")

for i in "${FNAMES[@]}"
do
	enscript -Epython --color -q -Z -p - -f Courier10 $i | ps2pdf - "$i.pdf"
done

