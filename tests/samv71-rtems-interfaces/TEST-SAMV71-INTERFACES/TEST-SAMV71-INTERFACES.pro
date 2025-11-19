TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn \
    samv71.dv.xml
DISTFILES += TEST-SAMV71-INTERFACES.msc
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/*.msc
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += TEST-SAMV71-INTERFACES.asn
DISTFILES += TEST-SAMV71-INTERFACES.acn
include(work/taste.pro)
message($$DISTFILES)

