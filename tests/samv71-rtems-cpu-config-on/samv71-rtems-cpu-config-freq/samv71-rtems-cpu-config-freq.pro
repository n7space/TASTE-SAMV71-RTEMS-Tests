TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn \
    samv71.dv.xml
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += samv71-rtems-cpu-config-freq.asn
DISTFILES += samv71-rtems-cpu-config-freq.acn
include(work/taste.pro)
message($$DISTFILES)

