#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2018)
#
# SmartMet Data Ingestion Module for Radar in HDF5 Odim format
#

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME/smartmet
fi

OUT=$BASE/data/radar
IN=$BASE/data/incoming/radar
EDITOR=$BASE/editor/radar
LOGFILE=$BASE/logs/data/radar.log

# Use log file if not run interactively
if [ $TERM = "dumb" ]; then
    exec &> $LOGFILE
fi

for FILE in $IN/*.h5
do
    if [ -s $FILE ]; then
	SITE=$(basename $FILE|cut -f1 -d.)
	PROD=$(basename $FILE|cut -f3 -d.)
	TIMESTAMP=$(basename $FILE|cut -f2 -d.)
	h5toqd --lowercase --producername "${SITE} ${PROD}" $FILE "$EDITOR/%ORIGINTIME_radar_%PLC_%PRODUCT_%QUANTITY%INTERVAL.sqd"
	rm -f $FILE
        # copy data files to /smartmet/data/
        mkdir -p $OUT/${SITE}/querydata/
        rsync -av  $EDITOR/* $OUT/${SITE}/querydata/         
    fi
done
