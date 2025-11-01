TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn
DISTFILES += samv71-rtems-serial.msc
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/*.msc
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += deploymentview.dv.xml
DISTFILES += samv71-rtems-serial.asn
DISTFILES += samv71-rtems-serial.acn
include(work/taste.pro)
message($$DISTFILES)

