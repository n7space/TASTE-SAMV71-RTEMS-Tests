# MAKEFILE_PATH   := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_PATH   := $(lastword $(MAKEFILE_LIST))
TOOL_INST       := $(shell taste-config --prefix)
OUTDIR          := $(dir $(MAKEFILE_PATH))
TASTE_SHARED_TYPES?=${HOME}/.local/share/QtProject/QtCreator/shared_types
ASN1_FILES      :=../TEST-SAMV71-STRESS.asn ${TOOL_INST}/share/taste-types/taste-types.asn system.asn
CP_FILES        :=       # Context parameters
DATAVIEW_PATH   := ${OUTDIR}/dataview
DATAVIEW_UNIQ   := ${DATAVIEW_PATH}/dataview-uniq.asn
DATAVIEW_ACN    := ${DATAVIEW_PATH}/dataview-uniq.acn
# the dataview with AADLv1 data is generated in Python by asn2aadlPlus
DATAVIEW_AADLV1 := ${DATAVIEW_PATH}/dataview_aadlv1.aadl
ASN1_POLICY_FLAGS ?= -typePrefix asn1Scc -renamePolicy 3 -equal -fp AUTO -c -ig -uPER -ACN
#TASTE_SHARED_TYPES?=${TOOL_INST}/share/SharedTypes  # Ellidiss only

# These languages are used in the system: C
# Project cache folder is used to speed up all ASN.1-related processing
export PROJECT_CACHE=${HOME}/.taste_AST_cache
export IV_FILE=$(shell readlink -f ../interfaceview.xml)
all:	build-default
	$(info Run "make -C work check_stack" to analyze the stack usage of your application")

# Call the stack checker
check_stack:
	$(MAKE) -C build -f Makefile.taste check_stack


# Check that all runtimes used in the system are installed
check_targets:
	$(MAKE) -C build -f Makefile.taste check_targets

# Generate the language-specific data view needed before editing user code
dataview:	${DATAVIEW_UNIQ} dataview/C/built

# Generate the complete dataview, including Python bindings if there is a GUI
${DATAVIEW_PATH}/built:  dataview/C/built dataview
	touch $@

${DATAVIEW_AADLV1}: ${DATAVIEW_UNIQ}
	echo [-] Generate dataview entry in Python for aadl2glueC
	asn2aadlPlus  $< $@


# Build based on the deployment view
# The parallel invocation can not be added here because of matlab remote error
# For local matlab instalation it can be added
build-default:	aadl2glueC build/system_config.h ${DATAVIEW_PATH}/built build/deploymentview_final/Makefile
	$(MAKE) -C build -f Makefile.taste

# Execute the generated binaries (used in Space Creator when using the Run button)
run: # Space creator will always build before, so no need to depend on build-default
	$(MAKE) -j -C build -f Makefile.taste run

# Run the Concurrency View analysis tool (cheddar/marzhin)
run_cv: build/ConcurrencyView.aadl
	TASTECV --load $^

# The Concurrency View needed by Cheddar is the concatenation of system.aadl and ocarina_components.aadl
build/ConcurrencyView.aadl:	build/system.aadl
	cat $^ $(shell taste-config --prefix)/share/ocarina/AADLv2/ocarina_components.aadl > $@

# Rule to invoke Ocarina (generation of POHI middleware code)
build/deploymentview_final/Makefile:	build/main.aadl ${DATAVIEW_UNIQ}
	# Nothing will be generated if POHIC is not needed
	$(MAKE) -C build -f Makefile.taste ocarina

# Optionally manage SQL Database (run taste-create-database to enable)
sql_db/DV.py:
	mkdir -p sql_db && touch $@

# Create dataview-uniq.asn by concatenating all asn1 input files
${DATAVIEW_UNIQ}:	${ASN1_FILES}
	mkdir -p ${PROJECT_CACHE} && mkdir -p ${DATAVIEW_PATH}
	sed -e '$$s/$$/\n/' -s $^ > $@

# Create dataview-uniq.acn by concatenating all input files
${DATAVIEW_ACN}:	../TEST-SAMV71-STRESS.acn
	mkdir -p ${DATAVIEW_PATH}
	sed -e '$$s/$$/\n/' -s $^ > $@

# system_config.h is used to filter out non-needed ASN.1 encoder/decoders
build/system_config.h:	$(wildcard */*/wrappers/*_system_config.h)
	cat $^ > $@

#  Call DMT/aadl2glueC to generate glue code from the mini-cv.aadl files
aadl2glueC:	function_10/C/wrappers/aadl2glueC_built function_100/C/wrappers/aadl2glueC_built function_101/C/wrappers/aadl2glueC_built function_102/C/wrappers/aadl2glueC_built function_103/C/wrappers/aadl2glueC_built function_104/C/wrappers/aadl2glueC_built function_106/C/wrappers/aadl2glueC_built function_107/C/wrappers/aadl2glueC_built function_108/C/wrappers/aadl2glueC_built function_109/C/wrappers/aadl2glueC_built function_11/C/wrappers/aadl2glueC_built function_110/C/wrappers/aadl2glueC_built function_111/C/wrappers/aadl2glueC_built function_112/C/wrappers/aadl2glueC_built function_113/C/wrappers/aadl2glueC_built function_115/C/wrappers/aadl2glueC_built function_116/C/wrappers/aadl2glueC_built function_117/C/wrappers/aadl2glueC_built function_118/C/wrappers/aadl2glueC_built function_119/C/wrappers/aadl2glueC_built function_12/C/wrappers/aadl2glueC_built function_120/C/wrappers/aadl2glueC_built function_121/C/wrappers/aadl2glueC_built function_122/C/wrappers/aadl2glueC_built function_124/C/wrappers/aadl2glueC_built function_125/C/wrappers/aadl2glueC_built function_126/C/wrappers/aadl2glueC_built function_127/C/wrappers/aadl2glueC_built function_128/C/wrappers/aadl2glueC_built function_129/C/wrappers/aadl2glueC_built function_13/C/wrappers/aadl2glueC_built function_130/C/wrappers/aadl2glueC_built function_131/C/wrappers/aadl2glueC_built function_132/C/wrappers/aadl2glueC_built function_14/C/wrappers/aadl2glueC_built function_15/C/wrappers/aadl2glueC_built function_16/C/wrappers/aadl2glueC_built function_17/C/wrappers/aadl2glueC_built function_18/C/wrappers/aadl2glueC_built function_19/C/wrappers/aadl2glueC_built function_2/C/wrappers/aadl2glueC_built function_20/C/wrappers/aadl2glueC_built function_21/C/wrappers/aadl2glueC_built function_22/C/wrappers/aadl2glueC_built function_23/C/wrappers/aadl2glueC_built function_24/C/wrappers/aadl2glueC_built function_25/C/wrappers/aadl2glueC_built function_26/C/wrappers/aadl2glueC_built function_27/C/wrappers/aadl2glueC_built function_28/C/wrappers/aadl2glueC_built function_29/C/wrappers/aadl2glueC_built function_3/C/wrappers/aadl2glueC_built function_30/C/wrappers/aadl2glueC_built function_31/C/wrappers/aadl2glueC_built function_32/C/wrappers/aadl2glueC_built function_33/C/wrappers/aadl2glueC_built function_34/C/wrappers/aadl2glueC_built function_35/C/wrappers/aadl2glueC_built function_36/C/wrappers/aadl2glueC_built function_37/C/wrappers/aadl2glueC_built function_38/C/wrappers/aadl2glueC_built function_39/C/wrappers/aadl2glueC_built function_4/C/wrappers/aadl2glueC_built function_40/C/wrappers/aadl2glueC_built function_41/C/wrappers/aadl2glueC_built function_42/C/wrappers/aadl2glueC_built function_43/C/wrappers/aadl2glueC_built function_44/C/wrappers/aadl2glueC_built function_45/C/wrappers/aadl2glueC_built function_46/C/wrappers/aadl2glueC_built function_47/C/wrappers/aadl2glueC_built function_48/C/wrappers/aadl2glueC_built function_49/C/wrappers/aadl2glueC_built function_5/C/wrappers/aadl2glueC_built function_50/C/wrappers/aadl2glueC_built function_51/C/wrappers/aadl2glueC_built function_52/C/wrappers/aadl2glueC_built function_53/C/wrappers/aadl2glueC_built function_54/C/wrappers/aadl2glueC_built function_55/C/wrappers/aadl2glueC_built function_56/C/wrappers/aadl2glueC_built function_57/C/wrappers/aadl2glueC_built function_58/C/wrappers/aadl2glueC_built function_59/C/wrappers/aadl2glueC_built function_6/C/wrappers/aadl2glueC_built function_60/C/wrappers/aadl2glueC_built function_61/C/wrappers/aadl2glueC_built function_62/C/wrappers/aadl2glueC_built function_63/C/wrappers/aadl2glueC_built function_64/C/wrappers/aadl2glueC_built function_65/C/wrappers/aadl2glueC_built function_66/C/wrappers/aadl2glueC_built function_67/C/wrappers/aadl2glueC_built function_68/C/wrappers/aadl2glueC_built function_69/C/wrappers/aadl2glueC_built function_7/C/wrappers/aadl2glueC_built function_70/C/wrappers/aadl2glueC_built function_71/C/wrappers/aadl2glueC_built function_72/C/wrappers/aadl2glueC_built function_73/C/wrappers/aadl2glueC_built function_74/C/wrappers/aadl2glueC_built function_75/C/wrappers/aadl2glueC_built function_76/C/wrappers/aadl2glueC_built function_77/C/wrappers/aadl2glueC_built function_78/C/wrappers/aadl2glueC_built function_79/C/wrappers/aadl2glueC_built function_8/C/wrappers/aadl2glueC_built function_80/C/wrappers/aadl2glueC_built function_81/C/wrappers/aadl2glueC_built function_82/C/wrappers/aadl2glueC_built function_83/C/wrappers/aadl2glueC_built function_84/C/wrappers/aadl2glueC_built function_85/C/wrappers/aadl2glueC_built function_86/C/wrappers/aadl2glueC_built function_87/C/wrappers/aadl2glueC_built function_88/C/wrappers/aadl2glueC_built function_89/C/wrappers/aadl2glueC_built function_9/C/wrappers/aadl2glueC_built function_90/C/wrappers/aadl2glueC_built function_91/C/wrappers/aadl2glueC_built function_92/C/wrappers/aadl2glueC_built function_93/C/wrappers/aadl2glueC_built function_94/C/wrappers/aadl2glueC_built function_95/C/wrappers/aadl2glueC_built function_96/C/wrappers/aadl2glueC_built function_97/C/wrappers/aadl2glueC_built function_98/C/wrappers/aadl2glueC_built function_99/C/wrappers/aadl2glueC_built testfunction/C/wrappers/aadl2glueC_built triggerfunction/C/wrappers/aadl2glueC_built

function_10/C/wrappers/aadl2glueC_built: function_10/C/wrappers/function_10_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_100/C/wrappers/aadl2glueC_built: function_100/C/wrappers/function_100_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_101/C/wrappers/aadl2glueC_built: function_101/C/wrappers/function_101_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_102/C/wrappers/aadl2glueC_built: function_102/C/wrappers/function_102_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_103/C/wrappers/aadl2glueC_built: function_103/C/wrappers/function_103_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_104/C/wrappers/aadl2glueC_built: function_104/C/wrappers/function_104_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_106/C/wrappers/aadl2glueC_built: function_106/C/wrappers/function_106_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_107/C/wrappers/aadl2glueC_built: function_107/C/wrappers/function_107_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_108/C/wrappers/aadl2glueC_built: function_108/C/wrappers/function_108_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_109/C/wrappers/aadl2glueC_built: function_109/C/wrappers/function_109_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_11/C/wrappers/aadl2glueC_built: function_11/C/wrappers/function_11_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_110/C/wrappers/aadl2glueC_built: function_110/C/wrappers/function_110_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_111/C/wrappers/aadl2glueC_built: function_111/C/wrappers/function_111_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_112/C/wrappers/aadl2glueC_built: function_112/C/wrappers/function_112_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_113/C/wrappers/aadl2glueC_built: function_113/C/wrappers/function_113_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_115/C/wrappers/aadl2glueC_built: function_115/C/wrappers/function_115_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_116/C/wrappers/aadl2glueC_built: function_116/C/wrappers/function_116_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_117/C/wrappers/aadl2glueC_built: function_117/C/wrappers/function_117_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_118/C/wrappers/aadl2glueC_built: function_118/C/wrappers/function_118_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_119/C/wrappers/aadl2glueC_built: function_119/C/wrappers/function_119_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_12/C/wrappers/aadl2glueC_built: function_12/C/wrappers/function_12_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_120/C/wrappers/aadl2glueC_built: function_120/C/wrappers/function_120_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_121/C/wrappers/aadl2glueC_built: function_121/C/wrappers/function_121_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_122/C/wrappers/aadl2glueC_built: function_122/C/wrappers/function_122_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_124/C/wrappers/aadl2glueC_built: function_124/C/wrappers/function_124_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_125/C/wrappers/aadl2glueC_built: function_125/C/wrappers/function_125_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_126/C/wrappers/aadl2glueC_built: function_126/C/wrappers/function_126_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_127/C/wrappers/aadl2glueC_built: function_127/C/wrappers/function_127_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_128/C/wrappers/aadl2glueC_built: function_128/C/wrappers/function_128_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_129/C/wrappers/aadl2glueC_built: function_129/C/wrappers/function_129_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_13/C/wrappers/aadl2glueC_built: function_13/C/wrappers/function_13_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_130/C/wrappers/aadl2glueC_built: function_130/C/wrappers/function_130_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_131/C/wrappers/aadl2glueC_built: function_131/C/wrappers/function_131_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_132/C/wrappers/aadl2glueC_built: function_132/C/wrappers/function_132_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_14/C/wrappers/aadl2glueC_built: function_14/C/wrappers/function_14_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_15/C/wrappers/aadl2glueC_built: function_15/C/wrappers/function_15_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_16/C/wrappers/aadl2glueC_built: function_16/C/wrappers/function_16_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_17/C/wrappers/aadl2glueC_built: function_17/C/wrappers/function_17_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_18/C/wrappers/aadl2glueC_built: function_18/C/wrappers/function_18_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_19/C/wrappers/aadl2glueC_built: function_19/C/wrappers/function_19_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_2/C/wrappers/aadl2glueC_built: function_2/C/wrappers/function_2_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_20/C/wrappers/aadl2glueC_built: function_20/C/wrappers/function_20_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_21/C/wrappers/aadl2glueC_built: function_21/C/wrappers/function_21_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_22/C/wrappers/aadl2glueC_built: function_22/C/wrappers/function_22_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_23/C/wrappers/aadl2glueC_built: function_23/C/wrappers/function_23_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_24/C/wrappers/aadl2glueC_built: function_24/C/wrappers/function_24_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_25/C/wrappers/aadl2glueC_built: function_25/C/wrappers/function_25_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_26/C/wrappers/aadl2glueC_built: function_26/C/wrappers/function_26_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_27/C/wrappers/aadl2glueC_built: function_27/C/wrappers/function_27_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_28/C/wrappers/aadl2glueC_built: function_28/C/wrappers/function_28_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_29/C/wrappers/aadl2glueC_built: function_29/C/wrappers/function_29_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_3/C/wrappers/aadl2glueC_built: function_3/C/wrappers/function_3_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_30/C/wrappers/aadl2glueC_built: function_30/C/wrappers/function_30_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_31/C/wrappers/aadl2glueC_built: function_31/C/wrappers/function_31_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_32/C/wrappers/aadl2glueC_built: function_32/C/wrappers/function_32_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_33/C/wrappers/aadl2glueC_built: function_33/C/wrappers/function_33_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_34/C/wrappers/aadl2glueC_built: function_34/C/wrappers/function_34_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_35/C/wrappers/aadl2glueC_built: function_35/C/wrappers/function_35_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_36/C/wrappers/aadl2glueC_built: function_36/C/wrappers/function_36_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_37/C/wrappers/aadl2glueC_built: function_37/C/wrappers/function_37_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_38/C/wrappers/aadl2glueC_built: function_38/C/wrappers/function_38_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_39/C/wrappers/aadl2glueC_built: function_39/C/wrappers/function_39_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_4/C/wrappers/aadl2glueC_built: function_4/C/wrappers/function_4_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_40/C/wrappers/aadl2glueC_built: function_40/C/wrappers/function_40_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_41/C/wrappers/aadl2glueC_built: function_41/C/wrappers/function_41_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_42/C/wrappers/aadl2glueC_built: function_42/C/wrappers/function_42_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_43/C/wrappers/aadl2glueC_built: function_43/C/wrappers/function_43_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_44/C/wrappers/aadl2glueC_built: function_44/C/wrappers/function_44_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_45/C/wrappers/aadl2glueC_built: function_45/C/wrappers/function_45_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_46/C/wrappers/aadl2glueC_built: function_46/C/wrappers/function_46_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_47/C/wrappers/aadl2glueC_built: function_47/C/wrappers/function_47_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_48/C/wrappers/aadl2glueC_built: function_48/C/wrappers/function_48_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_49/C/wrappers/aadl2glueC_built: function_49/C/wrappers/function_49_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_5/C/wrappers/aadl2glueC_built: function_5/C/wrappers/function_5_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_50/C/wrappers/aadl2glueC_built: function_50/C/wrappers/function_50_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_51/C/wrappers/aadl2glueC_built: function_51/C/wrappers/function_51_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_52/C/wrappers/aadl2glueC_built: function_52/C/wrappers/function_52_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_53/C/wrappers/aadl2glueC_built: function_53/C/wrappers/function_53_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_54/C/wrappers/aadl2glueC_built: function_54/C/wrappers/function_54_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_55/C/wrappers/aadl2glueC_built: function_55/C/wrappers/function_55_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_56/C/wrappers/aadl2glueC_built: function_56/C/wrappers/function_56_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_57/C/wrappers/aadl2glueC_built: function_57/C/wrappers/function_57_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_58/C/wrappers/aadl2glueC_built: function_58/C/wrappers/function_58_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_59/C/wrappers/aadl2glueC_built: function_59/C/wrappers/function_59_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_6/C/wrappers/aadl2glueC_built: function_6/C/wrappers/function_6_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_60/C/wrappers/aadl2glueC_built: function_60/C/wrappers/function_60_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_61/C/wrappers/aadl2glueC_built: function_61/C/wrappers/function_61_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_62/C/wrappers/aadl2glueC_built: function_62/C/wrappers/function_62_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_63/C/wrappers/aadl2glueC_built: function_63/C/wrappers/function_63_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_64/C/wrappers/aadl2glueC_built: function_64/C/wrappers/function_64_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_65/C/wrappers/aadl2glueC_built: function_65/C/wrappers/function_65_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_66/C/wrappers/aadl2glueC_built: function_66/C/wrappers/function_66_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_67/C/wrappers/aadl2glueC_built: function_67/C/wrappers/function_67_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_68/C/wrappers/aadl2glueC_built: function_68/C/wrappers/function_68_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_69/C/wrappers/aadl2glueC_built: function_69/C/wrappers/function_69_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_7/C/wrappers/aadl2glueC_built: function_7/C/wrappers/function_7_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_70/C/wrappers/aadl2glueC_built: function_70/C/wrappers/function_70_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_71/C/wrappers/aadl2glueC_built: function_71/C/wrappers/function_71_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_72/C/wrappers/aadl2glueC_built: function_72/C/wrappers/function_72_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_73/C/wrappers/aadl2glueC_built: function_73/C/wrappers/function_73_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_74/C/wrappers/aadl2glueC_built: function_74/C/wrappers/function_74_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_75/C/wrappers/aadl2glueC_built: function_75/C/wrappers/function_75_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_76/C/wrappers/aadl2glueC_built: function_76/C/wrappers/function_76_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_77/C/wrappers/aadl2glueC_built: function_77/C/wrappers/function_77_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_78/C/wrappers/aadl2glueC_built: function_78/C/wrappers/function_78_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_79/C/wrappers/aadl2glueC_built: function_79/C/wrappers/function_79_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_8/C/wrappers/aadl2glueC_built: function_8/C/wrappers/function_8_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_80/C/wrappers/aadl2glueC_built: function_80/C/wrappers/function_80_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_81/C/wrappers/aadl2glueC_built: function_81/C/wrappers/function_81_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_82/C/wrappers/aadl2glueC_built: function_82/C/wrappers/function_82_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_83/C/wrappers/aadl2glueC_built: function_83/C/wrappers/function_83_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_84/C/wrappers/aadl2glueC_built: function_84/C/wrappers/function_84_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_85/C/wrappers/aadl2glueC_built: function_85/C/wrappers/function_85_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_86/C/wrappers/aadl2glueC_built: function_86/C/wrappers/function_86_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_87/C/wrappers/aadl2glueC_built: function_87/C/wrappers/function_87_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_88/C/wrappers/aadl2glueC_built: function_88/C/wrappers/function_88_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_89/C/wrappers/aadl2glueC_built: function_89/C/wrappers/function_89_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_9/C/wrappers/aadl2glueC_built: function_9/C/wrappers/function_9_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_90/C/wrappers/aadl2glueC_built: function_90/C/wrappers/function_90_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_91/C/wrappers/aadl2glueC_built: function_91/C/wrappers/function_91_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_92/C/wrappers/aadl2glueC_built: function_92/C/wrappers/function_92_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_93/C/wrappers/aadl2glueC_built: function_93/C/wrappers/function_93_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_94/C/wrappers/aadl2glueC_built: function_94/C/wrappers/function_94_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_95/C/wrappers/aadl2glueC_built: function_95/C/wrappers/function_95_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_96/C/wrappers/aadl2glueC_built: function_96/C/wrappers/function_96_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_97/C/wrappers/aadl2glueC_built: function_97/C/wrappers/function_97_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_98/C/wrappers/aadl2glueC_built: function_98/C/wrappers/function_98_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

function_99/C/wrappers/aadl2glueC_built: function_99/C/wrappers/function_99_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

testfunction/C/wrappers/aadl2glueC_built: testfunction/C/wrappers/testfunction_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@

triggerfunction/C/wrappers/aadl2glueC_built: triggerfunction/C/wrappers/triggerfunction_mini_cv.aadl ${DATAVIEW_AADLV1}
	touch $@


# Compile the ASN.1 models in C
dataview/C/built: ${DATAVIEW_UNIQ} ${DATAVIEW_ACN} ${CP_FILES}
	$(info [-] Compiling the dataview in C)
	mkdir -p $(dir $@)
	asn1scc ${ASN1SCC_FLAGS} -o $(dir $@) ${ASN1_POLICY_FLAGS} $^
	cp ${TOOL_INST}/share/AutoGUI/debug_messages.? dataview/C
	cp ${TOOL_INST}/share/AutoGUI/timeInMS.? dataview/C
	cd dataview/C && msgPrinterASN1 ../dataview-uniq.asn
	touch $@



simulink_skeletons:
	# target required only for SIMULINK and VHDL, which use specific DMT paths
	# empty otherwise

clean:
	rm -rf binaries dataview
	$(MAKE) -C build -f Makefile.taste clean

.PHONY: clean simu compile-all-linux function-instances-linux function-types-linux build-default dataview build-rtems-ada dataview build/modelchecking modelchecking/subtypes/$(SUBTYPE) obs-to-if aadl-to-if asn-to-if $(PROPERTIES_CONFIG) run_cv simulink_skeletons

