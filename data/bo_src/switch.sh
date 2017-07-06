#!/bin/bash

GDML="bo_src"
GEO="bo_src"
PMT="PMTINFO"
SUFFIX="_all_sensitive"
TEMP_SUFFIX="_temp"

mv $GDML$SUFFIX.gdml $GDML$TEMP_SUFFIX.gdml
mv $GEO$SUFFIX.geo $GEO$TEMP_SUFFIX.geo
mv $PMT$SUFFIX.ffrll $PMT$TEMP_SUFFIX.ratdb

mv $GDML.gdml $GDML$SUFFIX.gdml
mv $GEO.geo $GEO$SUFFIX.geo
mv $PMT.ratdb $PMT$SUFFIX.ffrll

mv $GDML$TEMP_SUFFIX.gdml $GDML.gdml
mv $GEO$TEMP_SUFFIX.geo $GEO.geo
mv $PMT$TEMP_SUFFIX.ratdb $PMT.ratdb
