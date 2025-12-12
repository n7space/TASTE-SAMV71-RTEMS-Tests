TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn \
    samv71.dv.xml
DISTFILES += TEST-SAMV71-FUNCTION-C-IMPLEMENTATION.msc
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/*.msc
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += TEST-SAMV71-FUNCTION-C-IMPLEMENTATION.asn
DISTFILES += TEST-SAMV71-FUNCTION-C-IMPLEMENTATION.acn
include(work/taste.pro)
message($$DISTFILES)

