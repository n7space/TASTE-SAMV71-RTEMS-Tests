TEMPLATE = lib
CONFIG -= qt
CONFIG += generateC

DISTFILES +=  $(HOME)/tool-inst/share/taste-types/taste-types.asn
DISTFILES += TEST-SAMV71-1-N-COMMUNICATION.msc
DISTFILES += interfaceview.xml
DISTFILES += work/binaries/*.msc
DISTFILES += work/binaries/coverage/index.html
DISTFILES += work/binaries/filters
DISTFILES += work/system.asn

DISTFILES += TEST-SAMV71-1-N-COMMUNICATION.asn
DISTFILES += TEST-SAMV71-1-N-COMMUNICATION.acn
include(work/taste.pro)
message($$DISTFILES)

