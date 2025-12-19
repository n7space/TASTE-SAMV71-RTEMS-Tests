TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn
DISTFILES += test-sam-rtems-can.msc
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/*.msc
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += deploymentview.dv.xml
DISTFILES += test-sam-rtems-can.asn
DISTFILES += test-sam-rtems-can.acn
include(work/taste.pro)
message($$DISTFILES)

