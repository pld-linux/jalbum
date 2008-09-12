#!/bin/sh
exec /usr/bin/java -Xmx512M -jar @APPDIR@/JAlbum.jar ${1:+"$@"}
