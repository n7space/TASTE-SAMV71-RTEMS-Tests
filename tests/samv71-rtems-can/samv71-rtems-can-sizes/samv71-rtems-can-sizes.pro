TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += deploymentview.dv.xml
DISTFILES += samv71-rtems-can-sizes.asn
DISTFILES += samv71-rtems-can-sizes.acn
include(work/taste.pro)
message($$DISTFILES)

