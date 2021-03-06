PDYNAMO_PCORE = /home/mikolaj/local/opt/pDynamo-1.9.0/pCore-1.9.0
PY_INCLUDE    = /usr/include/python2.7

# The options -fdata-sections and -ffunction-sections are for not linking the unused code
CFLAGS        = -O2 -fPIC -c -I$(PDYNAMO_PCORE)/extensions/cinclude -I$(PY_INCLUDE) -I../cinclude 
CC            = gcc


default: MCModelDefault.so EnergyModel.so StateVector.so
	@echo "\n*** Use 'make clean_all' and then 'make' if you want to recompile Cython sources ***\n"

install: MCModelDefault.so EnergyModel.so StateVector.so
	mv MCModelDefault.so ../../ContinuumElectrostatics/
	mv EnergyModel.so    ../../ContinuumElectrostatics/
	mv StateVector.so    ../../ContinuumElectrostatics/

clean:
	if [ -e ContinuumElectrostatics.MCModelDefault.o ]; then rm ContinuumElectrostatics.MCModelDefault.o ; fi
	if [ -e ContinuumElectrostatics.EnergyModel.o    ]; then rm ContinuumElectrostatics.EnergyModel.o    ; fi
	if [ -e ContinuumElectrostatics.StateVector.o    ]; then rm ContinuumElectrostatics.StateVector.o    ; fi
	if [ -e MCModelDefault.so                        ]; then rm MCModelDefault.so                        ; fi
	if [ -e EnergyModel.so                           ]; then rm EnergyModel.so                           ; fi
	if [ -e StateVector.so                           ]; then rm StateVector.so                           ; fi
	+$(MAKE) -C ../csource clean

clean_all: clean
	if [ -e ContinuumElectrostatics.MCModelDefault.c ]; then rm ContinuumElectrostatics.MCModelDefault.c ; fi
	if [ -e ContinuumElectrostatics.EnergyModel.c    ]; then rm ContinuumElectrostatics.EnergyModel.c    ; fi
	if [ -e ContinuumElectrostatics.StateVector.c    ]; then rm ContinuumElectrostatics.StateVector.c    ; fi
	+$(MAKE) -C ../csource clean_all


#===============================================================================
#                                 pCore-library
#===============================================================================
../csource/lib/libpcore.a:
	+$(MAKE) -C ../csource/lib


#===============================================================================
#                                MCModelDefault 
#===============================================================================
../csource/MCModelDefault.o:
	+$(MAKE) -C ../csource

# -lm is needed because of exp
MCModelDefault.so: ../csource/MCModelDefault.o ../csource/EnergyModel.o ../csource/StateVector.o ../csource/lib/libpcore.a ContinuumElectrostatics.MCModelDefault.o
	$(CC) -shared ContinuumElectrostatics.MCModelDefault.o ../csource/MCModelDefault.o ../csource/EnergyModel.o ../csource/StateVector.o ../csource/lib/libpcore.a -o MCModelDefault.so -lm

ContinuumElectrostatics.MCModelDefault.o: ContinuumElectrostatics.MCModelDefault.c
	$(CC) $(CFLAGS) ContinuumElectrostatics.MCModelDefault.c -o ContinuumElectrostatics.MCModelDefault.o

ContinuumElectrostatics.MCModelDefault.c: ContinuumElectrostatics.MCModelDefault.pyx ContinuumElectrostatics.MCModelDefault.pxd
	python cython_compile.py $(PDYNAMO_PCORE) ContinuumElectrostatics.MCModelDefault.pyx


#===============================================================================
#                                  EnergyModel
#===============================================================================
../csource/EnergyModel.o:
	+$(MAKE) -C ../csource

EnergyModel.so: ../csource/EnergyModel.o ../csource/StateVector.o ../csource/lib/libpcore.a ContinuumElectrostatics.EnergyModel.o
	$(CC) -shared ContinuumElectrostatics.EnergyModel.o ../csource/EnergyModel.o ../csource/StateVector.o ../csource/lib/libpcore.a -o EnergyModel.so

ContinuumElectrostatics.EnergyModel.o: ContinuumElectrostatics.EnergyModel.c
	$(CC) $(CFLAGS) ContinuumElectrostatics.EnergyModel.c -o ContinuumElectrostatics.EnergyModel.o

ContinuumElectrostatics.EnergyModel.c: ContinuumElectrostatics.EnergyModel.pyx ContinuumElectrostatics.EnergyModel.pxd
	python cython_compile.py $(PDYNAMO_PCORE) ContinuumElectrostatics.EnergyModel.pyx


#===============================================================================
#                                  StateVector
#===============================================================================
../csource/StateVector.o:
	+$(MAKE) -C ../csource

StateVector.so: ../csource/StateVector.o ../csource/lib/libpcore.a ContinuumElectrostatics.StateVector.o
	$(CC) -shared ContinuumElectrostatics.StateVector.o ../csource/StateVector.o ../csource/lib/libpcore.a -o StateVector.so

ContinuumElectrostatics.StateVector.o: ContinuumElectrostatics.StateVector.c
	$(CC) $(CFLAGS) ContinuumElectrostatics.StateVector.c -o ContinuumElectrostatics.StateVector.o

ContinuumElectrostatics.StateVector.c: ContinuumElectrostatics.StateVector.pyx ContinuumElectrostatics.StateVector.pxd
	python cython_compile.py $(PDYNAMO_PCORE) ContinuumElectrostatics.StateVector.pyx
