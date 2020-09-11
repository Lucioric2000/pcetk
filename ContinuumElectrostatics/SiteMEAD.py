# -------------------------------------------------------------------------------
# . File      : SiteMEAD.py
# . Program   : pDynamo-1.8.0                           (http://www.pdynamo.org)
# . Copyright : CEA, CNRS, Martin  J. Field  (2007-2012),
#                          Mikolaj J. Feliks (2014-2016)
# . License   : CeCILL French Free Software License     (http://www.cecill.info)
# -------------------------------------------------------------------------------
from pCore import Vector3, Selection, Clone
from Error import ContinuumElectrostaticsError
from Site import Site
from InstanceMEAD import InstanceMEAD
from PQRFileWriter import PQRFile_FromSystem
from InputFileWriter import WriteInputFile

import os


class SiteMEAD(Site):
    """A class representing a MEAD-based titratable site."""

    defaultAttributes = {}
    defaultAttributes.update(Site.defaultAttributes)

    def __init__(self, **keywordArguments):
        """Constructor."""
        super(SiteMEAD, self).__init__(**keywordArguments)

    # -------------------------------------------------------------------------------
    def _WriteMEADFiles(self, system, systemCharges, systemRadii):
        """For each instance of each site, write:
        - PQR file for the site    - PQR file for the model compound
        - OGM file for the site    - MGM file for the model compound"""
        grids = []
        model = self.parent
        for stepIndex, (nodes, resolution) in enumerate(model.focusingSteps):
            if stepIndex < 1:
                grids.append("ON_GEOM_CENT %d %f\n" % (nodes, resolution))
            else:
                x, y, z = self.center
                grids.append("(%f %f %f) %d %f\n" % (x, y, z, nodes, resolution))

        selectSite = Selection(self.siteAtomIndices)
        selectModel = Selection(self.modelAtomIndices)

        # . In the PQR file of the model compound, charges of the site atoms must be set to zero (requirement of the my_2diel_solver program)
        chargesZeroSite = Clone(systemCharges)
        for atomIndex in self.siteAtomIndices:
            chargesZeroSite[atomIndex] = 0.0

        for instance in self.instances:
            PQRFile_FromSystem(
                instance.modelPqr,
                system,
                selection=selectModel,
                charges=chargesZeroSite,
                radii=systemRadii,
            )

            # . Update system charges with instance charges
            chargesInstance = Clone(systemCharges)
            for chargeIndex, atomIndex in enumerate(self.siteAtomIndices):
                chargesInstance[atomIndex] = instance.charges[chargeIndex]

            PQRFile_FromSystem(
                instance.sitePqr,
                system,
                selection=selectSite,
                charges=chargesInstance,
                radii=systemRadii,
            )
            del chargesInstance

            # . Write OGM and MGM files (they have the same content)
            for fileGrid in (instance.modelGrid, instance.siteGrid):
                WriteInputFile(fileGrid, grids)

        del chargesZeroSite

    # -------------------------------------------------------------------------------
    def _CreateFilename(self, prefix, label, postfix):
        model = self.parent
        if model.splitToDirectories:
            return os.path.join(
                model.pathScratch,
                self.segName,
                "%s%d" % (self.resName, self.resSerial),
                "%s_%s.%s" % (prefix, label, postfix),
            )
        else:
            return os.path.join(
                model.pathScratch,
                "%s_%s_%s_%d_%s.%s"
                % (prefix, self.segName, self.resName, self.resSerial, label, postfix),
            )

    # -------------------------------------------------------------------------------
    def _CreateInstances(self, templatesOfInstances, globalIndex):
        """Create instances of a site."""
        self.instances = []
        cemodel = self.parent
        for instIndex, instance in enumerate(templatesOfInstances):
            newInstance = InstanceMEAD(
                parent=self,
                instIndex=instIndex,
                _instIndexGlobal=globalIndex,
                label=instance.label,
                charges=instance.charges,
                modelPqr=self._CreateFilename("model", instance.label, "pqr"),
                modelLog=self._CreateFilename("model", instance.label, "out"),
                modelGrid=self._CreateFilename("model", instance.label, "mgm"),
                sitePqr=self._CreateFilename("site", instance.label, "pqr"),
                siteLog=self._CreateFilename("site", instance.label, "out"),
                siteGrid=self._CreateFilename("site", instance.label, "ogm"),
            )

            # . Recalculate reaction energy depending on the temperature
            Gmodel = instance.Gmodel * cemodel.temperature / 300.0
            cemodel.energyModel.SetGmodel(globalIndex, Gmodel)

            # . Set the number of bound protons
            cemodel.energyModel.SetProtons(globalIndex, instance.nprotons)

            # . Add the newly created instance to the list of instances
            self.instances.append(newInstance)
            globalIndex += 1

        return globalIndex


# ===============================================================================
# . Main program
# ===============================================================================
if __name__ == "__main__":
    pass
