__doc__ = """
Glide cross-docking application.  Takes ligands, receptors, complexes, and
grids as input.  Generates grids for receptors and complexes, docks all ligands
(including those from complexes) into all grids, and calculates RMSDs for
docked ligand poses compared to their input references.

$Revision: 3.5 $
$Date: 2010/01/15 08:14:50 $

Copyright Schrodinger, LLC. All rights reserved.
"""
# Contributors: Jeff A. Saunders

# xglide_mga.py Contributors: Tomohiro Ban, Masahito Ohue and Yutaka Akiyama

########################################################################
#         xglide_mga.py version 1.0 (last updete: 29 Jan, 2016)        #
########################################################################


_input_file_documentation = """
########################################################################
#                                                                      #
#                  XGlide input file documentation                     #
#                                                                      #
#    The input file is based on keyword/value pairs, though certain    #
#    keywords can accept multiple values).  The notes below            #
#    the keywords, with explanations of their purpose and accepted     #
#    values.                                                           #
#                                                                      #
########################################################################

####################
# Input structures #
####################

COMPLEX <file/dir>[,<ligand_asl>]
#    Can be a Maestro or PDB file, or a directory.  If a directory, all of the
#    Maestro and PDB files there will be read in as complexes.  Multiple-CT
#    files will be treated as a combined complex.  If a file has only a
#    single molecule, it is ignored.  By default, the first ligand detected
#    by the AslLigandSearcher is assumed to be the ligand, unless a ligand ASL
#    expression <ligand_asl> is provided.
#    NOTE: In earlier versions, the option field was the ligand molecule
#    number.  The equivalent ASL expression is "mol.num <ligand_molnum>".
#    For backwards compatibility, if the <ligand_asl> is an integer, it will
#    be intpreted as a molecule number; if the value is 0, the ligand will be
#    the last molecule in the structure.

RECEPTOR <file/dir>
#    Can be a Maestro or PDB file, or a directory.  If a directory, all of the
#    Maestro and PDB files there will be read in as receptors.  Multiple-CT
#    files will be treated as a combined receptor.  Multiple molecules
#    are assumed to be part of the receptor structure.

LIGAND <file/dir>[,REFPOSE][,<file>]
#    Can be a Maestro, PDB, or SDF file, or a directory.  If a directory, all
#    of the Maestro and PDB files there will be read in as receptors.
#    Multiple-CT files will be treated as multiple ligands.  If REFPOSE is
#    present (no spaces allowed), the ligands so specified are assumed to be in
#    the proper pose and frame of reference for grid generation (if AUTO) and
#    RMSD calculations.  If an additional filename is provided for a file
#    LIGAND specification, and it matches a file RECEPTOR or GRID
#    specification, the LIGAND will be linked to that receptor or grid for the
#    purpose of native redocking; this option no longer implies REFPOSE, so
#    use that keyword explicitly to use these ligands for setting the grid
#    center (if SELF) and for RMSD calculations.

GRID <file>[,<int>]
#    Can be a .grd or .zip grid file.  The optional <int> specifies the number
#    of constraints to enforce, if there are any defined in the GRID.  A value
#    of -1 means require all eligible constraints.  Currently, only H-bond and
#    metal constraints can be applied.  If no <int> value is given, any
#    constraints defined in the GRID will be ignored.

ALIGN <TRUE/FALSE>
#    Default is FALSE.  Run 'structalign' on all non-GRID RECEPTORs and
#    COMPLEXes.  The reference for the alignment will be the REFERENCE
#    structure, if defined.  Otherwise, it will be the first COMPLEX
#    listed.  Otherwise, it will be the first RECEPTOR listed.  If the
#    COMPLEX/RECEPTOR is a directory, the first structure found in the
#    specified directory will be used.  Warning: If ALIGN is TRUE when there
#    are LIGANDs associated with RECEPTORs, the RECEPTORs may be moved out of
#    the proper frame of reference for RMSD calculations; the LIGANDs are not
#    ALIGNed.

REFERENCE <file>
#    Reference receptor/complex for alignment.  Not included in the
#    cross-docking unless also listed as a COMPLEX or RECEPTOR.

MAXLIGATOMS <int>
#    Default is 90.  When extracting a ligand from a COMPLEX, the maximum
#    number of atoms for molecules that can be considered ligands.  This is
#    not the same as the DOCK_MAXATOMS setting for Glide.

MINLIGATOMS <int>
#    Default is 12.  When extracting a ligand from a COMPLEX, the minimum
#    number of atoms for molecules that can be considered ligands.

EXCLUDE_IONS <TRUE/FALSE>
#    Default is TRUE.  When extracting a ligand from a COMPLEX, exclude
#    small charged molecules and ions.

EXCLUDE_AMINO_ACIDS <TRUE/FALSE>
#    Default is FALSE.  When extracting a ligand from a COMPLEX, exclude
#    peptides.

EXCLUDED_RESIDUES <list>
#    Default is to use the built-in excluded_residues list of the
#    AslLigandSearcher, consisting of a variety of small molecules that
#    occur in crystal structures but aren't considered ligands (e.g.,
#    SO4, ACY, GOL, NAG).  A list of PDB residue codes can be specified
#    instead.

###############
# Preparation #
###############

PPREP <TRUE/FALSE>
#    Default is FALSE.  Run the command-line Protein Preparation Wizard on
#    all RECEPTORs and COMPLEXes.  The following PPREP_* options apply only
#    if PPREP is TRUE.

PPREP_FIXBONDS <TRUE/FALSE>
#    Default is TRUE.  Assign bond orders to het groups.

PPREP_HTREAT <TRUE/FALSE>
#    Default is TRUE.  Add hydrogens.

PPREP_REHTREAT <TRUE/FALSE>
#    Default is FALSE.  Delete and re-add hydrogens (will reset PDB atom
#    names).

PPREP_TREATMETALS <TRUE/FALSE>
#    Default is TRUE.  Treat metals (e.g., break covalent bonds).

PPREP_CAPTERMINI <TRUE/FALSE>
#    Default is FALSE.  Cap chain termini.

PPREP_KEEPWATERS <TRUE/FALSE>
#    Default is FALSE.  Don't delete waters far from het groups.

PPREP_WATERDIST <float>
#    Default is 5.0 A.  Distance threshhold for 'far' waters.

PPREP_EPIK <TRUE/FALSE>
#    Default is TRUE.  Generate het group states with Epik.  Requires an Epik
#    license.

PPREP_PROTASSIGN <TRUE/FALSE>
#    Default is TRUE.  Run 'protassign' to optimize H-bond networks.

PPREP_PROTASSIGN_EXHAUSTIVE <TRUE/FALSE>
#    Default is FALSE.  Use exhaustive mode.

PPREP_PROTASSIGN_WATER <TRUE/FALSE>
#    Default is TRUE.  Sample waters.

PPREP_IMPREF <TRUE/FALSE>
#    Default is TRUE.  Run 'impref' constrained refinement.

PPREP_IMPREF_RMSD <float>
#    Default is 0.30 A.  RMSD cutoff for 'impref'

PPREP_IMPREF_FIXHEAVY <TRUE/FALSE>
#    Default is FALSE.  Fix heavy atoms during refinement.

LIGPREP <TRUE/FALSE>
#    Default is FALSE.  Run LigPrep on all ligands.  This can generate
#    multiple varaints (ionization and tautomerization states, stereoisomers)
#    for each input ligand.  In the XGlide analysis calculations, a ligand is
#    counted as docking successfully or docking correctly if any of its
#    variants dock successfully or correctly.  Requires a LigPrep license.

LIGPREP_EPIK <TRUE/FALSE>
#    Default is FALSE.  Use Epik instead of the Ionizer to generate ionization
#    states.  Requires an Epik license.

###########
# SiteMap #
###########

SITEMAP <TRUE/FALSE>
#    Default is FALSE.  If GRIDGEN_GRID_CENTER is SELF and there is no
#    ligand associated with a RECEPTOR, use SiteMap to identify the top
#    binding site(s) for defining the grid center(s).  NOTE: Currently,
#    SiteMap jobs will run on 'localhost' even if a remote host/queue
#    is specified for the XGlide job.
SITEMAP_MAXSITES <int>
#    Default is 1.  The maximum number of sites per receptor for which grids
#    will be generated.
SITEMAP_FORCE <TRUE/FALSE>
#   Default is FALSE.  If TRUE, use SiteMap to identify the binding site(s)
#   even if there is a ligand associated with the receptor.

#########
# Glide #
#########

GRIDGEN_<keyword> <value>
# Passes Grid Generation keyword/value pairs to Glide.  See the documentation
# for the $SCHRODINGER/glide simplified input file.  The defaults that XGlide
# sets are:
#     RECEP_VSCALE    1.0
#     RECEP_CCUT      0.25
#     INNERBOX        10
# When multiple values are specified for a keyword, they should be a commma-
# separated list

GRIDGEN_STANDARD_SETTING <TRUE/FALSE>
# This is xglide_mga.py original option made by Ban et al..
# Arrange a grid which has the size of 10A(innerbox) and 30A(outerbox) at centroid
# of sitemap sitepoints.

GRIDGEN_INCLUSION_SETTING <TRUE/FALSE>
# This is xglide_mga.py original option made by Ban et al.
# Arrange a grid, innerbox is the same size of sitemap sitepoints length and outerbox
# is innerbox size + 20A, at centroid of sitemap sitepoints.

GRIDGEN_GREEDY_SETTING <TRUE/FALSE>
# This is xglide_mga.py original option made by Ban et al.
# If you chose TRUE, arrange grids, innerbox size is 10A and outerbox size is 30A,
# at the points which got by greedy algorithm of set cover problem.

GRIDGEN_DIVISION_SETTING <TRUE/FALSE>
# This is xglide_mga.py original option made by Ban et al.
# If you chose TRUE, arrange grids, innerbox size is 10A and outerbox size is 30A,
# at the points arranged like lattice.

GRIDGEN_RANDOM_SETTING <TRUE/FALSE>
# This is xglide_mga.py original option made by Ban et al.
# If you chose TRUE, arrange grids, innerbox size is 10A and outerbox size is 30A,
# at the random chosed points of sitemap sitepoints untile covering sitepoints.

GRIDGEN_GRID_CENTER <AUTO/SELF/x,y,z>
#    GRID_CENTER is a standard Glide keyword, the normal value of which is
#    the X, Y, and Z coordinates of the grid box center.  Alternatively, the
#    value can be AUTO (the default) or SELF.  With AUTO, the grid center for
#    all receptors is set at the centroid of the all pre-positioned LIGANDs;
#    this option should be used only when all the receptors are pre-aligned, or
#    if ALIGN is TRUE.  With SELF, the grid center for each receptor is
#    determined only by the associated ligand (i.e., the native ligand).

GRIDGEN_INNERBOX <size/x,y,z>
#    INNERBOX is a keyword made by Ban et al.

GRIDGEN_OUTERBOX <AUTO/SELF/size/x,y,z>
#    OUTERBOX is a standard Glide keyword, the normal real value of which is
#    the outer grid box dimension (single value for cubic box) or dimensions
#    (x,y,z).  Alternatively, the value can be AUTO (the default) or SELF.
#    With AUTO, the grid size for all receptors is set according to the
#    largest of all the pre-positioned LIGANDs associated with receptors.
#    With SELF, the grid size for each receptor is set according to the sizes
#    of the pre-positioned and associated (i.e., native) ligand or ligands.

GRIDGEN_OUTERBOX_BUFFER <float>
#    If GRIDGEN_OUTERBOX is AUTO or SELF, the grid size will be the sum of
#    the inner box size (default 10), the computed max ligand size, and
#    GRIDGEN_OUTERBOX_BUFFER (default 0.0).  This keyword can be used to make
#    the grid boxes a bit larger in cases where the pre-positioned, associated
#    ligands might be smaller than other ligands that will be docked to the
#    receptors.

DOCK_<keyword> <value>
# Passes Ligand Docking keyword/value pairs to Glide.  See the documentation
# for the $SCHRODINGER/glide simplified input file.  The defaults that XGlide
# sets are:
#     LIG_CCUT        0.15
#     CV_CUTOFF       0.0
#     POSES_PER_LIG   1
#     AMIDE_MODE      penal
#     PRECISION       SP
#     DOCKING_METHOD  confgen
#     WRITE_XP_DESC   FALSE
#     COMPRESS_POSES  TRUE
#     POSE_OUTTYPE    ligandlib
# When multiple values are specified for a keyword, they should be a commma-
# separated list

DOCK_LIG_VSCALE <float/min,max,increment>
#    LIG_VSCALE is a standard Glide keyword, the normal value of which is
#    the ligand vdW scaling factor (default is 0.8).  Alternatively, the value
#    can be three values -- the minimum scaling factor, the maximum scaling
#    factor, and the increment (e.g., "0.5,1.0,0.1").  XGlide then will run
#    docking jobs with this range of scaling factors, and the optimal scaling
#    per receptor will be determined from the number of ligands that dock to
#    2.0 A or less.  Note that the "AUTO" option greatly increases the length
#    of the docking stage (there are 10x the number of subjobs).

DOCK_NUSECONS <int>
#    Apply this many H-bond/metal constraints in the docking jobs.  This value
#    is overridden by number-of-constraint specifications for individual
#    GRIDs.

#################
# Miscellaneous #
#################

NATIVEONLY <TRUE/FALSE>
#    Default is FALSE.  Only dock ligands into the corresponding receptors
#    of COMPLEXes (or RECEPTORs/GRIDs associated with LIGANDs).

SKIP_DOCKING <TRUE/FALSE>
#    Default is FALSE.  Skip the docking and RMSD calculation stages.  Useful
#    for using XGlide just to generate grids.

GOOD_RMSD <float>
#    Default is 2.0 A.  Cutoff for the a "good" ligand RMSD for the summary
#    results and ligand vdW scaling analysis.

GENERATE_TOP_COMPLEXES <int>
#    Default is 0.  If non-zero, produce an output file of complexes
#    representing each input receptor and the ligand pose with the best
#    GlideScore.  This option probably should be used only when docking
#    a single ligand (and perhaps its variants) to a set of receptor
#    structures.  The complexes will be sorted by GlideScore.

MERGE_SUBSET_POSES <TRUE/FALSE>
#    Default is TRUE.  After RMSD calculations are finished, merge the
#    docking results for each receptor/scaling into a single pose file.
#    The subset pose files are archived.  Doesn't apply to NATIVEONLY
#    docking.

"""

_examples_documentation = """
########################################################################
#                                                                      #
#                          XGlide examples                             #
#                                                                      #
#    Some example input files for common usages of XGlide.             #
#                                                                      #
########################################################################

Full MxN docking of M prepared ligands with N prepared grids
------------------------------------------------------------
The input file below cross-docks the 1kms, 1mvs, and 1s3v ligands into
those three receptors.  The ligands and receptors were aligned and prepared
previously, and grids were calculated for the receptors.  Docking is with
Glide SP (i.e., the default), so no PRECISION keyword is needed.  In
addition to the three native ligands, an additional set of 50 ligand is
docked to each receptor; these are not in the proper frame of reference, so
no REFPOSE keyword is used.  The three native ligands have been associated
with the three grids, so RMSD calculations will be performed for them, and
the native redocking results will be marked.

GRID             1kms_grid.zip
GRID             1mvs_grid.zip
GRID             1s3v_grid.zip
LIGAND           1kms_lig.mae,1kms_grid.zip
LIGAND           1mvs_lig.mae,1mvs_grid.zip
LIGAND           1s3v_lig.mae,1s3v_grid.zip
LIGAND           50ligs.mae


Full cross docking with protein and ligand preparation
------------------------------------------------------
In this example, the three complexes are aligned and prepared from the raw
PDB files.  The GRIDGEN_GRID_CENTER grid center keyword is omitted, and it is
AUTO by default, which means the grid box center will be set at the
centroid of the ligands in the aligned complexes.  Note that for 1kms,
there is a NDP cofactor in the complex; however, the first ligand-size
molecule in the file is the LIH ligand, so there is no need to list the
ligand molecule number explicitly on the 1kms COMPLEX line.  We set
PPREP_WATDIST to 0.0 so that all waters are deleted.

COMPLEX          1kms.pdb
COMPLEX          1mvs.pdb
COMPLEX          1s3v.pdb
ALIGN            TRUE
PPREP            TRUE
PPREP_WATERDIST  0.0
LIGPREP          TRUE
LIGPREP_EPIK     TRUE


Native redocking with Glide XP
------------------------------
In this example, we start from the raw PDB files, but we redock just the
native ligands.  We're skipping the alignment step (which isn't necessary
for native redocking), so we have to set GRIDGEN_GRID_CENTER to SELF so the
grid centers are set separately for each receptor from the centroid of the
corresponding native ligand.

COMPLEX              1kms.pdb
COMPLEX              1mvs.pdb
COMPLEX              1s3v.pdb
PPREP                TRUE
PPREP_WATERDIST      0.0
DOCK_PRECISION       XP
GRIDGEN_GRID_CENTER  SELF
NATIVEONLY           TRUE


Docking to receptor with unknown binding site
---------------------------------------------
In this example, the binding site of a receptor is not known.  SiteMap is
used to identify up to three possible binding sites.  Grids are calculated
for each site, and the ligands are docked to each.

RECEPTOR             myrec.mae
LIGAND               myligands.mae
SITEMAP              TRUE
SITEMAP_MAXSITES     3
GRIDGEN_GRID_CENTER  SELF


Docking with core constraint
----------------------------
In this example, a core constraint is applied so that ligands with matching
cores dock with poses overlapping the reference core structure.  Note that
the reference core structure must be in the frame of the receptors, so the
receptors must be aligned.  If the alignment is done by XGlide itself, the
core must be in the frame of the structure used as the alignment reference
(see documentation for the ALIGN keyword).

RECEPTOR                1kms_rec.mae
RECEPTOR                1mvs_rec.mae
LIGAND                  ligands.mae
DOCK_USE_REF_LIGAND     1
DOCK_REF_LIGAND_FILE    core.mae
DOCK_CORE_RESTRAIN      1
DOCK_CORE_POS_MAX_RMSD  2.0


Docking with H-bond/metal/hydrophobic constraints with default features
-----------------------------------------------------------------------
In this example, H-bond and hydrophobic constraints from an existing grid
are enforced during docking, using the default ligand features (e.g.,
"Donor") for the constraint type.  The DOCK_USE_CONS value must be a
comma-separated list (no spaces) of constraint labels from the Glide grid.
DOCK_NREQUIRED_CONS is the number of specified constraints that each
successfully-docked ligand must match.

GRID                 1ett_grid.zip
LIGAND               50ligs.mae.gz
DOCK_PRECISION       HTVS
DOCK_USE_CONS        H:ASP:189:OD2(hbond),region1
DOCK_NREQUIRED_CONS  2


Docking with constraints (e.g., positional) with custom ligand features
-----------------------------------------------------------------------
In this example, constraints with non-default or custom ligand features,
as required for positional constraints, are enforced. The Glide feature
file is not designed to be written from scratch, so using an existing
.feat file (e.g., written by Maestro after setting up a constrained
docking job in Maestro) is recommended.

GRID                       factorXa_grid.zip
LIGAND                     50ligs.mae.gz
DOCK_PRECISION             HTVS
DOCK_GLIDECONS             YES
DOCK_GLIDEUSECONSFEAT      YES
DOCK_HAVEGLIDECONSFEAT     YES
DOCK_GLIDE_CONS_FEAT_FILE  custom.feat

"""


# TO DO: Finish unimplemented features.
#        Decide what intermediate files to return for REMOTEDRIVER jobs.
#        Track stage times.
#        Print ligands per subset.
#        Report ligands that don't dock successfully.
#        Output matrix format results, perhaps graphically or CSV.
#        Decide what to do if <jobname>_workdir already exists.
#
# LIGAND_ID/RECEPTOR_ID        ***Not yet implemented***
#    Perhaps there should be a way to indicate the label for receptor or
#    ligand.  If the titles aren't unique, the RSMD table will be ambiguous,
#    so some other ID must be used (file+index? property?).  The default
#    should be TITLE.
#
# CSEARCH <TRUE/FALSE>         ***Not yet implemented***
#    Default is FALSE.  Run MacroModel CSearch on all ligands
#
# Notes: It would be good to add more ligand subset control, like VSW.
#        For example, automatically choosing subsets within certain ranges
#        for different Glide precisions.



################################################################################
# Packages
################################################################################
import schrodinger.job.jobcontrol as jobcontrol
import schrodinger.job.launcher as launcher
import schrodinger.job.app as app
import schrodinger.structure as structure
import schrodinger.structutils.analyze as analyze
import schrodinger.structureutil as structureutil
import schrodinger.job.queue as jobdj
import schrodinger.application.glide.glide as glide
import schrodinger.utils.log
import schrodinger.utils.cmdline as cmdline
import schrodinger.utils.fileutils as futils
import schrodinger.infra.mm as mm
import sys, os, shutil, time, logging, glob, tarfile, subprocess, zipfile, random # random is insarted by Ban et al.


################################################################################
# Globals/Constants 
################################################################################
_version = "$Revision: 3.5 $"
_copyright = "Copyright Schrodinger, LLC. All rights reserved."
_jobapp = 0   # Job application instance
# Check version
_require_version = 35207    # Command-line PPW was added in 2007 update1
schrodinger.version_at_least(_require_version)

# Check if we are running within Maestro
try:
    import schrodinger.maestro.maestro as maestro
except ImportError:
    maestro = None

# Logging
logger = schrodinger.utils.log.get_output_logger("xglide")
logger.setLevel(logging.INFO)

# Add file type and extensions for Glide grids
futils.GLIDEGRID = 'glidegrid'
futils.EXTENSIONS[futils.GLIDEGRID] = ['.grd','.zip']
def get_structure_file_format(filename):
    """
    Replaces the futils version so Grid files are recognized.
    """
    fmt = futils.get_structure_file_format(filename)
    if not fmt:
        basename, ext = futils.splitext(filename.lower())
        if ext in futils.EXTENSIONS[futils.GLIDEGRID]:
            return futils.GLIDEGRID
    return fmt
        
###############################################################################
# Functions 
################################################################################
def show_panel():
    """Display graphical user interface to conf_cluster."""
    global _jobapp
    if _jobapp:
        # Don't create a new application instance if one exists
        _jobapp.gui()
    else:
        # Create main window
        start_app("-gui")


def quit_panel():
    """
    Closes the GUI panel.  Destroys the GUI, not just a simple withdraw().

    """
    global _jobapp
    if _jobapp:
        _jobapp.destroy_gui()


def start_app(args):
    """ Create the App instance """
    global _jobapp
    _jobapp = XGlideApp(__file__,args)
    _jobapp.run()


################################################################################
# Classes 
################################################################################

class _FileTracker:
    """
    Base class for convenience classes that track the file/job names
    associated with particular input files.
    """

    FORMATS = [futils.MAESTRO]       # Override this in derived classes

    def __init__(self,file,index=None):
        self.extensionCheck(file)
        self._history = [file]
        self._reference = file
        self._basename = futils.get_basename(self._history[0])
        self.index = index

    def extensionCheck(self,file):
        if not os.path.exists(file):
            raise Exception("File '%s' does not exist" % file)
        if os.path.isdir(file):
            return
        if get_structure_file_format(file) not in self.FORMATS:
            raise Exception("File '%s' is not the proper format." % file)

    def changeBasename(self,base=None,file=None):
        if base:
            self._basename = base
        elif file:
            self._basename = futils.get_basename(file)
        else:
            raise Exception("No basename or file specified.")

    def update(self,file,reference=False):
        self._history.append(file)
        if reference:
            self._reference = file

    def getOriginalFilename(self):
        return self._history[0]

    def getReferenceFilename(self):
        return self._reference

    def getCurrentFilename(self):
        return self._history[-1]

    def getBasename(self):
        """
        Return the base name (without path or extension) of the original file.
        """
        return self._basename

    def expand(self):
        """
        If the original file is a directory, return objects of the same class
        for all suitable files in that directory.
        """
        currfile = self._history[-1]
        newfiles = []
        if os.path.isdir(currfile):
            dirfiles = []
            for fmt in self.FORMATS:
                for ext in futils.EXTENSIONS[fmt]:
                    dirfiles.extend(glob.glob(os.path.join(currfile,"*"+ext)))
            for f in dirfiles:
                newfiles.append(self.__class__(f))
        elif os.path.isfile(currfile):
            newfiles.append(self.__class__(currfile))
        else:
            raise IOError("Error: File '%s' not found." % currfile)
        return newfiles

    def printMe(self):
        print "%s.printMe()" % self.__class__
        print "Basename: %s" % self._basename
        print "History:"
        for ifile in self._history:
            if ifile==self._reference:
                print "    %s (reference)" % ifile
            else:
                print "    %s" % ifile
        print "Extensions: ",self.FORMATS

class _Complex(_FileTracker):
    FORMATS = [futils.MAESTRO,futils.PDB]
    def __init__(self,file):
        _FileTracker.__init__(self,file)
        self.receptor = None
        self.ligand = []
        self.ligasl = None   # ASL for the the ligand
    def expand(self):
        """
        Override the base class method so the extra properties are propagated
        to the all the complex files in the directory.
        """
        newfiles = _FileTracker.expand(self)
        for cfile in newfiles:
            cfile.receptor = self.receptor
            cfile.ligand.extend(self.ligand)
            cfile.ligasl = self.ligasl
        return newfiles
    def printMe(self):
        _FileTracker.printMe(self)
        if self.receptor:
            print "Receptor: %s" % self.receptor._basename
        if self.ligasl!=None:
            print "Ligand ASL: %s" % self.ligasl
        for lig in self.ligand:
            print "Ligand: %s" % lig._basename

class _Receptor(_FileTracker):
    FORMATS = [futils.MAESTRO,futils.PDB]
    def __init__(self,file):
        _FileTracker.__init__(self,file)
        self.ligand = []
        self.complex = None
        self.sites = None
    def expand(self):
        """
        Override the base class method so the extra properties are propagated
        to the all the receptor files in the directory.
        """
        newfiles = _FileTracker.expand(self)
        for rfile in newfiles:
            rfile.ligand.extend(self.ligand)
            rfile.complex = self.complex
            rfile.sites = self.sites
        return newfiles
    def printMe(self):
        _FileTracker.printMe(self)
        for lig in self.ligand:
            print "Ligand: %s" % lig._basename
        if self.complex:
            print "Complex: %s" % self.complex._basename
        if self.sites:
            print "Sites: %s" % self.sites

class _Ligand(_FileTracker):
    FORMATS = [futils.MAESTRO,futils.PDB,futils.SD]
    def __init__(self,file,refpose=False):
        _FileTracker.__init__(self,file)
        self.receptor = None
        self.complex = None
        self.grid = None
        self.refpose = refpose
    def expand(self):
        """
        Override the base class method so the extra properties are propagated
        to the all the ligand files in the directory.
        """
        newfiles = _FileTracker.expand(self)
        for lfile in newfiles:
            lfile.receptor = self.receptor
            lfile.complex = self.complex
            lfile.grid = self.grid
            lfile.refpose = self.refpose
        return newfiles
    def printMe(self):
        _FileTracker.printMe(self)
        if self.receptor:
            if isinstance(self.receptor,_FileTracker):
                print "Receptor: %s" % self.receptor._basename
            else:
                print "Receptor: %s" % self.receptor
        if self.complex:
            print "Complex: %s" % self.complex._basename
        if self.grid:
            print "Grid: %s" % self.grid._basename
        print "Refpose: %s" % self.refpose

class _Grid(_FileTracker):
    FORMATS = [futils.GLIDEGRID]
    def __init__(self,file,usecons=0):
        _FileTracker.__init__(self,file)
        self.usecons = usecons     # Number of constraints to enforce
        self.receptor = None
        self.ligand = []
    def isZipped(self):
        base,ext = futils.splitext(self._history[-1])
        if ext==".zip":
            return True
        else:
            return False
    def expand(self):
        """
        Override the base class method so the extra properties are propagated
        to the all the grid files in the directory.
        """
        newfiles = _FileTracker.expand(self)
        for gfile in newfiles:
            gfile.usecons = self.usecons
            gfile.receptor = self.receptor
            gfile.ligand = self.ligand
        return newfiles
    def printMe(self):
        _FileTracker.printMe(self)
        if self.usecons:
            print "Usecons: %s" % self.usecons
        if self.receptor:
            print "Receptor: %s" % self.receptor._basename
        for lig in self.ligand:
            print "Ligand: %s" % lig._basename

class MyAslLigandSearcher(analyze.AslLigandSearcher):
    """
    Subclass to workaround PYTHON-2437
    """
    def getAsl(self):
        """
        Get a default ASL for matching putative ligands.  The default ASL is
        based on molecule size, and excludes amino acids and certain known small
        molecules.  See exclusion list in L{__init__}.
        @rtype: str
        @return: an ASL expression to match putative ligands.
        """

        size_clause = "(m.atoms %d-%d)" % (
            self.min_atom_count,
            self.max_atom_count
        )

        exclude_clause = []
        # Add HXT to backbone atoms
        backbone = "((res.pt ACE) OR (atom.pt ca,c,n,o,oxt,hxt OR (a.e H and withinbonds 1 atom.pt ca, n)) and not (res.pt hoh or res.pt spc or res.pt t4p or res.pt t3p or res.pt DPPC, POPC, POPE, DMPC, DOPC, DOPS, POPS, DPPS, DMPS, DPPE, DMPE, DOPE,  POPE, PIP, POPA, DOPA, DMPA, DPPA))"
        if self.exclude_amino_acids:
            exclude_clause.append('(sidechain) or (%s)' % backbone)
        if self.exclude_ions:
            exclude_clause.append('(ions)')

        if self.excluded_residues:
            exclude_clause.append(
                "(res.pt %s)" % " ".join(self.excluded_residues)
            )

        asl = "%s" % size_clause
        if exclude_clause:
            asl = "((%s) and not (%s))" % (
                size_clause,
                " or ".join(exclude_clause)
            )

        analyze.logger.debug("MyAslLigandSearcher.getAsl: %s" % asl)
        return asl
 

class XGlideApp(app.App):

    """
    Application for running the XGlide GUI and for running the backend
    under job control.  App requires 'commandLine', 'backend', and 'gui'
    methods.

    """
    GSCOREPROP = 'r_i_docking_score'  # GlideScore and Epik state penalty
    JOBEXTS = {'ALIGN_REF':'refalign',
               'ALIGN_PRE':'prealign',
               'ALIGN':'align',
               'CONVERT':'convert',
               'PPREP':'pprep',
               'SPLIT_REC':'rec',
               'SPLIT_LIG':'lig',
               'LIGPREP':'ligprep',
               'SITEMAP':'sitemap',
               'GRID':'grid',
               'DOCK':'dock'}
    # Stages
    (ALIGN,
     CONVERT,
     PPREP,
     SPLIT,
     SUBSET,
     LIGPREP,
     CSEARCH,
     SITEMAP,
     GRID,
     DOCK,
     RMS,
     GENTOPCOMPLEXES,
     MERGE) = range(1,14)  # 0 is reserved for new jobs

    def error(self,text):
        """
        Log an error message.
        """
        logger.error(text)

    def warning(self,text):
        """
        Log a warning message.
        """
        logger.warning(text)

    def info(self,text):
        """
        Log an info message.  This is used for standard job output.
        """
        logger.info(text)

    def debug(self,text):
        """
        Log a debug message.
        """
        logger.debug(text)

    def setDefaults(self):
        """
        Set the default parameters for the XGlide job.
        """
        # Input structure settings
        self.complexes = []
        self.receptors = []
        self.ligands = []
        self.ligandisnative = []
        self.grids = []
        self.align = False
        self.reference = None
        self.maxligatoms = 90
        self.minligatoms = 12
        self.exclude_ions = True
        self.exclude_amino_acids = False
        self.excluded_residues = None
        # Structure preparation settings
        self.pprep = False
        self.pprep_impref = True
        self.pprep_impref_rmsd = 0.30
        self.pprep_impref_fixheavy = False
        self.pprep_captermini = False
        self.pprep_keepwaters = False
        self.pprep_waterdist = 5.0
        self.pprep_treatmetals = True
        self.pprep_fixbonds = True
        self.pprep_htreat = True
        self.pprep_rehtreat = False
        self.pprep_epik = True
        self.pprep_protassign = True
        self.pprep_protassign_exhaustive = False
        self.pprep_protassign_water = True
        self.ligprep = False
        self.ligprep_epik = False
        self.csearch = False
        self.sitemap = False
        self.sitemap_maxsites = 1
        self.sitemap_force = False
        # Glide settings
        # Should we use the glide.py defaults?  Keep the XGlide defaults for
        # now.
        self.gridkeywords = {"RECEP_VSCALE":1.0,
                             "RECEP_CCUT":0.25,
                             "INNERBOX":10}
        self.dockkeywords = {"LIG_VSCALE":0.8,
                             "LIG_CCUT":0.15,
                             "CV_CUTOFF":0.0,
                             "POSES_PER_LIG":1,
                             "AMIDE_MODE":glide.PENALIZE,
                             "PRECISION":glide.SP,
                             "DOCKING_METHOD":"confgen",  # No module constant
                             "WRITE_XP_DESC":"FALSE",
                             "COMPRESS_POSES":"TRUE",
                             "POSE_OUTTYPE":"ligandlib"}
        self.gridcenter = "AUTO"
        self.gridsize = "AUTO"
        # *************************************************************************
        # These options(INCLUSION,DISPERSION,LATTICE,RANDOM) made by Ban et al.
        # *************************************************************************
        self.innerboxsize = 10    # xglide_mga.py original option
        self.gridgenStandardSetting = False # xglide_mga.py original option
        self.gridgenInclusionSetting = False # xglide_mga.py original option
        self.gridgenGreedySetting = False # xglide_mga.py original option
        self.gridgenLatticeSetting = False # xglide_mga.py original option
        self.gridgenRandomSetting = False # xglide_mga.py original option
        # *************************************************************************
        self.gridsize_buffer = 0.0
        self.lvdw_autoscale = False
        self.lvdw_autoscale_min = 0.1
        self.lvdw_autoscale_max = 1.0
        self.lvdw_autoscale_inc = 0.1
        self.nusecons = 0
        # Miscellaneous settings
        self.nativeonly = False
        self.skipdocking = False
        self.goodrmsd = 2.0
        self.generatecomplexes = 0
        self.mergesubsetposes = True
        self.jdj = None    # Need class attribute for JobDJ restartability
        self.stage_completed = 0
        self.lig_scaling = []
        return

    def readInputFile(self):
        """
        Read the input file and set the appropriate instance attributes.
        """
        for line in open(self.inputfile,'r').readlines():
            if not line.strip() or line.startswith("#"):
                continue
            s = line.split(None,1)
            if not len(s)==2:
                print "Error: Improper format, keyword/value pair expected"
                print "Line: %s" % line
                sys.exit(1)
            keyword = s[0]
            value = s[1].strip()
            # Input structure settings
            if keyword=="COMPLEX":
                ligasl = None
                values = value.split(",")
                if len(values)>2:
                    print "Error: Too many values for COMPLEX entry"
                    print "Line: %s" % line
                    sys.exit(1)
                elif len(values)==2:
                    ligasl = values[1]
                    # If it's an integer, intepret as a molecule number, for
                    # backwards compatibility.
                    try:
                        ligasl = "mol.num %s" % int(ligasl)
                    except:
                        pass
                if values[0] not in [x.getOriginalFilename() for x in self.complexes]:
                    self.complexes.append(_Complex(values[0]))
                    self.complexes[-1].ligasl = ligasl
            elif keyword=="RECEPTOR":
                if value not in [x.getOriginalFilename() for x in self.receptors]:
                    self.receptors.append(_Receptor(value))
            elif keyword=="LIGAND":
                refpose = False
                assoc_receptor = None
                values = value.split(",")
                if "REFPOSE" in values:
                    refpose = True
                    values.remove("REFPOSE")
                if "NATIVE" in values:
                    refpose = True
                    values.remove("NATIVE")
                    print "Warning: The use of the NATIVE option for LIGAND"
                    print "         entries is deprecated.  Use REFPOSE instead."
                    print "Line: %s" % line
                if len(values) > 2:
                    print "Error: Too many values for LIGAND entry"
                    print "Line: %s" % line
                    sys.exit(1)
                elif len(values)==2:
                    # This associates the ligand file with a receptor/grid,
                    # but no longer makes them reference poses automatically;
                    # use REFPOSE for that.
                    assoc_receptor = values[1]
                if values[0] not in [x.getOriginalFilename() for x in self.ligands]:
                    self.ligands.append(_Ligand(values[0],refpose))
                    # This will be turned into a _FileTracker later.
                    self.ligands[-1].receptor = assoc_receptor
            elif keyword=="GRID":
                usecons = 0
                values = value.split(",")
                if len(values) > 2:
                    print "Error: Too many values for GRID entry"
                    print "Line: %s" % line
                    sys.exit(1)
                elif len(values)==2:
                    usecons = int(values[1])
                    if usecons<-1 or usecons>4:
                        print "Error: Number of constraints must be in range [-1,4]"
                        print "Line: %s" % line
                        sys.exit(1)
                if values[0] not in self.grids:
                    self.grids.append(_Grid(values[0],usecons))
            elif keyword=="ALIGN":
                if value.lower() in ("true","t"):
                    self.align = True
            elif keyword=="REFERENCE":
                self.reference = _Receptor(value)
            elif keyword=="MAXLIGATOMS":
                self.maxligatoms = int(value)
            elif keyword=="MINLIGATOMS":
                self.minligatoms = int(value)
            elif keyword=="EXCLUDE_IONS":
                if value.lower() in ("false","f"):
                    self.exclude_ions = False
            elif keyword=="EXCLUDE_AMINO_ACIDS":
                if value.lower() in ("true","t"):
                    self.exclude_amino_acids = True
            elif keyword=="EXCLUDED_RESIDUES":
                values = value.split(",")
                self.excluded_residues = [x.strip() for x in values]
            # Structure preparation settings
            elif keyword=="PPREP":
                if value.lower() in ("true","t"):
                    self.pprep = True
            elif keyword=="PPREP_IMPREF":
                if value.lower() in ("false","f"):
                    self.pprep_impref = False
            elif keyword=="PPREP_IMPREF_RMSD":
                self.pprep_impref_rmsd = float(value)
            elif keyword=="PPREP_IMPREF_FIXHEAVY":
                if value.lower() in ("true","t"):
                    self.pprep_impref_fixheavy = True
            elif keyword=="PPREP_FIXBONDS":
                if value.lower() in ("false","f"):
                    self.pprep_fixbonds = False
            elif keyword=="PPREP_CAPTERMINI":
                if value.lower() in ("true","t"):
                    self.pprep_captermini = True
            elif keyword=="PPREP_KEEPWATERS":
                if value.lower() in ("true","t"):
                    self.pprep_keepwaters = True
            elif keyword=="PPREP_WATERDIST":
                self.pprep_waterdist = float(value)
            elif keyword=="PPREP_TREATMETALS":
                if value.lower() in ("false","f"):
                    self.pprep_treatmetals = False
            elif keyword=="PPREP_HTREAT":
                if value.lower() in ("false","f"):
                    self.pprep_htreat = False
            elif keyword=="PPREP_REHTREAT":
                if value.lower() in ("true","t"):
                    self.pprep_rehtreat = True
            elif keyword=="PPREP_EPIK":
                if value.lower() in ("false","f"):
                    self.pprep_epik = False
            elif keyword=="PPREP_PROTASSIGN":
                if value.lower() in ("false","f"):
                    self.pprep_protassign = False
            elif keyword=="PPREP_PROTASSIGN_EXHAUSTIVE":
                if value.lower() in ("true","t"):
                    self.pprep_protassign_exhaustive = True
            elif keyword=="PPREP_PROTASSIGN_WATER":
                if value.lower() in ("false","f"):
                    self.pprep_protassign_water = False
            elif keyword=="LIGPREP":
                if value.lower() in ("true","t"):
                    self.ligprep = True
            elif keyword=="LIGPREP_EPIK":
                if value.lower() in ("true","t"):
                    self.ligprep_epik = True
            elif keyword=="CSEARCH":
                if value.lower() in ("true","t"):
                    self.csearch = True
            # SiteMap settings
            elif keyword=="SITEMAP":
                if value.lower() in ("true","t"):
                    self.sitemap = True
            elif keyword=="SITEMAP_MAXSITES":
                self.sitemap_maxsites = int(value)
            elif keyword=="SITEMAP_FORCE":
                if value.lower() in ("true","t"):
                    self.sitemap_force = True
            # Glide settings
            elif keyword.startswith("GRIDGEN_"):
                key = keyword[8:]
                if key=="GRID_CENTER":
                    # This intercepts the normal glide.py keyword, so we can use
                    # the "AUTO" and "SELF" methods for determining the grid
                    # center.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["AUTO","SELF"]:
                        self.gridcenter = values[0]
                    elif len(values)==3:
                        # Coordinates
                        self.gridcenter = (float(values[0]),
                                           float(values[1]),
                                           float(values[2]))
                    else:
                        print "Error: Unrecognized grid box center specification."
                        print "Line: %s" % line
                        sys.exit(1)
            
                # *************************************************************************
                # These options(INCLUSION,GREEDY,LATTICE,RANDOM) made by Ban et al.
                # *************************************************************************
                
                elif key=="INNERBOX":
                    values = value.split(",")
                    if len(values)==1:
                        # Size (cubic)
                        self.innerboxsize = int(values[0])
                        self.gridkeywords["INNERBOX"] = self.innerboxsize
                    elif len(values)==3:
                        # Size (x,y,z dimensions)
                        self.innerboxsize = (int(values[0]),
                                             int(values[1]),
                                             int(values[2]))
                        self.gridkeywords["INNERBOX"] = self.innerboxsize
                    else:
                        print "Error: Unrecognized grid box size specification at INNERBOX."
                        print "Line: %s" % line
                        sys.exit(1)
                
                # *************************************************************************
            
                elif key=="OUTERBOX":
                    # This intercepts the normal glide.py keyword, so we can use
                    # the "AUTO" and "SELF" methods for determining the grid
                    # size.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["AUTO","SELF"]:
                        self.gridsize = values[0]
                    elif len(values)==1:
                        # Size (cubic)
                        self.gridsize = float(values[0])
                    elif len(values)==3:
                        # Size (x,y,z dimensions)
                        self.gridsize = (float(values[0]),
                                         float(values[1]),
                                         float(values[2]))
                    else:
                        print "Error: Unrecognized grid box size specification."
                        print "Line: %s" % line
                        sys.exit(1)
                elif key=="OUTERBOX_BUFFER":
                    self.gridsize_buffer = float(value)
                
                # *************************************************************************
                # These options(INCLUSION,GREEDY,LATTICE,RANDOM) made by Ban et al.
                # *************************************************************************
                
                elif key=="STANDARD_SETTING":
                    # GRIDGEN_INCLUSION_SETTING is xglide_mga.py original option.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["TRUE"]:
                        self.gridgenStandardSetting = True
                
                elif key=="INCLUSION_SETTING":
                    # GRIDGEN_INCLUSION_SETTING is xglide_mga.py original option.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["TRUE"]:
                        self.gridgenInclusionSetting = True
                
                elif key=="GREEDY_SETTING":
                    # GRIDGEN_GREEDY_SETTING is xglide_mga.py original option.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["TRUE"]:
                        self.gridgenGreedySetting = True
                
                elif key=="LATTICE_SETTING":
                    # GRIDEN_LATTICE_SETTING is xglide_mga.py original option.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["TRUE"]:
                        self.gridgenLatticeSetting = True

                elif key=="RANDOM_SETTING":
                    # GRIDGEN_RANDOM_SETTING is xglide_mga.py original option.
                    values = value.split(",")
                    if len(values)==1 and values[0] in ["TRUE"]:
                        self.gridgenRandomSetting = True

                # *************************************************************************
                else:
                    self.gridkeywords[key] = value.split(",")
                    # If not multi-valued, don't use a list
                    if len(self.gridkeywords[key])==1:
                        self.gridkeywords[key] = self.gridkeywords[key][0]

            elif keyword.startswith("DOCK_"):
                key = keyword[5:]
                if key=="LIG_VSCALE":
                    # This intercepts the normal glide.py keyword, so we can use
                    # a min,max,inc tuple for autoscaling.
                    values = value.split(",")
                    if len(values)==1:
                        # Simple scaling
                        self.dockkeywords[key] = float(values[0])
                    elif len(values)==3:
                        # Autoscaling
                        self.lvdw_autoscale = True
                        self.lvdw_autoscale_min = float(values[0])
                        self.lvdw_autoscale_max = float(values[1])
                        self.lvdw_autoscale_inc = float(values[2])
                    else:
                        print "Error: Need a single value for the ligand vdW scaling, or min"
                        print "       max, and increment values for ligand vdW autoscaling."
                        print "Line: %s" % line
                        sys.exit(1)
                elif key=="NUSECONS":
                    # Use the specified number of eligible constraints from
                    # the grid(s).  This is set directly in the Dock object
                    # rather than being passed to the backend.
                    self.nusecons = int(value)
                else:
                    self.dockkeywords[key] = value.split(",")
                    # If not multi-valued, don't use a list
                    if len(self.dockkeywords[key])==1:
                        self.dockkeywords[key] = self.dockkeywords[key][0]
            # Miscellaneous settings
            elif keyword=="NATIVEONLY":
                if value.lower() in ("true","t"):
                    self.nativeonly = True
            elif keyword=="SKIP_DOCKING":
                if value.lower() in ("true","t"):
                    self.skipdocking = True
            elif keyword=="GOOD_RMSD":
                self.goodrmsd = float(value)
            elif keyword=="GENERATE_TOP_COMPLEXES":
                self.generatecomplexes = int(value)
            elif keyword=="MERGE_SUBSET_POSES":
                if value.lower() in ("false","f"):
                    self.mergesubsetposes = False
            # Obsolete keywords
            elif keyword in ("IMPREF","IMPREF_RMSD","FIX_BONDS","PROTASSIGN",
                             "PPREP_FIXFORPRIME","RVDW","RECCUT",
                             "INNER_BOX_SIZE","OUTER_BOX_SIZE","XCENT","YCENT",
                             "ZCENT","LVDW","LIGCCUT","CV_CUTOFF","MAXPERLIG",
                             "AMIDE_MODE","PRECISION","MODE","XP_DESC"):
                print "Error: Obsolete keyword '%s'" % keyword
                print "       Please run XGlide with '-doc' to see the full list of keywords."
                sys.exit(1)
            else:
                print "Error: Unrecognized keyword '%s'" % keyword
                sys.exit(1)
        # If running SiteMap to identify binding sites, the GRIDGEN_GRIDCENTER
        # must be set to SELF and the GRIDGEN_OUTERBOX cannot be AUTO.
        if self.sitemap:
            if self.gridcenter!="SELF":
                print "Warning: Must use SELF for GRIDGEN_GRID_CENTER when using SiteMap"
                print "         for binding sites.  Adjusting."
                self.gridcenter = "SELF"
            if self.gridsize=="AUTO":
                print "Warning: Can't use AUTO for GRIDGEN_OUTERBOX when using SiteMap"
                print "         for binding sites.  Adjusting to SELF."
                self.gridsize = "SELF"
        # If WRITE_XP_DESC is TRUE, make sure that the output is in PV format
        if self.dockkeywords["WRITE_XP_DESC"].lower() in ["true","yes","1"]:
            if self.dockkeywords["POSE_OUTTYPE"]!='poseviewer':
                print "Warning: Generating Glide XP descriptors requires 'poseviewer' output."
                print "         Adjusting DOCK_POSE_OUTTYPE parameter."
                self.dockkeywords["POSE_OUTTYPE"] = 'poseviewer'
        # Determine the Glide output file format
        if self.dockkeywords["POSE_OUTTYPE"]=="ligandlib":
            self.glide_output_extension = "_lib"
        else:
            self.glide_output_extension = "_pv"
        if self.dockkeywords["COMPRESS_POSES"]=="TRUE":
            self.glide_output_extension += ".maegz"
        else:
            self.glide_output_extension += ".mae"
        if self.nativeonly and self.ligprep:
            print "Error: LigPrep cannot be run in a NATIVEONLY job, because"
            print "       there currently is no way to match the multiple"
            print "       docked states against the input reference structures"
            print "       for RMSD calcualtions."
            sys.exit(1)
        if self.generatecomplexes:
            if self.lvdw_autoscale:
                print "Error: Generating top complexes is not compatible with"
                print "       ligand vdW autoscaling."
                sys.exit(1)
            if self.dockkeywords["POSE_OUTTYPE"]=="ligandlib":
                print "Error: Generating top complexes is not compatible with"
                print "       producing 'lib' Glide output files."
                sys.exit(1)
            if self.nativeonly:
                print "Error: Generating top complexes is not compatible with"
                print "       native-only docking."
                sys.exit(1)
        return

    def printFiles(self):
        if self.complexes:
            print "Complexes"
            print "---------"
            for f in self.complexes:
                f.printMe()
            print ""
        if self.receptors:
            print "Receptors"
            print "---------"
            for f in self.receptors:
                f.printMe()
            print ""
        if self.ligands:
            print "Ligands"
            print "-------"
            for f in self.ligands:
                f.printMe()
            print ""
        if hasattr(self,'ligandsubsets'):
            print "Ligand subsets"
            print "--------------"
            for f in self.ligandsubsets:
                f.printMe()
                if hasattr(f,'subsetorigin'):
                    print "Subset origin:"
                    for lfile,(start,end) in f.subsetorigin:
                        print "    %s  (%8d,%8d)" % (lfile.getCurrentFilename(),start,end)
            print ""
        if self.grids:
            print "Grids"
            print "-----"
            for f in self.grids:
                f.printMe()
            print ""

    def checkReceptorAssociations(self):
        """
        Check that a receptor file associated with a LIGAND is
        a file, not a directory, and matches a RECEPTOR or GRID.  This
        is a startup test only; the _FileTracker cross-references won't
        be made until the backend.
        """
        for lfile in self.ligands:
            if lfile.receptor:
                if not os.path.isfile(lfile.receptor):
                    print ""
                    print "Error: Receptor/grid file '%s' associated with" % lfile.receptor
                    print "       LIGAND '%s' is not a regular file." % lfile.getBasename()
                    print ""
                    sys.exit(1)
                match_index = -1
                for index,rfile in enumerate(self.receptors):
                    if lfile.receptor==rfile.getOriginalFilename():
                        match_index = index
                        break
                if match_index>=0:
                    lfile.receptor = match_index
                    continue
                for index,gfile in enumerate(self.grids):
                    if lfile.receptor==gfile.getOriginalFilename():
                        match_index = index
                        break
                if match_index>=0:
                    lfile.receptor = None
                    lfile.grid = match_index
                    continue
                else:
                    print ""
                    print "Error: Receptor/grid file '%s' for LIGAND" % lfile.receptor
                    print "       '%s' does not match a RECEPTOR or GRID." % lfile.getBasename()
                    print ""
                    sys.exit(1)
        return

    def expandDirectories(self,files):
        """
        Expand all _FileTracker objects that are directories.  Return a list
        of new objects for the directory contents.
        """
        newfiles = []
        for f in files:
            newfiles.extend(f.expand())
        return newfiles

    def checkFilenames(self):
        """
        Check that the files exist.  Note that this check prevents the
        specification of files that exist only on the intended compute
        host.  The filenames (excluding paths) cannot be identical, or Job
        Control could copy multiple files to the same scratch directory file.
        """
        for iindex,ifile in enumerate(self.complexes+self.receptors+
                                      self.ligands+self.grids):
            ifilename = ifile.getOriginalFilename()
            if not os.path.isfile(ifilename):
                print ""
                print "Error: File '%s' does not exist" % ifilename
                print ""
                sys.exit(1)
            for jindex,jfile in enumerate(self.complexes+self.receptors+
                                          self.ligands+self.grids):
                if jindex<=iindex:
                    continue
                jfilename = jfile.getOriginalFilename()
                # Check that the original files have different names.  Note
                # that we disallow this even if they refer to the same
                # physical file, because that would mean duplicate subjobs
                # later.
                if os.path.basename(ifilename)==os.path.basename(jfilename):
                    print ""
                    print "Error: Multiple input files have the name '%s'." % ifilename
                    print ""
                    sys.exit(1)
        return

    def getParser(self):
        """
        Return an OptionParser for the application.
        """
        # There should be an App parser to which these options get added.
        parser = cmdline.SingleDashOptionParser(
            usage="$SCHRODINGER/run %prog [options] <input_file>",
            version_source=__doc__
        )
        parser.add_option(
            "-doc",
            action="store_true",
            dest="doc",
            help="Print documentation of the input file format.  Job will not run."
        )
        parser.add_option(
            "-examples",
            action="store_true",
            dest="examples",
            help="Print sample XGlide input files.  Job will not run."
        )
        parser.add_option(
            "-verbose",
            action="store_true",
            default=False,
            dest="verbose",
            help="Increase verbosity level"
        )
        parser.add_option(
            "-NJOBS",
            action="store",
            type="int",
            default=1,
            dest="njobs",
            help="Number of LigPrep subjobs and number of Glide subjobs per receptor.  Doesn't apply to NATIVEONLY jobs."
        )
        parser.add_option(
            "-REMOTEDRIVER",
            action="store_true",
            default=False,
            dest="remotedriver",
            help="Run the driver on the first -HOST compute host instead of on the local machine.  Note: Most intermediate job files will not be transferred back to the launch directory.  By default, XGlide always runs the driver locally, and with -LOCAL, to preserve the intermediate files and directory structure."
        )
        # The -SAVE and -DEBUG options are parsed by App, but they get passed
        # on to this method, so we must catch them.
        #parser.add_option(
        #    "-SAVE",
        #    action="store_true",
        #    help="Save contents of scratch directories"
        #)
        #parser.add_option(
        #    "-DEBUG",
        #    action="store_true",
        #    help="Show details of Job Control activity"
        #)
        # The following are top-level/App options that never reach this point,
        # but we add them because they won't be included in the usage
        # otherwise.
        #parser.add_option(
        #    "-HOST",
        #    metavar="<host>:<ncpu>",
        #    help="List of hosts to which subjobs are sent.  Default is 'localhost:1'."
        #)
        jc_opts = [
            cmdline.HOSTLIST,
            cmdline.SAVE,
            cmdline.DEBUG
        ]
        cmdline.add_jobcontrol_options(parser,options=jc_opts)
        self.addCommandLineOptions(parser,distributed=True,use_group=True)
        return parser

    def commandLine(self,inargs):
        """
        Required by App.  Parse the application-specific command-line
        arguments (and the main input file), register input/output files, and
        set instance attributes for backend usage.  Return unused arguments
        [this may not be necessary anymore, since backend() doesn't accept
        arguments].

        """
        parser = self.getParser()
        options,args = parser.parse_args(args=inargs)
        if options.doc:
            print _input_file_documentation
        if options.examples:
            print _examples_documentation
        if options.doc or options.examples:
            sys.exit(0)
        self.nsubsets = int(options.njobs)
        self.verbose = options.verbose
        if len(args)>0:
            self.inputfile = args.pop(0)
        else:
            print ""
            print "Error: Input file required"
            print ""
            parser.print_help()
            sys.exit(1)
        if not os.path.exists(self.inputfile):
            print "Error: Input file '$s' not found." % self.inputfile
            sys.exit(1)
        else:
            (self.jobname,ext) = futils.splitext(self.inputfile)
            if (ext not in (".inp",".in")):
                self.jobname = self.inputfile
            self.jobname = os.path.basename(self.jobname)
            self.workdir = self.jobname+"_workdir"
            self.setJobName(self.jobname)
            self.setProgramName("XGlide")
            self.setDefaults()
            self.readInputFile()
            self.checkReceptorAssociations()
            #self.printFiles()
            self.complexes = self.expandDirectories(self.complexes)
            self.receptors = self.expandDirectories(self.receptors)
            self.ligands = self.expandDirectories(self.ligands)
            self.grids = self.expandDirectories(self.grids)
            self.checkFilenames()
            #self.printFiles()
            if not self.complexes and not self.receptors and not self.grids:
                print "Error: No receptors specified"
                sys.exit(1)
            if not self.complexes and not self.ligands:
                print "Error: No ligands specified"
                sys.exit(1)
            # Register the input files
            for cfile in self.complexes:
                self.addInputFile(cfile.getOriginalFilename())
            for rfile in self.receptors:
                self.addInputFile(rfile.getOriginalFilename())
            for lfile in self.ligands:
                self.addInputFile(lfile.getOriginalFilename())
            for gfile in self.grids:
                gridjobname,ext = futils.splitext(gfile.getOriginalFilename())
                if ext==".grd":
                    for gridext in (".cons","_coul2.fld",".csc",".grd",
                                    "_greedy.save",".gsc",".phob","_recep.mae",
                                    ".save",".site","_vdw.fld"):
                        if os.path.isfile(gridjobname+gridext):
                            self.addInputFile(gridjobname+gridext)
                else:
                    self.addInputFile(gfile.getOriginalFilename())
            if self.reference:
                # Register the reference file if not done registered already
                refname = self.reference.getOriginalFilename()
                if (os.path.isfile(refname) and
                    refname not in [x.getOriginalFilename() for x in
                    self.complexes+self.receptors]):
                    self.addInputFile(refname)
            if not options.remotedriver:
                # Override the -HOST setting for the driver so that it runs
                # on the launch machine.  This is the default, so that the
                # workdir and subjob files remain accessible on the launch
                # machine.  If running on the localhost, always use -LOCAL
                # to preserve the intermediate files.
                self.useLocalDriver()
                self.alwaysLocal()
        return args

    def printParameters(self):
        """ Print the job parameters. """
        # Input structure settings
        self.info("Input structures")
        if self.complexes:
            self.info("    Complexes:")
            for cfile in self.complexes:
                self.info("        %s" % cfile.getOriginalFilename())
        if self.receptors:
            self.info("    Receptors:")
            for rfile in self.receptors:
                self.info("        %s" % rfile.getOriginalFilename())
        if self.ligands:
            self.info("    Ligands:")
            for index,lfile in enumerate(self.ligands):
                if lfile.refpose:
                    self.info("        %s, REFPOSE" % lfile.getOriginalFilename())
                else:
                    self.info("        %s" % lfile.getOriginalFilename())
        if self.grids:
            self.info("    Grids:")
            for gfile in self.grids:
                self.info("        %s" % gfile.getOriginalFilename())
        self.info("Align structures:                       %s" % self.align)
        if self.align and self.reference:
            self.info("Reference structure:                    %s" %
                self.reference.getOriginalFilename())
        self.info("Max. ligand atoms:                      %s" % self.maxligatoms)
        self.info("Min. ligand atoms:                      %s" % self.minligatoms)
        self.info("Exclude ions:                           %s" % self.exclude_ions)
        self.info("Exclude amino acids:                    %s" % self.exclude_amino_acids)
        if self.excluded_residues:
            self.info("Excluded residues:                      %s" % self.excluded_residues)
        # Structure preparation settings
        self.info("Run protein preparation:                %s" % self.pprep)
        if self.pprep:
            self.info("    Cap termini:                        %s" % self.pprep_captermini)
            self.info("    Keep waters:                        %s" % self.pprep_keepwaters)
            self.info("    'Far' water distance:               %s" % self.pprep_waterdist)
            self.info("    Treat metals:                       %s" % self.pprep_treatmetals)
            self.info("    Fix bonds:                          %s" % self.pprep_fixbonds)
            if self.pprep_rehtreat:
                self.info("    Delete and re-add hydrogens:        %s" % self.pprep_rehtreat)
            else:
                self.info("    Apply hydrogen treatment:           %s" % self.pprep_htreat)
            self.info("    Run impref:                         %s " % self.pprep_impref)
            if self.pprep_impref:
                self.info("        Impref RMSD cutoff:             %s" % self.pprep_impref_rmsd)
            self.info("    Generate states with Epik:          %s" % self.pprep_epik)
            self.info("    Run protassign:                     %s" % self.pprep_protassign)
            if self.pprep_protassign:
                self.info("        Exhaustive protassign sampling: %s" % self.pprep_protassign_exhaustive)
                self.info("        Protassign water sampling:      %s" % self.pprep_protassign_water)
        self.info("Run LigPrep:                            %s" % self.ligprep)
        #self.info("Run MMod CSearch:                       %s" % self.csearch)
        self.info("Use SiteMap for grid centers:           %s" % self.sitemap)
        if (self.sitemap):
            self.info("    Maximum number of sites:            %s" % self.sitemap_maxsites)
            self.info("    Use sites for all grid centers:     %s" % self.sitemap_force)
        # Glide settings
        self.info("Glide Grid Generation")
        self.info("    Grid center specification:          %s" % str(self.gridcenter))
        self.info("    Grid size specification:            %s" % str(self.gridsize))
        self.info("    Grid size buffer:                   %s" % str(self.gridsize_buffer))
        for key,value in self.gridkeywords.iteritems():
            self.info("    %-36s%s" % (key,value))
        if self.skipdocking:
            self.info("Skipping Docking and RMSD stages")
        else:
            self.info("Glide Docking")
            for key,value in self.dockkeywords.iteritems():
                if key=="LIG_VSCALE" and self.lvdw_autoscale:
                    self.info("    Ligand autoscaling minimum:         %s" % self.lvdw_autoscale_min)
                    self.info("    Ligand autoscaling maximum:         %s" % self.lvdw_autoscale_max)
                    self.info("    Ligand autoscaling increment:       %s" % self.lvdw_autoscale_inc)
                elif key=="NUSECONS":
                    self.info("    Number of constraints to use:       %s" % self.nusecons)
                else:
                    self.info("    %-36s%s" % (key,value))
        # Miscellaneous settings
        self.info("Number of ligand subsets:               %s" % self.nsubsets)
        self.info("Native docking only:                    %s" % self.nativeonly)
        self.info("Cutoff for a 'good' RMSD:               %s" % self.goodrmsd)
        if self.generatecomplexes:
            self.info("Number of top complexes per receptor:   %s" % self.generatecomplexes)
        if self.mergesubsetposes:
            self.info("Merge subset docking results:           %s" % self.mergesubsetposes)
        self.info("Run with increased verbosity:           %s" % self.verbose)
        return

    def generateNewFilePath(self,file):
        """
        Given a relative file path, move the reference up a directory to
        reflect the use of the workdir.  If the file doesn't exist, assume it
        has been transferred to the JobDir.
        """
        newfile = file
        if not os.path.isfile(newfile):
            # File should be in the JobDir
            newfile = os.path.join(os.path.basename(newfile))
        if not os.path.isabs(newfile):
            # Adjust path relative to the workdir
            newfile = os.path.join("..",newfile)
        return newfile

    def updateFileReferences(self):
        """
        Subjobs are run in a subdirectory, so all file references must be
        updated.  Any relative paths must be modified to reflect the directory
        change.  In addition, inaccessible files may have been copied to the
        JobDir by Job Control, so use that path if the file is not at the
        specified path.  Is there a more efficient way to write this?
        """
        self.debug("")
        self.debug("")
        self.debug("Updating file references for CWD change to workdir")
        for c in self.complexes:
            c.update(self.generateNewFilePath(c.getCurrentFilename()),
                     reference=True)
            for lig in c.ligand:
                # Update the associated LIGANDs so the paths are correct for
                # nativeonly docking.
                lig.update(self.generateNewFilePath(lig.getCurrentFilename()))
        for r in self.receptors:
            r.update(self.generateNewFilePath(r.getCurrentFilename()),
                     reference=True)
            for lig in r.ligand:
                # Update the associated LIGANDs so the paths are correct for
                # nativeonly docking.
                lig.update(self.generateNewFilePath(lig.getCurrentFilename()))
        for l in self.ligands:
            l.update(self.generateNewFilePath(l.getCurrentFilename()),
                     reference=True)
        for g in self.grids:
            g.update(self.generateNewFilePath(g.getCurrentFilename()),
                     reference=True)
            for lig in g.ligand:
                # Update the associated LIGANDs so the paths are correct for
                # nativeonly docking.
                lig.update(self.generateNewFilePath(lig.getCurrentFilename()))
        if self.reference:
            self.reference.update(self.generateNewFilePath(
                                  self.reference.getCurrentFilename()))
        # Update file paths for Glide keyword input files, if used
        for key in self.dockkeywords:
            if key in ["GLIDE_CONS_FEAT_FILE","REF_LIGAND_FILE"]:
                self.dockkeywords[key] = self.generateNewFilePath(self.dockkeywords[key])
        return

    def setReceptorAssociations(self):
        """
        Set the LIGAND-RECEPTOR/GRID cross-references.  This must be done
        in the back end, because object references aren't preserved through
        the pickling process.
        """
        for lfile in self.ligands:
            #  The frontend stores the index of associated GRID/RECEPTOR
            if lfile.receptor!=None:
                self.receptors[lfile.receptor].ligand.append(lfile)
                lfile.receptor = self.receptors[lfile.receptor]
            elif lfile.grid!=None:
                self.grids[lfile.grid].ligand.append(lfile)
                lfile.grid = self.grids[lfile.grid]
        return

    def saveState(self):
        """
        Create/refresh the restart file.  All subjobs are run in the _workdir,
        so the restart file needs to be written one directory up.
        """
        self.dumpBE(relpath="..")

    def completedStage(self,stage):
        """
        Record the completed stage and save the restart file.  The 'stage'
        is one of the class stage constants (e.g., ALIGN).
        """
        self.stage_completed = stage
        self.saveState()

    def alignStructures(self):
        """
        Align Complexes and Receptors to a reference structure.  The reference
        structure is 1) the specified REFERENCE file, 2) the first COMPLEX
        structure, or 3) the first RECEPTOR, in that order.  The 'structalign'
        utility requires PDB files, so we must convert everything.  Grids are
        assumed to be in the proper alignment already.  Structures can't be
        aligned against an existing grid; instead, set the reference to the
        receptor structure used to generate the grid.
        """
        self.info("")
        self.info("")
        # RMSD calculations won't work correctly with LIGAND-associated
        # RECEPTORS if ALIGN is True, because the receptor will be moved
        # out of the frame of the ligand.
        for lfile in self.ligands:
            if lfile.refpose:
                self.warning("Warning: Aligning receptors when using pre-positioned ligands will")
                self.warning("         invalidate RMSD calculations because the receptor will move")
                self.warning("         out of the frame of reference of the ligand.")
                break
        if self.reference:
            reffile = self.reference
        elif self.complexes:
            self.info("No REFERENCE, using complex '%s'" % self.complexes[0].getCurrentFilename())
            reffile = self.complexes[0]
        elif self.receptors:
            self.info("No REFERENCE, using receptor '%s'" % self.receptors[0].getCurrentFilename())
            reffile = self.receptors[0]
        else:
            # I don't think this error can occur.
            self.error("Error: There is no structure that can act as the reference for alignment")
            sys.exit(1)
        # The 'structalign' program needs to act on local files, so copy or
        # the input files into the local directory.
        reffilename = reffile.getCurrentFilename()
        localrefpdbfile = "_".join((self.jobname,"",reffile.getBasename(),"",
                                    self.JOBEXTS['ALIGN_REF']+".pdb"))
        if get_structure_file_format(reffilename)!=futils.PDB:
            # Convert to PDB format.  PDB format wipes out properties,
            # so store them in the _FileTracker object temporarily.
            ref = structure.StructureReader(reffile.getCurrentFilename()).next()
            reffile.old_props = ref.property
            ref.write(localrefpdbfile)
        else:
            shutil.copyfile(reffilename,localrefpdbfile)
        pdbfiles = []
        for f in self.complexes+self.receptors:
            filename = f.getCurrentFilename()
            localpdbfile = "_".join((self.jobname,"",f.getBasename(),"",
                                     self.JOBEXTS['ALIGN_PRE']+".pdb"))
            if get_structure_file_format(filename)!=futils.PDB:
                # Convert to PDB format.  PDB format wipes out properties,
                # so store them in the _FileTracker object temporarily.
                st = structure.StructureReader(f.getCurrentFilename()).next()
                f.old_props = dict(st.property)
                st.write(localpdbfile)
            else:
                shutil.copyfile(filename,localpdbfile)
            f.update(localpdbfile)
            pdbfiles.append(localpdbfile)
        structalign = os.path.join(os.environ['SCHRODINGER'],'utilities',
                                   'structalign')
        cmd = [structalign,localrefpdbfile]
        cmd.extend(pdbfiles)
        logfilename = "_".join((self.jobname,self.JOBEXTS['ALIGN']+".log"))
        logfile = open(logfilename,'w')
        # Nested try's needed because python doesn't allow both "except" and
        # "finally" clauses of a single "try" block.
        try:
            try:
                process = subprocess.Popen(cmd,stdout=logfile,stderr=subprocess.STDOUT)
            except:
                self.error("Error: There was a problem running the alignment command...\n   %s" % " ".join(cmd))
                sys.exit(1)
        finally:
            logfile.close()
        process.wait()
        # Rename the output PDB files
        os.remove("rot-"+localrefpdbfile)
        for f in self.complexes+self.receptors:
            outpdbfile = "_".join((self.jobname,"",f.getBasename(),"",
                                   self.JOBEXTS['ALIGN']+".pdb"))
            os.rename("rot-"+f.getCurrentFilename(),outpdbfile)
            if os.path.isfile(outpdbfile):
                f.update(outpdbfile,reference=True)
            else:
                self.error("Error: Alignment output file '%s' not found!" % outpdbfile)
                sys.exit(1)
        self.info("Alignment complete")
        return

    def convertFormat(self):
        """
        Convert non-Maestro input to Maestro format in an explicit stage, so
        we can redirect conversion warnings.
        """
        ref = []
        if self.reference:
            ref = [self.reference]
        # We must make our own mmerr handle to redirect the conversion
        # warnings to a file.
        mm.mmerr_initialize()
        # We have to convert the ligands, because the Glide Dock class
        # assumes Maestro-formatted ligands.
        for f in self.complexes+self.receptors+ref+self.ligands:
           filename = f.getCurrentFilename()
           if get_structure_file_format(filename)!=futils.MAESTRO:
               basename = "_".join((self.jobname,"",f.getBasename(),"",
                                    self.JOBEXTS['CONVERT']))
               logfile = open(basename+".log",'w')
               mmerr_handle = mm.mmerr_new()
               mm.mmerr_file(mmerr_handle,logfile)
               outfile = basename+".maegz"
               for st in structure.StructureReader(filename,
                         error_handler=mmerr_handle):
                   if hasattr(f,"old_props"):
                       # Restore properties wiped out by PDB conversion in
                       # the alignment stage.  The Structure.property attribute
                       # is not a true dictionary, so we must cast it first.
                       # This is relevant only for non-PDB receptor/complexes
                       # that have been aligned.
                       st.property.update(f.old_props)
                       del f.old_props
                   st.append(outfile)
                   logfile.flush()
               mm.mmerr_delete(mmerr_handle)
               logfile.close()
               f.update(outfile,reference=True)

    def runPPrep(self):
        """
        Run command-line Protein Preparation Wizard jobs on COMPLEXes and
        RECEPTORs.
        """
        if not (self.complexes or self.receptors):
            return
        self.info("")
        self.info("")
        self.info("---------------------")
        self.info(" Protein Preparation ")
        self.info("---------------------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        if not self.jdj:
            # Not resuming a JobDJ run.  Create a new instance.
            self.jdj = jobdj.JobDJ(verbosity="normal",
                                   max_failures=jobdj.NOLIMIT)
            options = []
            if not self.pprep_fixbonds:
                options.append("-nobondorders")
            if self.pprep_rehtreat:
                options.append("-rehtreat")
            elif not self.pprep_htreat:
                options.append("-nohtreat")
            if self.pprep_captermini:
                options.append("-c")
            if self.pprep_keepwaters:
                options.append("-keepfarwat")
            else:
                options.extend(["-watdist",str(self.pprep_waterdist)])
            if not self.pprep_treatmetals:
                options.append("-nometaltreat")
            if not self.pprep_epik:
                options.append("-noepik")
            if self.pprep_protassign:
                if self.pprep_protassign_exhaustive:
                    options.append("-x")
                if self.pprep_protassign_water:
                    options.append("-s")
            else:
                options.append("-noprotassign")
            if self.pprep_impref:
                options.extend(["-rmsd",str(self.pprep_impref_rmsd)])
                if self.pprep_impref_fixheavy:
                    options.append("-fix")
            else:
                options.append("-noimpref")
            for f in self.complexes+self.receptors:
                ppwjobname = "_".join((self.jobname,"",f.getBasename(),
                                       "",self.JOBEXTS['PPREP']))
                outfile = ppwjobname+".maegz"
                cmd = ["prepwizard"]
                cmd.extend(options)
                cmd.append(f.getCurrentFilename())
                cmd.append(outfile)
                self.jdj.addJob(cmd)
                f.update(outfile,reference=True)
        try:
            self.jdj.run(self.saveState)  # Enable JobDJ restartability
        except RuntimeError:
            sys.exit(1)
        self.jdj = None   # Clear for the next stage
        self.debug("")
        if self.complexes:
            self.debug("New complex files...")
            for cfile in self.complexes:
                self.debug("    %s" % cfile.getCurrentFilename())
        if self.receptors:
            self.debug("New receptor files...")
            for rfile in self.receptors:
                self.debug("    %s" % rfile.getCurrentFilename())
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("runPPrep runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************
        return

    def splitComplexes(self):
        """
        Identify the ligand in each COMPLEX and split the complex into ligand
        and receptor files.  The resulting receptor and ligand keep the
        identifier (basename) of the complex.
        """
        def get_res_string(st):
            """Return list of residue labels"""
            reslist = []
            resstring = ""
            for res in st.residue:
                reslabel = "%s:%s%d%s" % (res.chain,res.pdbres.strip(),
                                          res.resnum,res.inscode.strip())
                if reslabel not in reslist:
                    reslist.append(reslabel)
                    if resstring:
                        resstring += ","
                    resstring += reslabel
            return resstring

        if not self.complexes:
            return
        self.info("")
        self.info("")
        self.info("Splitting complexes...")
        first = True
        for cfile in self.complexes:
            basename = cfile.getBasename()
            # Merge all CT's in the file into one complex.
            c = None
            if not os.path.isfile(cfile.getCurrentFilename()):
                self.warning("Warning: Missing file '%s'." % cfile.getCurrentFilename())
                continue
            for st in structure.StructureReader(cfile.getCurrentFilename()):
                if not c:
                    c = st
                else:
                    c.extend(st)
            if c.mol_total<2:
                self.warning("Warning: File '%s' is not a complex.  Ignoring." % cfile.getCurrentFilename())
            else:
                ligandasl = None
                searchasl = None
                if cfile.ligasl!=None:
                    if cfile.ligasl=="mol.num 0":
                        # Special case, change to last molecule in structure
                        searchasl = "mol.num %s" % c.mol_total
                    else:
                        searchasl = cfile.ligasl
                # Use the AslLigandSearcher to identify the ligand, using the
                # user-supplied ASL if specified for the COMPLEX.  We have to
                # check covalent ligands in order to get the original atom
                # molecule numbers stored.  PYTHON-2666.  We don't actually
                # want covalent ligands (for now), because structural repair
                # is needed to extract them; they'll be filtered out.  We
                # won't break ZOBs before evaluating the ligand ASL, because
                # we want to maintain the same molecules (as determined by ZOB
                # traversal settings) as the original structure.  Removing
                # ZOBs causes the heme iron to be treated as a separate
                # ligand, along with Ca/Zn ions and waters molecules attached
                # to them with the same molecule number.
                asl_searcher = MyAslLigandSearcher(
                    remove_zobs=False,
                    check_covalent=True
                )
                asl_searcher.min_atom_count = self.minligatoms
                asl_searcher.max_atom_count = self.maxligatoms
                asl_searcher.exclude_ions = self.exclude_ions
                asl_searcher.exclude_amino_acids = self.exclude_amino_acids
                if self.excluded_residues:
                    asl_searcher.excluded_residues = self.excluded_residues
                # Pass in the COMPLEX-specific ligand ASL (None if not
                # specified), which will override the ASL expression
                # constructed within the AslLigandSearcher.
                ligands = asl_searcher.search(st,searchasl)
                # The returned Ligands are not in molecule order, so sort them.
                ligands.sort(cmp=lambda x,y:cmp(x.mol_num,y.mol_num))
                if not ligands:
                    self.warning("    Warning: File '%s' contains no ligands.  Ignoring." % cfile.getCurrentFilename())
                else:
                    # Note: The 'ligand_asl' attribute is generated only
                    # for the matching atoms, not for the entire ligand
                    # molecule. PYTHON-2436. By not removing ZOBs, we
                    # don't have to worry about molecule fragments (e.g.,
                    # metal ions) being detected as separate ligand
                    # molecules.  We'll just use the molecule number
                    # reported for the ligand by AslLigandSearcher, which
                    # seems to be valid for non-covalent ligands.
                    #
                    # Note: Terminal HXT atoms on peptides are not matched by
                    # the standard 'backbone' and 'sidechain' ASL expressions
                    # used for amino acid detection.  As a result, these atoms
                    # (and therefore the whole peptide molecules) will be
                    # treated as ligands. PYTHON-2437.  As a workaround, use
                    # a subclass of AslLigandSearcher that includes HXT in
                    # the 'backbone' definition.
                    #
                    # Note: If amino acids are excluded, the 'backbone' ASL
                    # expression (which includes "atom.pt ca,c,n,o,oxt" may
                    # exclude some atoms in non-amino-acid residues.  This
                    # isn't a problem once the ASL expression is reconstructed
                    # from all atoms in the ligand molecule.
                    #
                    # Note: Similar to the previous note, if a multiresidue
                    # ligand is above the size cutoff, it's possible that only
                    # parts of it will be detected as covalent ligands due to
                    # certain residues incorrectly being removed because of
                    # protein-like atom names during the covalent ligand check.
                    # This problem might go away if we we're able to turn off
                    # the covalent check after PYTHON-2666 is fixed.
                    #
                    # Note: If an 'override' ASL expression is specified for
                    # a complex, the covalent check can misidentify some
                    # covalent ligands, due to molecule and atom numbers
                    # changing in the covalent-check working structure.
                    # These are identified as covalent ligands, so they'll
                    # just be ignored.  PYTHON-2667.
                    #
                    self.debug("    Found %s ligand(s) for '%s'" % (len(ligands),cfile.getBasename()))
                    found_noncovalent_ligand = False
                    for index,ligand in enumerate(ligands,1):
                        # Atoms in split covalent ligands won't have the
                        # 'orig_index_prop' property defined
                        #atomlist = []
                        #for at in ligand.st.atom:
                        #    if asl_searcher.orig_index_prop in at.property:
                        #        atomlist.append(at.property[asl_searcher.orig_index_prop])
                        #asl = analyze.generate_asl(c,atomlist)
                        #self.debug("        MATCH_ASL = %s (%s atoms)" % (ligand.ligand_asl,len(analyze.evaluate_asl(c,ligand.ligand_asl))))
                        #if ligand.mol_num<0:
                        #    self.debug("        COVALENT")
                        #else:
                        #    self.debug("        MOL_ASL = %s (%s atoms)" % (asl,len(analyze.evaluate_asl(c,asl))))
                        #self.debug("        RES_IDS = %s" % get_res_string(ligand.st))
                        #if ligand.mol_num<0:
                        #    self.debug("        mol num = %s" % ligand.mol_num)
                        #else:
                        #    self.debug("        mol num = %s (%s atoms)" % (ligand.mol_num,len(analyze.evaluate_asl(c,"mol.num %s" % ligand.mol_num))))
                        # Find first non-covalent ligand
                        if ligand.mol_num<0:
                            self.debug("        %s: %s (covalent)" % (index,get_res_string(ligand.st)))
                        else:
                            self.debug("        %s: %s (mol num %s, %s atoms)" % (index,get_res_string(ligand.st),ligand.mol_num,len(c.molecule[ligand.mol_num].atom)))
                            if not found_noncovalent_ligand:
                                # Use the ligand molecule number found by AslLigandSearcher
                                ligandasl = "mol.num %s" % ligand.mol_num
                                found_noncovalent_ligand = True
                    if not ligandasl:
                        self.warning("    Warning: File '%s' contains no non-covalent ligands. Ignoring." % cfile.getCurrentFilename())
                if ligandasl:
                    #lig = c.molecule[ligandmol].extractStructure()
                    ligatomlist = analyze.evaluate_asl(c,ligandasl)
                    lig = c.extract(ligatomlist)
                    lig.title = basename+" ligand"
                    c.deleteAtoms(ligatomlist)
                    recfile = "_".join((self.jobname,"",basename,"",
                                        self.JOBEXTS['SPLIT_REC']+".maegz"))
                    c.write(recfile)
                    self.receptors.append(_Receptor(recfile))
                    self.receptors[-1].changeBasename(basename)
                    self.receptors[-1].complex = cfile
                    cfile.receptor = self.receptors[-1]
                    ligfile = "_".join((self.jobname,"",basename,"",
                                        self.JOBEXTS['SPLIT_LIG']+".maegz"))
                    lig.write(ligfile)
                    self.ligands.append(_Ligand(ligfile))
                    self.ligands[-1].changeBasename(basename)
                    self.ligands[-1].refpose = True
                    self.ligands[-1].complex = cfile
                    self.ligands[-1].receptor = cfile.receptor
                    cfile.ligand.append(self.ligands[-1])
                    if first:
                        first = False
                    self.info("    Extracted ligand '%s (%s, %s atoms)' from '%s'"
                               % (get_res_string(lig),ligandasl,lig.atom_total,cfile.getBasename()))
        if first:
            self.info("No complexes split")
        return

    def createLigandSubsets(self):
        """
        Create ligand subset files.  The docking subjobs are distributed, so
        the ligands (from LIGANDs and COMPLEXes) must be divided into roughly-
        equal subset files.  The number of subsets is an input parameter and
        determines the number of ligands per subset file.

        To calculate an RMSD later for ligands from COMPLEXes or marked as
        REFPOSE, add properties to the subset structures for the subset and
        whether the RMSD should be calculated.
        """
        self.debug("")
        self.debug("")
        # Counting structures
        self.ntotligands = 0
        self.nligands = {}
        self.ntotrefligands = 0
        self.nrefligands = {}
        self.nligperfile = 0
        for lfile in self.ligands:
            if lfile.getCurrentFilename().endswith(".mol2"):
                # count_structures() currently doesn't work with mol2 files.
                # Count them manually.  This could be slow if the file is big.
                nlig = 0
                for st in structure.StructureReader(lfile.getCurrentFilename()):
                    nlig += 1
            else:
                nlig = structure.count_structures(lfile.getCurrentFilename())
                if not nlig and get_structure_file_format(lfile)==futils.PDB:
                    # count_structures() doesn't work for PDB files unless
                    # the structures are listed as MODELs.  If a zero count is
                    # returned, assume there is a single structure.
                    nlig = 1
            self.nligands[lfile] = nlig
            self.ntotligands += nlig
            if lfile.refpose:
                self.nrefligands[lfile] = nlig
                self.ntotrefligands += nlig
            if (lfile.receptor or lfile.grid) and nlig>self.nligperfile:
                # Set the initial value of this variable to the maximum number
                # of ligands in a file associated with a RECEPTOR or GRID, for
                # use with nativeonly.
                self.nligperfile = nlig
        if not self.ntotligands:
            self.error("Error: There are no ligands in the LIGAND file(s)")
            sys.exit(1)
        if self.nativeonly:
            self.debug("No ligand subsets created for native-only docking.")
            return
        self.debug("Creating ligand subsets...")
        if self.nsubsets<1:
            self.nsubsets = 1
        self.debug("")
        self.debug("There are %d ligands in %d files" % (self.ntotligands,
                     len(self.ligands)))
        self.debug("There are %d ligands in the reference frame." % self.ntotrefligands)
        if self.ntotligands < self.nsubsets:
            self.nsubsets = self.ntotligands
        self.nligperfile,mod = divmod(self.ntotligands,self.nsubsets)
        if mod>0:
            self.nligperfile += 1
        index = 0
        self.debug("")
        self.debug("Ligands will be split into %d file(s), with %d ligands per file." % (self.nsubsets,self.nligperfile))
        w = len(str(self.nsubsets))
        nliginfile = 0
        nfile = 0
        self.ligandsubsets = []
        for lfile in self.ligands:
            # Since we are splitting up the ligands into subset files, we
            # need to record whether a ligand is in the reference frame.
            # Ligands that are derived from complexes are in the reference
            # frame, and LIGANDs specified as REFPOSE are, also.  Is the
            # storage going to be prohibitive for large ligand files?
            if nliginfile:
                # Start indexing another file in the current subset
                self.ligandsubsets[-1].subsetorigin.append([lfile,[0,-1]])
            for stindex,st in enumerate(structure.StructureReader(lfile.getCurrentFilename())):
                # Add a property that records the position in the file, so
                # any variants (e.g., generated by LigPrep) can be traced back
                # to the original structure.
                st.property['i_xglide_ligandID'] = nliginfile
                if nliginfile==0:
                    # Start a new ligand file
                    nfile += 1
                    subsetname = "ligsubset-%0*d" % (w,nfile)
                    ligsubsetfile = "%s_%s.maegz" % (self.jobname,subsetname)
                    # For each subset, store the range of ligands taken from
                    # each pre-subset ligand files.
                    st.write(ligsubsetfile)
                    self.ligandsubsets.append(_Ligand(ligsubsetfile))
                    self.ligandsubsets[-1].changeBasename(subsetname)
                    self.ligandsubsets[-1].subsetorigin = [[lfile,[stindex,-1]]]
                else:
                    st.append(ligsubsetfile)
                self.ligandsubsets[-1].subsetorigin[-1][1][1] = stindex
                nliginfile += 1
                if nliginfile>=self.nligperfile:
                    nliginfile = 0
            index += 1
        return

    def runLigPrep(self):
        """
        Run LigPrep on all LIGANDs to prepare and expand ligand states.
        """
        if not self.ligands:
            return
        self.info("")
        self.info("")
        self.info("--------------------")
        self.info(" Ligand Preparation ")
        self.info("--------------------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        if self.nativeonly:
            ligands = self.ligands
        else:
            ligands = self.ligandsubsets
        if not self.jdj:
            # Not resuming a JobDJ run.  Create a new instance.
            self.jdj = jobdj.JobDJ(verbosity="normal",
                                   max_failures=jobdj.NOLIMIT)
            options = []
            # "-s 32 -r 1 -bff 14 are LigPrep defaults
            if self.ligprep_epik:
                options.append("-epik")
                options.extend(["-W","e,-ph,7.0,-pht,2.0"])
            else:
                options.extend(["-i","2"])
                options.extend(["-W","i,-ph,7.0,-pht,2.0"])
            for lfile in ligands:
                if (self.nativeonly and
                    not (lfile.complex or lfile.receptor or lfile.grid)):
                    # In NATIVEONLY mode, a ligand file not associated with
                    # a receptor or grid won't be used, so there's no need to
                    # run LigPrep on it.
                    self.info("Skipping '%s' for NATIVEONLY job." % lfile.getBasename())
                    continue
                lpjobname = "_".join((self.jobname,"",lfile.getBasename(),
                                      "",self.JOBEXTS['LIGPREP']))
                outfile = lpjobname+".maegz"
                cmd = ["ligprep"]
                cmd.extend(options)
                cmd.extend(["-imae",lfile.getCurrentFilename(),"-omae",outfile])
                
                self.jdj.addJob(cmd)
                # The coordinates change through LigPrep, so the structures
                # can't be used as the reference.
                lfile.update(outfile,reference=False)
        try:
            self.jdj.run(self.saveState)  # Enable JobDJ restartability
        except RuntimeError:
            sys.exit(1)
        self.jdj = None   # Clear for the next stage
        self.debug("")
        for lfile in ligands:
            nst = structure.count_structures(lfile.getCurrentFilename())
            if nst>self.nligperfile:
                self.nligperfile = nst
        self.info("After LigPrep, the maximum number of ligands per file is %d" % self.nligperfile)
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("runLigPrep runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************
        return

    def generateSites(self):
        """
        For non-NATIVEONLY jobs, run SiteMap on each RECEPTOR without an
        associated ligand in order to determine the location of the active
        site for later Grid Generation.  If SITEMAP_FORCE, run on all RECEPTORS.
        """
        self.info("")
        self.info("")
        self.info("---------")
        self.info(" SiteMap ")
        self.info("---------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        if self.nativeonly and not self.sitemap_force:
            self.info("SiteMap stage not run for NATIVEONLY jobs unless SITEMAP_FORCE is TRUE.")
            self.info("")
            return
        if not self.jdj:
            # Not resuming a JobDJ run.  Create a new instance.
            self.sitemapjobs = []
            self.jdj = jobdj.JobDJ(verbosity="normal",
                                   max_failures=jobdj.NOLIMIT)
            for rfile in self.receptors:
                if (rfile.ligand or rfile.complex) and not self.sitemap_force:
                    # Don't generate sites for receptors that have an associated
                    # ligand.
                    continue
                sitemapjobname = "_".join((self.jobname,"",rfile.getBasename(),"",
                                           self.JOBEXTS['SITEMAP']))
                self.sitemapjobs.append(sitemapjobname)
                rec = structure.StructureReader(rfile.getCurrentFilename()).next()
                # SiteMap jobs don't support gzipped structure files yet
                rec.write(sitemapjobname+".mae")
                self.jdj.addJob(["sitemap","-maxsites",str(self.sitemap_maxsites),"-j",sitemapjobname,"-prot",sitemapjobname+".mae"])
                # Store the name of the site file in the _Receptor object
                rfile.sites = sitemapjobname+"_out.maegz"
        if not self.sitemapjobs:
            self.warning("Warning: No SiteMap jobs run")
            self.jdj = None
            return
        try:
            self.jdj.run(self.saveState)  # Enable JobDJ restartability
        except RuntimeError:
            sys.exit(1)
        self.jdj = None   # Clear for the next stage
        #  The surface files generated by SiteMap can be large and aren't
        #  needed by XGlide.  Zip them up to save space.
        self.info("Archiving the SiteMap surface files...")
        for sitejob in self.sitemapjobs:
            visarchive = tarfile.open(sitejob+"_vis.tar.gz",'w:gz')
            for visfile in glob.glob(sitejob+"*.vis"):
                visarchive.add(visfile)
                os.remove(visfile)
            visarchive.close()
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("generateSites runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************
        return

    def getCentroid(self,st):
        """
        Return the (x,y,z) coordinates of the centroid of the structure 'st'.
        """
        natoms = len(st.atom)
        if natoms==0:
            raise Exception("Error: No atoms in structure. Can't calculate centroid.")
        xsum = 0.0
        ysum = 0.0
        zsum = 0.0
        for at in st.atom:
            xsum += at.x
            ysum += at.y
            zsum += at.z
        return (xsum/natoms,ysum/natoms,zsum/natoms)

    # *************************************************************************
    # These options(INCLUSION,GREEDY,LATTICE,RANDOM) made by Ban et al.
    # *************************************************************************

    # This is a function of GRIDGEN_INCLUSION_SETTING made by Ban et al.
    def gridInclusionSetting(self,st):
        """
        Return the gridcenters. This is xglide_mga.py original option.
        """
        GridCenter=[]
        GridCenter.append(self.getCentroid(st))
        return GridCenter

    # This is a function of GRIDGEN_GREEDY_SETTING made by Ban et al.
    def gridGreedySetting(self,st):
        """
        Return the gridcenters. This is xglide_mga.py original option.
        """
        atoms = st.atom
        dots=[]
        for at in atoms:
            dots.append((at.x,at.y,at.z))
        GridCenter=[]
        Include_dots=[]
        while dots:
            max_count_dot=0
            for gc in dots:
                count_dot=0
                for dot in dots:
                    if ((gc[0]-0.5*int(self.gridkeywords["INNERBOX"])<dot[0] and dot[0]<gc[0]+0.5*int(self.gridkeywords["INNERBOX"])) and
                        (gc[1]-0.5*int(self.gridkeywords["INNERBOX"])<dot[1] and dot[1]<gc[1]+0.5*int(self.gridkeywords["INNERBOX"])) and
                        (gc[2]-0.5*int(self.gridkeywords["INNERBOX"])<dot[2] and dot[2]<gc[2]+0.5*int(self.gridkeywords["INNERBOX"]))):
                        Include_dots.append(dot)
                        count_dot += 1
                if count_dot>max_count_dot:
                    max_count_dot = count_dot
                    candidate_gc = gc
                    candidate_id = Include_dots
                Include_dots=[]
            GridCenter.append(candidate_gc)
            for dot in candidate_id:
                dots.remove(dot)

        return GridCenter

    # This is a function of GRIDGEN_LATTICE_SETTING made by Ban et al.
    def gridLatticeSetting(self,st):
        """
        Return the gridcenters. This is xglide_mga.py original option.
        """
        atoms = st.atom
        dots=[]
        for at in atoms:
            dots.append((at.x,at.y,at.z))
    
        GridCenter=[]
        m = self.getLigandMiddle(st)
        R = self.getLigandMaxWide(st)
        r = int(self.gridkeywords["INNERBOX"])
        if (R%r > 0):
            N = int(R/r) + 1
        else:
            N = int(R/r)
        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    gc = (m[0]+r*(1+2*i-N)/2,m[1]+r*(1+2*j-N)/2,m[2]+r*(1+2*k-N)/2)
                    for dot in dots:
                        if ((gc[0]-0.5*int(self.gridkeywords["INNERBOX"])<dot[0] and dot[0]<gc[0]+0.5*int(self.gridkeywords["INNERBOX"])) and
                            (gc[1]-0.5*int(self.gridkeywords["INNERBOX"])<dot[1] and dot[1]<gc[1]+0.5*int(self.gridkeywords["INNERBOX"])) and
                            (gc[2]-0.5*int(self.gridkeywords["INNERBOX"])<dot[2] and dot[2]<gc[2]+0.5*int(self.gridkeywords["INNERBOX"]))):
                            GridCenter.append(gc)
                            break

        return GridCenter

    def getLigandMiddle(self,st):
        """
        Return a float that is the middle point in the structure 'st'.
        """
        atoms = st.atom
        dots=[]
        maxwide=[0,0,0]
        middle=[0,0,0]
        for at in atoms:
            dots.append((at.x,at.y,at.z))
        for i in range(0,len(dots)-1):
            for j in range(i+1,len(dots)):
                dot1 = dots[i]
                dot2 = dots[j]
                for k in range(0,3):
                    if abs(dot1[k]-dot2[k])>maxwide[k]:
                        maxwide[k] = abs(dot1[k]-dot2[k])
                        middle[k] = float(dot1[k]+dot2[k])/2

        return (middle[0],middle[1],middle[2])

    def getLigandMaxWide(self,st):
        """
        Return a float that is the middle point in the structure 'st'.
        """
        atoms = st.atom
        dots=[]
        maxwide=0.0
        for at in atoms:
            dots.append((at.x,at.y,at.z))
        for i in range(0,len(dots)-1):
            for j in range(i+1,len(dots)):
                dot1 = dots[i]
                dot2 = dots[j]
                for k in range(0,3):
                    if abs(dot1[k]-dot2[k])>maxwide:
                        maxwide = abs(dot1[k]-dot2[k]);

        return int(maxwide)+1


    # This is a function of GRIDGEN_RANDOM_SETTING made by Ban et al.
    def gridRandomSetting(self,st):
        """
        Return the gridcenters. This is xglide_mga.py original option.
        """
        atoms = st.atom
        dots=[]
        for at in atoms:
            dots.append((at.x,at.y,at.z))
        GridCenter=[]
        random.seed(0)
        random.shuffle(dots)
        while dots:
            gc = dots.pop(0)
            GridCenter.append(gc)
            rmd = []
            for dot in dots:
                if ((gc[0]-0.5*int(self.gridkeywords["INNERBOX"])<dot[0] and dot[0]<gc[0]+0.5*int(self.gridkeywords["INNERBOX"])) and
                    (gc[1]-0.5*int(self.gridkeywords["INNERBOX"])<dot[1] and dot[1]<gc[1]+0.5*int(self.gridkeywords["INNERBOX"])) and
                    (gc[2]-0.5*int(self.gridkeywords["INNERBOX"])<dot[2] and dot[2]<gc[2]+0.5*int(self.gridkeywords["INNERBOX"]))):
                    rmd.append(dot)
            for dot in rmd:
                dots.remove(dot)

        return GridCenter

    # *************************************************************************

    def determineGridCenter(self):
        """
        Determine the (x,y,z) coordinates of the grid box center from the
        center of mass of the ligands derived from COMPLEXes (or associated
        with RECEPTORs).  Creates 'self.gridcenters', a dictionary whose keys
        are the receptor basenames, and whose values are lists of the grid centers
        for those receptors.
        """
        self.gridcenters = {}
        if (self.gridcenter not in ["AUTO","SELF"]):
            # Use the explicit coordinates for all grids
            for rfile in self.receptors:
                self.gridcenters[rfile.getBasename()] = [self.gridcenter]
        elif self.gridcenter=="AUTO":
            # Determine the grid center from the centroid of ligands from
            # aligned complexes and associated receptors.
            found = False
            for lfile in self.ligands:
                if lfile.refpose:
                    # Includes ligands from complexes, those associated with
                    # grids/receptors, and those flagged as REFPOSE.
                    found = True
            if not found:
                self.error("Error: The grid box center cannot be generated automatically without a LIGAND positioned in the active site (in a COMPLEX, associated with a GRID/RECEPTOR, or flagged as REFPOSE.")
                sys.exit(1)
            self.info("")
            self.info("")
            self.info("Determining the grid center from the centroid of ligands in reference frame...")
            xsum = 0.0
            ysum = 0.0
            zsum = 0.0
            natom = 0
            for lfile in self.ligands:
                if not lfile.refpose:
                    continue
                st = structure.StructureReader(lfile.getCurrentFilename()).next()
                for at in st.atom:
                    xsum += at.x
                    ysum += at.y
                    zsum += at.z
                natom += len(st.atom)
            self.info("Grid center X,Y,Z = (%12.6f,%12.6f,%12.6f)" % (
                      xsum/natom,ysum/natom,zsum/natom))
            for rfile in self.receptors:
                self.gridcenters[rfile.getBasename()] = [(xsum/natom,
                                                        ysum/natom,
                                                        zsum/natom)]
        else:
            # Determine the center of each grid from REFPOSE ligands
            # associated with the individual receptors.
            self.info("")
            self.info("")
            self.info("Determining the center(s) for each grid from the")
            self.info("associated ligand or SiteMap site(s).")
            for rfile in self.receptors:
                if (rfile.complex or rfile.ligand) and not (rfile.sites and self.sitemap_force):
                    # Set the grid center at the centroid of all associated REFPOSE ligands.
                    nat_and_centroid = []
                    ligfiles = rfile.ligand
                    if rfile.complex:
                        ligfiles.extend(rfile.complex.ligand)
                    for lig in ligfiles:
                        if not lig.refpose:
                            continue
                        st = structure.StructureReader(lig.getCurrentFilename()).next()
                        nat_and_centroid.append((st.atom_total,self.getCentroid(st)))
                    if not nat_and_centroid:
                        self.warning("No REFPOSE ligands associated with the receptor '%s'. Skipping" % rfile.getBasename())
                        continue
                    ntot = 0
                    xyztot = [0.0,0.0,0.0]
                    for nat,xyz in nat_and_centroid:
                        ntot += nat
                        xyztot[0] += xyz[0]*nat
                        xyztot[1] += xyz[1]*nat
                        xyztot[2] += xyz[2]*nat
                    xyztot[0] /= ntot
                    xyztot[1] /= ntot
                    xyztot[2] /= ntot
                    self.gridcenters[rfile.getBasename()] = [xyztot]
                elif rfile.sites:
                    # Either the RECEPTOR has no associated ligand, or we've
                    # calculated sites and SITEMAP_FORCE is True.  Store the grid
                    # centers determine by the top SiteMap sites, to a maximum of
                    # SITEMAP_MAXSITES.
                    if not os.path.isfile(rfile.sites):
                        # Not SiteMap output files
                        self.warning("No SiteMap output file '%s'.  Skipping" % rfile.sites)
                        continue
                    nst = structure.count_structures(rfile.sites)
                    try:
                        sr = structure.StructureReader(rfile.sites)
                    except:
                        self.warning("Could not read SiteMap sites for receptor '%s'.  Skipping." % (rfile.getBasename()))
                        continue
                    self.gridcenters[rfile.getBasename()] = []
                    index = 0
                    for st in sr:
                        index += 1
                        # Skip the last structure, which is the receptor.
                        if index>(nst-1):
                            break
                        if index>self.sitemap_maxsites:
                            break
                        
                        # *************************************************************************
                        # These options(INCLUSION,GREEDY,LATTICE,RANDOM) made by Ban et al.
                        # *************************************************************************

                        self.info("")
                        self.info("Sitepoints of SiteMap Site%s: %s " % (index,len(st.atom)) )

                        # GRIDGEN_INCLUSION_SETTING option by Ban et al.
                        if self.gridgenInclusionSetting==True:
                            self.info("GridGen mode is GRIDGEN_INCLUSION_SETTING")
                            self.info("")
                            gcl = self.gridInclusionSetting(st)
                            for gc in gcl:
                                self.gridcenters[rfile.getBasename()].append(gc)

                        # GRIDGEN_GREEDY_SETTING option by Ban et al.
                        elif self.gridgenGreedySetting==True:
                            self.info("GridGen mode is GRIDGEN_GREEDY_SETTING")
                            gcl = self.gridGreedySetting(st)
                            self.info("The Number of generated grids: %s" % len(gcl))
                            for gc in gcl:
                                self.gridcenters[rfile.getBasename()].append(gc)

                        # GRIDGEN_LATTICE_SETTING option by Ban et al.
                        elif self.gridgenLatticeSetting==True:
                            self.info("GridGen mode is GRIDGEN_LATTICE_SETTING")
                            gcl = self.gridLatticeSetting(st)
                            self.info("The Number of generated grids: %s" % len(gcl))
                            for gc in gcl:
                                self.gridcenters[rfile.getBasename()].append(gc)

                        # GRIDGEN_RANDOM_SETTING option by Ban et al.
                        elif self.gridgenRandomSetting==True:
                            self.info("GridGen mode is GRIDGEN_RANDOM_SETTING")
                            gcl = self.gridRandomSetting(st)
                            self.info("The Number of generated grids: %s" % len(gcl))
                            for gc in gcl:
                                self.gridcenters[rfile.getBasename()].append(gc)

                        # GRIDGEN_STANDARD_SETTING option by Schrodinger.inc.
                        else:
                            self.info("GridGen mode is GRIDGEN_STANDARD_SETTING")
                            self.info("")
                            self.gridcenters[rfile.getBasename()].append(self.getCentroid(st))
                                
                        # *************************************************************************
                else:
                    continue
            for rfile in self.receptors:
                bn = rfile.getBasename()
                if bn in self.gridcenters:
                    if len(self.gridcenters[bn])==1:
                        gc = self.gridcenters[bn][0]
                        self.info("Grid center X,Y,Z = (%12.6f,%12.6f,%12.6f) for '%s'" % (
                        gc[0],gc[1],gc[2],bn))
                    else:
                        self.info("Grid centers X,Y,Z for '%s'..." % bn)
                        for gc in self.gridcenters[bn]:
                            self.info("    (%12.6f,%12.6f,%12.6f)" % (gc[0],gc[1],gc[2]))
                else:
                    self.warning("Warning: Grid center can't be defined for '%s'." % bn)
        return

    def getLigandDiameter(self,st):
        """
        Return a float that is the longest distance between two atoms in the
        structure 'st'.
        """
        maxdist = 0.0
        for iat in range(1,len(st.atom)+1):
            for jat in range(iat+1,len(st.atom)+1):
                d = st.measure(iat,jat)
                if d>maxdist:
                    maxdist = d
        return maxdist
                

    def determineGridSize(self):
        """
        Determine the dimensions of the outer grid box from the sizes
        ligands derived from COMPLEXes (or associated with RECEPTORs).  Creates
        'self.gridsizes', a dictionary whose keys are the receptor basenames,
        and whose values are the sizes for those receptor grids.  The AUTO and
        SELF methods create cubic grid boxes that are the inner box size plus
        the size (diameter length) of the largest reference ligand (all, or just
        those associated with a particular receptor).
        """
        # NOTE: Should we still restrict to REFPOSE ligands?  That isn't
        # strictly necessary for a size calculation.  There might be too
        # many associated ligands, though.
        
        self.gridsizes = {}
        
        # *************************************************************************
        # These options(INCLUSION,GREEDY,LATTICE,RANDOM) made by Ban et al.
        # *************************************************************************
        
        self.innerboxsizes = {}
        
        # GRIDGEN_INCLUSION_SETTING option by Ban et al.
        if self.gridgenInclusionSetting==True:
            # If you expect to dock larger ligands, or if there is no Workspace ligand,
            # select Dock ligands with length <= and use the slider to choose an appropriate
            # maximum ligand length. The slider is set 20 A by default.
            for rfile in self.receptors:
                if rfile.sites:
                    if not os.path.isfile(rfile.sites):
                        # Not SiteMap output files
                        self.warning("No SiteMap output file '%s'.  Skipping" % rfile.sites)
                        continue
                    nst = structure.count_structures(rfile.sites)
                    try:
                        sr = structure.StructureReader(rfile.sites)
                    except:
                        self.warning("Could not read SiteMap sites for receptor '%s'.  Skipping." % (rfile.getBasename()))
                        continue
                    index = 0
                    for st in sr:
                        index += 1
                        # Skip the last structure, which is the receptor.
                        if index>(nst-1):
                            break
                        if index>self.sitemap_maxsites:
                            break
                        ibs = int(self.getLigandDiameter(st))
                        gs = ibs + 20
                        if ibs > 30:
                            ibs = 30
                        if gs > 50:
                            gs = 50
                        self.info("")
                        self.info("INNER_BOX_SIZE : %s" % ibs)
                        self.info("OUTER_BOX_SIZE : %s" % gs)
                        self.innerboxsizes[rfile.getBasename()] = [ibs]
                        self.gridsizes[rfile.getBasename()] = [gs]
    
        # GRIDGEN_GREEDY_SETTING option by Ban et al.
        elif self.gridgenGreedySetting==True:
            # If you expect to dock larger ligands, or if there is no Workspace ligand,
            # select Dock ligands with length <= and use the slider to choose an appropriate
            # maximum ligand length. The slider is set to 20 A by default.
            self.gridsize = self.innerboxsize + 20
            self.info("")
            self.info("INNER_BOX_SIZE : %s" % self.innerboxsize)
            self.info("OUTER_BOX_SIZE : %s" % self.gridsize)
            for rfile in self.receptors:
                bn = rfile.getBasename()
                if bn in self.gridcenters:
                    for gc in self.gridcenters[bn]:
                        self.innerboxsizes[bn] = [self.innerboxsize]
                        self.gridsizes[bn] = [self.gridsize]

        # GRIDGEN_LATTICE_SETTING option by Ban et al.
        elif self.gridgenLatticeSetting==True:
            # If you expect to dock larger ligands, or if there is no Workspace ligand,
            # select Dock ligands with length <= and use the slider to choose an appropriate
            # maximum ligand length. The slider is set to 20 A by default.
            self.gridsize = self.innerboxsize + 20
            self.info("")
            self.info("INNER_BOX_SIZE : %s" % self.innerboxsize)
            self.info("OUTER_BOX_SIZE : %s" % self.gridsize)
            for rfile in self.receptors:
                bn = rfile.getBasename()
                if bn in self.gridcenters:
                    for gc in self.gridcenters[bn]:
                        self.innerboxsizes[bn] = [self.innerboxsize]
                        self.gridsizes[bn] = [self.gridsize]

        # GRIDGEN_RANDOM_SETTING option by Ban et al.
        elif self.gridgenRandomSetting==True:
            # If you expect to dock larger ligands, or if there is no Workspace ligand,
            # select Dock ligands with length <= and use the slider to choose an appropriate
            # maximum ligand length. The slider is set to 20 A by default.
            self.gridsize = self.innerboxsize + 20
            self.info("")
            self.info("INNER_BOX_SIZE : %s" % self.innerboxsize)
            self.info("OUTER_BOX_SIZE : %s" % self.gridsize)
            for rfile in self.receptors:
                bn = rfile.getBasename()
                if bn in self.gridcenters:
                    for gc in self.gridcenters[bn]:
                        self.innerboxsizes[bn] = [self.innerboxsize]
                        self.gridsizes[bn] = [self.gridsize]

        # GRIDGEN_STANDARD_SETTING option by Ban et al
        elif (self.gridsize not in ["AUTO","SELF"]):
            # Use the explicit dimensions for all grids.  This can be x,y,z
            # dimensions.
            self.info("")
            self.info("INNER_BOX_SIZE : %s" % self.innerboxsize)
            self.info("OUTER_BOX_SIZE : %s" % self.gridsize)
            for rfile in self.receptors:
                self.innerboxsizes[rfile.getBasename()] = [self.innerboxsize]
                self.gridsizes[rfile.getBasename()] = [self.gridsize]

        # *************************************************************************

        elif self.gridsize=="AUTO":
            # Determine the grid size from the sizes of ligands from
            # aligned complexes and associated receptors.
            found = False
            for lfile in self.ligands:
                if lfile.refpose:
                    # Includes ligands from complexes, those associated with
                    # grids/receptors, and those flagged as REFPOSE.
                    found = True
            if not found:
                self.error("Error: The grid box size cannot be generated automatically without a LIGAND positioned in the active site (in a COMPLEX, associated with a GRID/RECEPTOR, or flagged as REFPOSE.")
                sys.exit(1)
            self.info("")
            self.info("")
            self.info("Determining the grid size from the sizes of ligands in reference frame...")
            maxsize = 0.0
            for lfile in self.ligands:
                if not lfile.refpose:
                    continue
                st = structure.StructureReader(lfile.getCurrentFilename()).next()
                sz = self.getLigandDiameter(st)
                if sz>maxsize:
                    maxsize = sz
            # The INNERBOX is either an integer, a string number, or a list of
            # string numbers.  Need to convert to list of integers.
            try:
                ibs = [int(self.gridkeywords["INNERBOX"])]
            except:
                try:
                    ibs = [int(x) for x in self.gridkeywords["INNERBOX"]]
                except:
                    self.error("Error: Inner box specification '%s' incorrect.  Must be comma-separated list of integers." % self.gridkeywords["INNERBOX"])
                    sys.exit(1)
            buf = self.gridsize_buffer
            if len(ibs)==3:
                gs = [ibs[0]+maxsize+buf,ibs[1]+maxsize+buf,ibs[2]+maxsize+buf]
            elif len(ibs)==1:
                gs = [ibs[0]+maxsize+buf,ibs[0]+maxsize+buf,ibs[0]+maxsize+buf]
            else:
                self.error("Error: Inner box specification must be a single size or X,Y,Z dimensions")
                sys.exit(1)
            self.info("Grid size = (%3.1f, %3.1f, %3.1f)" % (gs[0],gs[1],gs[2]))
            for rfile in self.receptors:
                self.gridsizes[rfile.getBasename()] = [gs]
        else:
            # Determine the size of each grid from REFPOSE ligands
            # associated with the individual receptors.
            self.info("")
            self.info("")
            self.info("Determining the size(s) for each grid from the")
            self.info("associated ligands or SiteMap site(s).")
            # The INNERBOX is either an integer, a string number, or a list of
            # string numbers.  Need to convert to list of integers.
            try:
                ibs = [int(self.gridkeywords["INNERBOX"])]
            except:
                try:
                    ibs = [int(x) for x in self.gridkeywords["INNERBOX"]]
                except:
                    self.error("Error: Inner box specification '%s' incorrect.  Must be comma-separated list of integers." % self.gridkeywords["INNERBOX"])
                    sys.exit(1)
            buf = self.gridsize_buffer
            for rfile in self.receptors:
                if (rfile.complex or rfile.ligand) and not (rfile.sites and self.sitemap_force):
                    # Set the grid size according to the sizes of all associated REFPOSE ligands.
                    ligfiles = rfile.ligand
                    if rfile.complex:
                        ligfiles.extend(rfile.complex.ligand)
                    maxsize = None
                    for lig in ligfiles:
                        if not lig.refpose:
                            continue
                        st = structure.StructureReader(lig.getCurrentFilename()).next()
                        sz = self.getLigandDiameter(st)
                        if maxsize==None or sz>maxsize:
                            maxsize = sz
                    if maxsize==None:
                        self.warning("No REFPOSE ligands associated with the receptor '%s'. Skipping" % rfile.getBasename())
                        continue
                    if len(ibs)==3:
                        gs = [ibs[0]+maxsize+buf,ibs[1]+maxsize+buf,ibs[2]+maxsize+buf]
                    elif len(ibs)==1:
                        gs = [ibs[0]+maxsize+buf,ibs[0]+maxsize+buf,ibs[0]+maxsize+buf]
                    else:
                        self.error("Error: Inner box specification must be a single size or X,Y,Z dimensions")
                        sys.exit(1)
                    self.gridsizes[rfile.getBasename()] = [gs]
                elif rfile.sites:
                    # Either the RECEPTOR has no associated ligand, or we've
                    # calculated sites and SITEMAP_FORCE is True.  Store the grid
                    # sizes determined by the top SiteMap sites, to a maximum of
                    # SITEMAP_MAXSITES.
                    if not os.path.isfile(rfile.sites):
                        # Not SiteMap output files
                        self.warning("No SiteMap output file '%s'.  Skipping" % rfile.sites)
                        continue
                    nst = structure.count_structures(rfile.sites)
                    try:
                        sr = structure.StructureReader(rfile.sites)
                    except:
                        self.warning("Could not read SiteMap sites for receptor '%s'.  Skipping." % (rfile.getBasename()))
                        continue
                    self.gridsizes[rfile.getBasename()] = []
                    index = 0
                    for st in sr:
                        index += 1
                        # Skip the last structure, which is the receptor.
                        if index>(nst-1):
                            break
                        if index>self.sitemap_maxsites:
                            break
                        sz = self.getLigandDiameter(st)
                        try:
                            
                            # *************************************************************************
                            # This code is modified to run correct by Ban et al.
                            # *************************************************************************
                            
                            if len(ibs)==3:
                                gs = [float(ibs[0])+sz+buf,float(ibs[1])+sz+buf,float(ibs[2])+sz+buf]
                            elif len(ibs)==1:
                                gs = [float(ibs[0])+sz+buf,float(ibs[0])+sz+buf,float(ibs[0])+sz+buf]
                            else:
                                self.error("Error: Inner box specification must be a single size or X,Y,Z dimensions")
                                sys.exit(1)

                            # *************************************************************************

                        except TypeError:
                            gs = [float(ibs)+sz+buf,float(ibs)+sz+buf,float(ibs)+sz+buf]
                        self.gridsizes[rfile.getBasename()].append(gs)
                else:
                    continue
            for rfile in self.receptors:
                bn = rfile.getBasename()
                if bn in self.gridsizes:
                    if len(self.gridsizes[bn])==1:
                        gs = self.gridsizes[bn][0]
                        self.info("Grid size = (%3.1f, %3.1f, %3.1f) for '%s'" % (gs[0],gs[1],gs[2],bn))
                    else:
                        self.info("Grid sizes for '%s'..." % bn)
                        for gs in self.gridsizes[bn]:
                            self.info("    (%3.1f, %3.1f, %3.1f)" % (gs[0],gs[1],gs[2]))
                else:
                    self.warning("Warning: Grid size can't be defined for '%s'." % bn)
        return

    def generateGrids(self):
        """
        Generate grid files for COMPLEXes and RECEPTORs.
        """
        self.info("")
        self.info("")
        self.info("-----------------------")
        self.info(" Glide Grid Generation ")
        self.info("-----------------------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        #self.printFiles()
        if not self.jdj:
            # Not resuming a JobDJ run.  Create a new instance.
            self.gridjobs = []
            self.jdj = jobdj.JobDJ(verbosity="normal",
                                   max_failures=jobdj.NOLIMIT)
            # *************************************************************************
            # runtime measurement is made by Ban et al.
            # *************************************************************************
            
            start_gridCenter_time = time.time()
            self.determineGridCenter()
            end_gridCenter_time = time.time()
            self.info("determineGridCenter runtime[sec]: %f"%(end_gridCenter_time - start_gridCenter_time))
            
            start_gridSize_time = time.time()
            self.determineGridSize()
            end_gridSize_time = time.time()
            self.info("determineGridSize runtime[sec]: %f"%(end_gridSize_time - start_gridSize_time))
            
            # *************************************************************************
            for rfile in self.receptors:
                if rfile.getBasename() not in self.gridcenters:
                    #self.warning("Warning: Grid center can't be defined for '%s'." % rfile.getBasename())
                    # Stick a placeholder in the gridjobs list so they line up with the receptors
                    self.gridjobs.append(None)
                    continue
                if rfile.getBasename() not in self.gridsizes:
                    #self.warning("Warning: Grid size can't be defined for '%s'." % rfile.getBasename())
                    # Stick a placeholder in the gridjobs list so they line up with the receptors
                    self.gridjobs.append(None)
                    continue
                if self.nativeonly:
                    if (not rfile.complex and
                        not rfile.ligand):
                        # Native redocking currently is possible only for
                        # COMPLEXes and LIGAND-associated RECEPTORs and GRIDs.
                        self.warning("Warning: No grid will be generated for RECEPTOR '%s' because it has no associated ligand for redocking." % rfile.getBasename())
                        # Stick a placeholder in the gridjobs list so they line up with the receptors
                        self.gridjobs.append(None)
                        continue
                multgrids = False
                if len(self.gridcenters[rfile.getBasename()])>1:
                    multgrids = True
                index = 0
                recgridjobs = []
                for gc in self.gridcenters[rfile.getBasename()]:
                    index += 1
                    if multgrids:
                        gridjobname = "_".join((self.jobname,"",
                                                "%s_site%s" % (rfile.getBasename(),index),
                                                "",self.JOBEXTS['GRID']))
                    else:
                        gridjobname = "_".join((self.jobname,"",rfile.getBasename(),
                                                "",self.JOBEXTS['GRID']))
                    recgridjobs.append(gridjobname)
                    rec = structure.StructureReader(rfile.getCurrentFilename()).next()
                    # Should we update the _Receptor with the grid job input file?
                    # The structure doesn't change.
                    rec.write(gridjobname+".maegz")
                    # We could consider setting the box sizes from the sizes of the
                    # ligands, or the overall active-site coverage of the ligands.
                    
                    # *************************************************************************
                    # This code is inserted by Ban et al.
                    # *************************************************************************
                    
                    if len(self.innerboxsizes[rfile.getBasename()])==1:
                        self.gridkeywords["INNERBOX"] = self.innerboxsizes[rfile.getBasename()][0]
                    else:
                        self.gridkeywords["INNERBOX"] = self.innerboxsizes[rfile.getBasename()][index-1]
                    
                    # *************************************************************************
                    
                    if len(self.gridsizes[rfile.getBasename()])==1:
                        gs = self.gridsizes[rfile.getBasename()][0]
                    else:
                        gs = self.gridsizes[rfile.getBasename()][index-1]
                    ggkeys = {'JOBNAME':gridjobname,
                              'RECEP_FILE':gridjobname+".maegz",
                              'WRITEZIP':True,
                              'GRID_CENTER':gc,
                              'OUTERBOX':gs}
                    ggkeys.update(self.gridkeywords)
                    gridgen = glide.Gridgen(ggkeys)
                    grid_inp = gridgen.writeSimplified()
                    self.jdj.addJob(["glide",grid_inp])
                self.gridjobs.append(recgridjobs)
        try:
            self.jdj.run(self.saveState)  # Enable JobDJ restartability
        except RuntimeError:
            sys.exit(1)
        self.jdj = None   # Clear for the next stage
        # The _Grids check for file existence, so create them after the jobs
        # have run.  Keep the receptor identifier for each _Grid.
        for recfile,gridjobnames in zip(self.receptors,self.gridjobs):
            if not gridjobnames:
                # Skip the receptors for which no grids were generated
                continue
            index = 0
            multgrids = False
            if len(gridjobnames)>1:
                multgrids = True
            for gridjob in gridjobnames:
                index += 1
                try:
                    self.grids.append(_Grid(gridjob+".zip"))
                except:
                    self.error("No grids generated for '%s'" % recfile.getBasename())
                else:
                    self.grids[-1].receptor = recfile
                    if multgrids:
                        self.grids[-1].changeBasename("%s_site%s" % (recfile.getBasename(),index))
                    else:
                        self.grids[-1].changeBasename(recfile.getBasename())
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("generateGrids runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************
        return

    def glideMerge(self):
        """
        Merge the docking results for each receptor.  Remove the subset pose
        files when complete.  Adapted from the Glide driver.
        """
        self.info("")
        self.info("Merging the Glide output files...")
        if "NREPORT" in self.dockkeywords:
            self.info("Max number of poses saved per receptor/scaling: %i" % self.dockkeywords["NREPORT"])
        posefiles = {}
        nreportcmd = []
        if "NREPORT" in self.dockkeywords:
            nreportcmd = ["-n", self.dockkeywords["NREPORT"]]
        for dockjob,gridfile,lscale,ligfile in self.dockjobs:
           # Group the pose files by grid and scaling factor
           posefiles.setdefault((gridfile,lscale),[])
           posefiles[(gridfile,lscale)].append(dockjob+self.glide_output_extension)
        for gridfile,lscale in posefiles:
            self.info("")
            self.info("    Merging files...")
            for f in posefiles[(gridfile,lscale)]:
                self.info("        %s" % f)
            # Create a text file that will be passed to glide_merge:
            mergefiles_file = self.jobname + '_subjob_output_files.txt'
            fh = open(mergefiles_file, 'w')
            for ligfile in posefiles[(gridfile,lscale)]:
                fh.write(ligfile + "\n")
            fh.close()
            # Construct the merged file name.  Ignore the ligfile component.
            mergejobname = "_".join((self.jobname,"",
                           gridfile.getBasename(),"",
                           self.JOBEXTS['DOCK']))
            if self.lvdw_autoscale:
                mergejobname += "_%2.1f" % lscale
            merged_file = "%s%s" % (mergejobname,self.glide_output_extension)
            self.info("    The merged output pose file is '%s'" % merged_file)
            # Construct the glide-merge command
            exe = os.path.join(os.environ["SCHRODINGER"], "utilities", "glide_merge")
            cmd = [exe, "-f", mergefiles_file, "-o", merged_file, "-b", "500", "-nofilter"]
            if nreportcmd:
                cmd.extend(nreportcmd)
            if "WRITEREPT" in self.dockkeywords:
                write_reptfile = ( writerept.lower() in [ 'yes', 'true', '1'] )
                if write_reptfile:
                    dockmode = self.dockkeywords['DOCKING_METHOD']
                    if (dockmode.lower() == 'inplace'):
                        report_file = "%s.scor" % mergejobname
                    else:
                        report_file = "%s.rept" % mergejobname
                    cmd += [ "-r", report_file ]
            self.debug("    Running merge command: %s" % cmd)
            mergelog = open(mergejobname+".log",'w')
            try:
                process = subprocess.Popen(cmd,stdout=mergelog,stderr=subprocess.STDOUT)
                process.wait()
            except:
                self.error("    Error: There was a problem running the glide_merge command...\n   %s" % " ".join(cmd))
                continue
            finally:
                mergelog.close()
            if process.returncode != 0:
                sys.exit("    Error: glide_merge failed.")
            else:
                # In case the above "exit()" method doesn't actually exit,
                # we may want to keep the "_subjob_output_files.txt" file
                # around if glide_merge failed.
                os.remove(mergefiles_file)
            if not os.path.isfile(merged_file):
                sys.exit("    Error: Failed to merge docked poses! '%s' not found." % merged_file)
            # Archive and remove subjob pose files.
            zipname = mergejobname + '_subjob_poses.zip'
            zipfh = zipfile.ZipFile(zipname, 'w')
            for ligfile in posefiles[(gridfile,lscale)]:
                if os.path.isfile(ligfile):
                    zipfh.write(ligfile)
                else:
                    self.warning("    Warning: Subset pose file '%s' is missing." % ligfile)
            zipfh.close()
            if not os.path.isfile(zipname):
                self.warning("    Warning: Failed to write archive '%s' of subjob pose files." % zipname)
            else:
                self.info("    Individual subjob pose files are archived in '%s'." % zipname)
                zipfh = zipfile.ZipFile(zipname, 'r')
                try:
                    lignames = zipfh.namelist()
                    if (lignames):
                        for ligfile in posefiles[(gridfile,lscale)]:
                            if ligfile in lignames:
                                os.remove(ligfile)
                finally:
                    zipfh.close()

    def dockLigands(self):
        """
        Dock ligands from COMPLEXes and LIGAND files into the receptor grids.
        """
        self.info("")
        self.info("")
        self.info("----------------------")
        self.info(" Glide Ligand Docking ")
        self.info("----------------------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        #self.printFiles()
        if not self.jdj:
            # Not resuming a JobDJ run.  Create a new instance.
            self.dockjobs = []
            self.jdj = jobdj.JobDJ(verbosity="normal",
                                   max_failures=jobdj.NOLIMIT)
            # Set up the ligand scalings
            if self.lvdw_autoscale:
               self.info("")
               self.info("LVDW set to AUTO.  Ligands will be docked")
               self.info("repeatedly with different vdW scalings.")
               self.info("")
               self.lig_scalings = []
               lscale = self.lvdw_autoscale_max
               while lscale>=self.lvdw_autoscale_min:
                   self.lig_scalings.append(lscale)
                   lscale -= self.lvdw_autoscale_inc
            else:
               self.lig_scalings = [float(self.dockkeywords['LIG_VSCALE'])]
            # Note:  This allows the user to override the calculated NREPORT,
            #        which might not be a good thing.
            dkeys = {'NREPORT':self.nligperfile*
                               int(self.dockkeywords['POSES_PER_LIG']),
                     'DIELECTRIC':2.0}
            dkeys.update(self.dockkeywords)
            for igrid,gridfile in enumerate(self.grids):
                gridbase,ext = futils.splitext(gridfile.getCurrentFilename())
                constraints = glide.read_constraints(gridfile.getCurrentFilename())
                conslabels = []
                ncons = 0
                if constraints and (gridfile.usecons or self.nusecons):
                    # Determine the constraints that will be included in the
                    # docking job, and the number that will be required.
                    self.info("Constraints found for grid '%s'." % gridfile.getBasename())
                    for c in constraints:
                        if c.type() in (glide.HBOND_DONOR,
                                        glide.HBOND_ACCEPTOR,
                                        glide.METAL,
                                        glide.HYDROPHOBIC):
                            conslabels.append(str(c))
                            self.info("    Using '%s' (%s)" % (c,c.type()))
                        else:
                            # Hydrophobic and positional constraints not
                            # supported.
                            self.info("    Ignoring '%s' (%s)" % (c,c.type()))
                    ncons = self.nusecons
                    if gridfile.usecons:
                        # Override the overall setting with the grid-specific
                        # setting.
                        ncons = gridfile.usecons
                    if ncons>len(conslabels):
                        ncons = len(conslabels)
                    nconsstr = ncons
                    if ncons==-1:
                        nconsstr = "All"
                    self.info("    %s of these constraints will be required" % (nconsstr))
                if self.nativeonly:
                    if not gridfile.receptor and not gridfile.ligand:
                        # Pre-generated GRIDs don't have a native ligand for
                        # redocking unless there is an associated LIGAND.
                        self.warning("Warning: Pre-generated grid '%s' will not be used in redocking mode." % gridbase)
                        continue
                dkeys['GRIDFILE'] = gridfile.getCurrentFilename()
                if (ext==".zip"):
                    compressed = True
                else:
                    compressed = False
                dkeys['READZIP'] = compressed
                for lscale in self.lig_scalings:
                    dkeys['LIG_VSCALE'] = lscale
                    if self.nativeonly:
                        assoc_ligfiles = []
                        if gridfile.ligand:
                            # LIGAND associated with GRID
                            assoc_ligfiles = gridfile.ligand
                        elif gridfile.receptor.ligand:
                            # LIGAND associated with RECEPTOR
                            assoc_ligfiles = gridfile.receptor.ligand
                        else:
                            # LIGAND from COMPLEX
                            assoc_ligfiles = gridfile.receptor.complex.ligand
                        for ligfile in assoc_ligfiles:
                            dockjobname = "_".join((self.jobname,"",
                                                    gridfile.getBasename(),"",
                                                    ligfile.getBasename(),"",
                                                    self.JOBEXTS['DOCK']))
                            if self.lvdw_autoscale:
                                # Name the jobs by the ligand scaling
                                dockjobname += "_%2.1f" % lscale
                            self.dockjobs.append((dockjobname,gridfile,lscale,
                                                  ligfile))
                            dkeys['JOBNAME'] = dockjobname
                            dkeys['LIGANDFILE'] = ligfile.getCurrentFilename()
                            dock = glide.Dock(dkeys)
                            for c in conslabels:
                                dock.useConstraint(c)
                            if conslabels:
                                dock.setNRequired(ncons)
                            dock_inp = dock.writeSimplified()
                            self.jdj.addJob(["glide",dock_inp])
                            # Register the output pose file with Job Control so it
                            # always will be copied back to the launch directory.
                            self.addOutputFileBE(os.path.join(self.workdir,dockjobname+self.glide_output_extension))
                    else:
                        for ligfile in self.ligandsubsets:
                            dockjobname = "_".join((self.jobname,"",
                                                    gridfile.getBasename(),"",
                                                    ligfile.getBasename(),"",
                                                    self.JOBEXTS['DOCK']))
                            if self.lvdw_autoscale:
                                # Name the jobs by the ligand scaling
                                dockjobname += "_%2.1f" % lscale
                            self.dockjobs.append((dockjobname,gridfile,lscale,
                                                  ligfile))
                            dkeys['JOBNAME'] = dockjobname
                            dkeys['LIGANDFILE'] = ligfile.getCurrentFilename()
                            dock = glide.Dock(dkeys)
                            for c in conslabels:
                                dock.useConstraint(c)
                            if conslabels:
                                dock.setNRequired(ncons)
                            dock_inp = dock.writeSimplified()
                            self.jdj.addJob(["glide",dock_inp])
                            # Register the output pose file with Job Control so
                            # it always will be copied back to the launch
                            # directory.
                            self.addOutputFileBE(os.path.join(self.workdir,dockjobname+self.glide_output_extension))
        try:
            self.jdj.run(self.saveState)  # Enable JobDJ restartability
        except RuntimeError:
            sys.exit(1)
        self.jdj = None   # Clear for the next stage
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("dockLigands runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************
        return

    def calculateRMSDs(self):
        """
        Calculate RMSDs.  This can be done only for ligands that have a
        a input pose in the reference frame of the receptors.  This is true
        for COMPLEXes, for LIGANDs that are identified as being REFPOSEs, or
        LIGANDs that are associated with RECEPTORs or GRIDs.

        Currently, the RMSD is calculated against the input to the docking job
        (i.e., the structure in the subset file).
        """
        self.info("")
        self.info("")
        self.info("--------------")
        self.info(" RMSD Results ")
        self.info("--------------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        # *************************************************************************
        # This dictionary is made by Ban et al.
        # *************************************************************************
        result_dic = {}
        # *************************************************************************
        #self.printFiles()
        self.info("")
        if self.lvdw_autoscale:
            self.info("%-24s %-7s %-30s %6s %8s" % ("Receptor","Scaling",
                "Ligand [file (index,title)]","RMSD","GScore"))
        else:
            self.info("%-24s %-35s %6s %8s" % ("Receptor",
                                               "Ligand [file (index,title)]",
                                               "RMSD","GScore"))
        self.info("-"*80)
        self.nligands_docked = {}
        self.nrefligands_docked = {}
        self.nrefligands_correct = {}
        self.refligands_averms = {}
        self.nposes = {}
        self.nrefposes = {}
        self.ntotligands_per_grid = {}
        self.ntotrefligands_per_grid = {}
        for gfile in self.grids:
            self.nligands_docked[gfile] = {}
            self.nrefligands_docked[gfile] = {}
            self.nrefligands_correct[gfile] = {}
            self.refligands_averms[gfile] = {}
            self.nposes[gfile] = {}
            self.nrefposes[gfile] = {}
            self.ntotligands_per_grid[gfile] = {}
            self.ntotrefligands_per_grid[gfile] = {}
        for dockjob,gridfile,lscale,ligfile in self.dockjobs:
            self.nligands_docked[gridfile].setdefault(lscale,0)
            self.nrefligands_docked[gridfile].setdefault(lscale,0)
            self.nrefligands_correct[gridfile].setdefault(lscale,0)
            self.refligands_averms[gridfile].setdefault(lscale,0.0)
            self.nposes[gridfile].setdefault(lscale,0)
            self.nrefposes[gridfile].setdefault(lscale,0)
            if self.nativeonly:
                # For nativeonly jobs, the original _Ligand objects are used.
                # For regular jobs, the ligands are split into subsets (new
                # _Ligand objects), so they can't be used as keys.  These two
                # stats are relevant only for nativeonly jobs anyway.
                self.ntotligands_per_grid[gridfile][lscale] = self.ntotligands_per_grid[gridfile].get(lscale,0)+self.nligands[ligfile]
                if ligfile in self.nrefligands:
                   self.ntotrefligands_per_grid[gridfile][lscale] = self.ntotrefligands_per_grid[gridfile].get(lscale,0)+self.nrefligands[ligfile]
            # Keep track of ligands for which poses already have been found.
            # This is to prevent overcounting docked ligands when maxperlig is
            # greater than one.  This could present a storage problem for
            # large ligand files.  We are counting a ligand as docking
            # correctly if any of its poses are correct.
            lig_dock = {}
            lig_ref_dock = {}
            lig_correct_dock = {}
            fname = dockjob+self.glide_output_extension
            if not os.path.isfile(fname):
                continue
            index = 0
            for st in structure.StructureReader(fname):
                # If the pose is a ligand from a COMPLEX, calculate the RMSD
                # with the ligand in that COMPLEX.  If the pose is a LIGAND
                # with a REFPOSE setting, calculate the RMSD with that
                # LIGAND.
                #
                # Skip the receptor, if this is the first st of a PV file.
                if index==0 and futils.is_poseviewer_file(fname):
                    index += 1
                    continue
                # Use the special ligandID to identify the original structure
                # index, because state expansion makes the 'lignum' unreliable
                # (many-to-one correspondence).
                if self.nativeonly:
                    # For nativeonly jobs, the ligands aren't split into
                    # subsets, so there is no opportunity to tag them with
                    # IDs.  Our only option is to use the lignum, but this
                    # will fail if a LigPrep stage is run.
                    ninfile = st.property['i_i_glide_lignum']
                else:
                    ninfile = st.property['i_xglide_ligandID']
                # Given the index in the subset file, find the reference
                # ligand structure (file and index).
                ligreffile = None
                ligreffileindex = 0
                if self.nativeonly:
                    # Subsets not used
                    ligreffile = ligfile
                    ligreffileindex = ninfile
                else:
                    cum = 0
                    for lfile,(start,end) in ligfile.subsetorigin:
                        if ninfile>=cum and ninfile<=cum+(end-start):
                            ligreffile = lfile
                            # The StructureReader indexing starts at 1, not 0
                            ligreffileindex = ninfile-(cum-start)+1
                            break
                        cum += (end-start)+1
                if ninfile not in lig_dock:
                    lig_dock[ninfile] = True
                    self.nligands_docked[gridfile][lscale] += 1
                self.nposes[gridfile][lscale] += 1
                if ligreffile.refpose:
                    self.nrefposes[gridfile][lscale] += 1
                    reflig = structure.StructureReader(ligreffile.getReferenceFilename(),ligreffileindex).next()
                    conf_rmsd = structureutil.ConformerRmsd(reflig,st)
                    # Set the following option so ConformerRmsd will work with
                    # varying tautomers and ionization states.
                    conf_rmsd.use_heavy_atom_graph = True
                    try:
                        rmsd = conf_rmsd.calculate()
                    except:
                        self.warning("Could not calculate the rmsd for ligand '%s (%s, %s)' docked to '%s'" % (ligreffile.getBasename(),ligreffileindex,st.title,gridfile.getBasename()))
                        continue
                    
                    # *************************************************************************
                    # This dictionary is made by Ban et al.
                    # *************************************************************************
                    result_dic[st.property[self.GSCOREPROP]] = rmsd
                    # *************************************************************************
                    
                    if ninfile not in lig_ref_dock:
                        lig_ref_dock[ninfile] = True
                        self.nrefligands_docked[gridfile][lscale] += 1
                    self.refligands_averms[gridfile][lscale] += rmsd
                    if rmsd<=self.goodrmsd and ninfile not in lig_correct_dock:
                        lig_correct_dock[ninfile] = True
                        self.nrefligands_correct[gridfile][lscale] += 1
                    marker = " "
                    if (ligreffile.receptor and gridfile.receptor and
                        ligreffile.receptor.getBasename()==
                            gridfile.receptor.getBasename()):
                        marker = "*"
                    if (ligreffile.grid and
                        ligreffile.grid.getBasename()==gridfile.getBasename()):
                        marker = "*"
                    if self.lvdw_autoscale:
                        self.info("%-24s %7.1f %-30s %6.2f %8.2f%s" % (
                            gridfile.getBasename(),lscale,"%s (%d, '%s')" % (
                            ligreffile.getBasename(),ligreffileindex,
                            st.title),rmsd,st.property[self.GSCOREPROP],marker))
                    else:
                        self.info("%-24s %-35s %6.2f %8.2f%s" % (
                            gridfile.getBasename(),"%s (%d, '%s')" % (
                            ligreffile.getBasename(),ligreffileindex,st.title),
                            rmsd,st.property[self.GSCOREPROP],marker))
                else:
                    if self.lvdw_autoscale:
                        self.info("%-24s %7.1f %-30s    --- %8.2f" % (
                            gridfile.getBasename(),lscale,"%s (%d, '%s')" % (
                            ligreffile.getBasename(),ligreffileindex,
                            st.title),st.property[self.GSCOREPROP]))
                    else:
                        self.info("%-24s %-35s    --- %8.2f" % (
                            gridfile.getBasename(),"%s (%d, '%s')" % (
                            ligreffile.getBasename(),ligreffileindex,st.title),
                            st.property[self.GSCOREPROP]))
                index += 1
        
        # Print the summary statistics and choose the optimal ligand vdW
        # scalings.  The optimal scaling is defined as that which yields the
        # most poses within 2 A.  The scaling is adjusted on a per-receptor
        # basis; that is, all ligands docking to a particular receptor will use
        # the same scaling, but the optimized scaling may be different for
        # different receptors.
        self.info("")
        self.info("Summary results...")
        self.info("")
        
        # *************************************************************************
        # This dictionary is made by Ban et al.
        # *************************************************************************
        if len(result_dic.keys()) > 0:
            self.info("bestGscore: %.2f" % min(result_dic.keys()))
            self.info("RMSD of bestGscore: %.2f" % (result_dic[min(result_dic.keys())]))
        # *************************************************************************
        
        self.info("")
        self.info("%-25s %4s %11s %11s %11s %11s" % ("Receptor","Scal",
            "%Docked","%RefDocked","AveRMS","%RefCorrect"))
        self.info("-"*79)
        opt_scaling = {}
        opt_rms = {}
        opt_val = {}
        for gfile in self.grids:
            opt_scaling[gfile] = []
            opt_rms[gfile] = []
            opt_val[file] = None
            for lscale in self.lig_scalings:
                if lscale not in self.nposes[gfile]:
                    # The grid wasn't used for docking, 
                    continue
                # The average is over all poses
                if self.nrefposes[gfile][lscale]:
                    self.refligands_averms[gfile][lscale] = self.refligands_averms[gfile][lscale]/self.nrefposes[gfile][lscale]
                ncorrect = self.nrefligands_correct[gfile][lscale]
                if not opt_scaling[gfile] or ncorrect>opt_val[gfile]:
                    opt_scaling[gfile] = ["%.1f" % lscale]
                    opt_rms[gfile] = [self.refligands_averms[gfile][lscale]]
                    opt_val[gfile] = ncorrect
                elif ncorrect==opt_val[gfile]:
                    opt_scaling[gfile].append("%.1f" % lscale)
                    opt_rms[gfile].append(self.refligands_averms[gfile][lscale])
                if self.nativeonly:
                    nlig = self.ntotligands_per_grid[gfile][lscale]
                    nreflig = self.ntotrefligands_per_grid[gfile][lscale]
                else:
                    nlig = self.ntotligands
                    nreflig = self.ntotrefligands
                if nreflig==0:
                    self.info("%-25s %4.1f %11.2f         ---         ---         ---" % (
                        gfile.getBasename(),
                        lscale,
                        100.0*self.nligands_docked[gfile][lscale]/nlig))
                else:
                    self.info("%-25s %4.1f %11.2f %11.2f %11.2f %11.2f" % (
                        gfile.getBasename(),
                        lscale,
                        100.0*self.nligands_docked[gfile][lscale]/nlig,
                        100.0*self.nrefligands_docked[gfile][lscale]/nreflig,
                        self.refligands_averms[gfile][lscale],
                        100.0*self.nrefligands_correct[gfile][lscale]/nreflig))
        self.info("")
        if self.lvdw_autoscale:
            self.info("Optimal scalings, judging by the percent of ligands")
            self.info("redocked to %s A or less, with average overall RMS..." %
                      self.goodrmsd)
            self.info("")
            for gfile in self.grids:
                # This calculation might not be correct for nativeonly jobs.
                opt_val[gfile] = 100.0*opt_val[gfile]/self.ntotrefligands
                z = zip(opt_rms[gfile],opt_scaling[gfile])
                z.sort()
                self.info("%-25s (%6.2f%%)" % (gfile.getBasename(),
                                               opt_val[gfile]))
                for r,s in z:
                    self.info("%-25s %s (%6.2f)" % ("",s,r))
            self.info("")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("calculateRMSDs runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************
        return

    def generateTopComplexes(self):
        """
        For each receptor/grid, generate complexes with the top poses.  Sort all the complexes by
        the GlideScores.
        """
        self.info("")
        self.info("")
        self.info("--------------------------")
        self.info(" Generating Top Complexes ")
        self.info("--------------------------")
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        start_time = time.time()
        # *************************************************************************
        #self.printFiles()
        self.info("")
        recs = {}      # Keys are grid IDs, values are receptor structures
        topposes = {}  # Keys are grid IDs, values are lists of pose structures
        for dockjob,gridfile,lscale,ligfile in self.dockjobs:
            # Strategy -- go through all the docking results.  These are
            # sorted by GlideScore already, so once we have the top N poses
            # from a file, we don't need to look further.
            gridid = gridfile.getBasename()
            poses = topposes.setdefault(gridid,[])
            pvname = dockjob+self.glide_output_extension
            if not os.path.isfile(pvname):
                self.info("No docking results for job '%s'" % dockjob)
                continue
            for index,st in enumerate(structure.StructureReader(pvname)):
                if index==0:
                    # We require pose-viewer files, so this is the receptor.
                    recs[gridid] = st  # Will this require too much memory?
                    continue
                dscore = st.property[self.GSCOREPROP]
                if (len(poses)==self.generatecomplexes and
                    dscore>poses[-1]):
                    # Already have enough poses, and the rest in this file
                    # will have worse scores.
                    break
                else:
                    # Add the new pose at the appropriate point if it has a
                    # low enough score.
                    newposelist = []
                    added = False
                    for pose in poses:
                        if len(newposelist)==self.generatecomplexes:
                            break
                        if pose.property[self.GSCOREPROP]<=dscore:
                            newposelist.append(pose)
                        else:
                            if not added:
                                newposelist.append(st)
                                added = True
                            if len(newposelist)<self.generatecomplexes:
                                newposelist.append(pose)
                    if not added and len(newposelist)<self.generatecomplexes:
                        newposelist.append(st)
                    poses[:] = newposelist  # Replace with new list
        # Delete empty lists
        for gridid in topposes.keys():
            if not topposes[gridid]:
                del topposes[gridid]
        # Sort grids by GlideScore of top pose
        gridids = topposes.keys()
        gridids.sort(cmp=lambda x,y: cmp(topposes[x][0].property[self.GSCOREPROP],topposes[y][0].property[self.GSCOREPROP]))
        # Write out complexes in blocks by receptor
        outfile = self.jobname+"_topcomplexes.maegz"
        writer = structure.StructureWriter(outfile)
        self.addOutputFileBE(os.path.join(self.workdir,outfile))
        self.info("%-24s %4s %-35s    %8s" % ("Receptor","Top#","Ligand title", "GScore"))
        self.info("-"*77)
        for gridid in gridids:
            recst = recs[gridid]
            for index,ligst in enumerate(topposes[gridid]):
                self.info("%-24s %4d %-35s    %8.2f" % (
                    gridid,(index+1),ligst.title,
                    ligst.property[self.GSCOREPROP]))
                compst = recst.merge(ligst)
                # Add pose properties to complex.
                compst.property.update(ligst.property)
                compst.property['i_xglide_topposenum'] = index+1
                writer.append(compst)
        writer.close()
        self.info("")
        self.info("Complexes written to '%s'." % outfile)
        # *************************************************************************
        # runtime measurement is made by Ban et al.
        # *************************************************************************
        end_time = time.time()
        self.info("generateTopComplexes runtime[sec]: %f"%(end_time - start_time))
        # *************************************************************************

    def backend(self):
        """
        Required by App.  Run the backend from instance attributes set up
        during command-line (and input file) parsing.  Note that no
        command-line arguments are passed to this method; all options for the
        backend should be set via instance attributes.

        Run all subjobs in a subdirectory, to prevent accumulation of too
        many files in the original CWD, if run locally or with -LOCAL.  This
        requires modification of relative file references (including those
        resulting from Job Control file transfer).

        """
        # Opening a file <jobname>.log for output obliterates the stdout from
        # App, so just print to stdout
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        self.info("")
        self.info("="*70)
        self.info("XGlide".center(70))
        self.info(_version.center(70))
        self.info(_copyright.center(70))
        self.info("="*70)
        self.info("")
        self.info("XGlide starting at %s" % time.asctime())
        self.info("")
        self.info("")
        self.info("------------")
        self.info(" Parameters ")
        self.info("------------")
        self.printParameters()
        sys.stdout.flush()
        if not self.stage_completed:
            # New job.  Create working directory.  If one already exists,
            # delete it.
            if os.path.isdir(self.workdir):
                try:
                    shutil.rmtree(self.workdir)
                except:
                    print ""
                    print "Could not remove the existing workdir '%s'." % self.workdir
                    print ""
                    sys.exit(1)
            os.mkdir(self.workdir)
            self.info("")
            self.info("Starting new job...")
            self.info("")
            self.updateFileReferences()
            self.setReceptorAssociations()
        elif os.path.isdir(self.workdir):
            self.info("")
            self.info("Resuming existing job...")
            self.info("")
        else:
            self.error("")
            self.error("Error: Can't resume job without an existing work directory. Exiting.")
            self.error("")
            sys.exit(1)
        os.chdir(self.workdir)
        # Align structures - requires PDB format, so do it before the
        # CONVERT stage.
        if (self.align and (self.complexes or self.receptors) and
            self.stage_completed<self.ALIGN):
            self.alignStructures()
            self.completedStage(self.ALIGN)
        # Convert to Maestro format
        if self.stage_completed<self.CONVERT:
            self.convertFormat()
            self.completedStage(self.CONVERT)
        # Prepare proteins with the command-line PPrep Wizard
        if (self.pprep and self.stage_completed<self.PPREP):
            self.runPPrep()
            self.completedStage(self.PPREP)
        # Split complexes
        if self.stage_completed<self.SPLIT:
            self.splitComplexes()
            self.completedStage(self.SPLIT)
        # Create ligand subsets
        if self.stage_completed<self.SUBSET:
            self.createLigandSubsets()
            self.completedStage(self.SUBSET)
        # LigPrep
        if self.ligprep and self.stage_completed<self.LIGPREP:
            self.runLigPrep()
            self.completedStage(self.LIGPREP)
        # CSearch
        if self.csearch and self.stage_completed<self.CSEARCH:
            self.warning("Warning: CSearch not yet supported.")
            self.completedStage(self.CSEARCH)
        #self.printFiles()
        # SiteMap
        if self.sitemap and self.stage_completed<self.SITEMAP:
            self.generateSites()
            self.completedStage(self.SITEMAP)
        # Grid generation
        if self.receptors and self.stage_completed<self.GRID:
            self.generateGrids()
            self.completedStage(self.GRID)
        # Docking
        if not self.skipdocking and self.stage_completed<self.DOCK:
            self.dockLigands()
            self.completedStage(self.DOCK)
        # Calculate RMSDs.
        if not self.skipdocking and self.stage_completed<self.RMS:
            self.calculateRMSDs()
            self.completedStage(self.RMS)
        # Generate top complexes
        if self.generatecomplexes and not self.skipdocking and self.stage_completed<self.GENTOPCOMPLEXES:
            self.generateTopComplexes()
            self.completedStage(self.GENTOPCOMPLEXES)
        # Merge subset docking results.  This must be done after the RMSD
        # calulations, or it would mess up the pose/reference matching.
        if self.mergesubsetposes and not self.skipdocking and self.stage_completed<self.MERGE and not self.nativeonly:
            # If ligand subsets were created, merge results for each receptor.
            self.glideMerge()
            self.completedStage(self.MERGE)
        os.chdir("..")
        job = None
        try:
            job = jobcontrol.get_backend().getJob()
        except:
            # Not running under Job Control
            pass
        # Collect the log files if a scratch directory is used.
        if job and job.Dir!=job.JobDir:
            logarchivename = os.path.join(self.jobname+"_subjob-logs.tar.gz")
            if os.path.isfile(logarchivename):
                os.remove(logarchivename)
            logarchive = tarfile.open(logarchivename,'w:gz')
            for subjoblog in glob.glob(os.path.join(self.workdir,"*.log")):
                logarchive.add(subjoblog)
            logarchive.close()
            self.addOutputFileBE(logarchivename)
            self.info("")
            self.info("Subjob log files combined into archive '%s'." % logarchivename)
            self.info("")
        self.info("")
        self.info("XGlide terminating normally at %s" % time.asctime())
        self.info("")
        sys.stdout.flush()
        return

    def gui(self):
        """
        Required by App if a GUI is used.  Launch the GUI.  The GUI should call
        the App 'launchBackend' method with any command-line arguments set up
        from the GUI (e.g., "-i <inputfile>", "-HOST <host/queue>").  Lift the
        GUI if it already has been created.

        """
        #if hasattr(self,'appfw'):
        #    self.appfw.deiconify()
        #    self.appfw.lift()
        #    return
        #self.appfw = stkfrwk.AppFramework(
        #    # Xwindow title-bar text
        #    title="MacroModel Conf_Cluster",
        #    # Any button with a 'command' will be added to the application
        #    # button box.  We need a 'Start', 'Write' and 'Close buttons for
        #    # this app
        #    buttons = {
        #        'start': {'command':self.start_job},
        #        'write': {'command':self.write_job},
        #        'close' : {'command':self.quit_gui},
        #    },
        #    dialogs = {
        #        'start': {
        #            'jobname' : 'mmod_conf_cluster_x',
        #            'cpus' : True,
        #            'njobs' : True,
        #            'user' :1,
        #            'incorporation':False
        #        },
        #        'write': {
        #            'jobname' : 'mmod_conf_cluster_x',
        #        }
        #    }
        #)

        #if _in_maestro:
        #    maestro.tk_toplevel_add(self.appfw)
        #else:
        #    self.appfw.mainloop()  
        #return

        print "XGlide GUI not yet supported."
        return

    #def quit_gui(self):
    #    """ 
    #    Callback for the Close button.  Quit the GUI.  If in Maestro, just hide
    #    the panel to preserve the settings.

    #    """
    #    if hasattr(self,'appfw'):
    #        if _in_maestro:
    #            self.appfw.withdraw()
    #        else:
    #            self.destroy_gui()

    #def destroy_gui(self):
    #    """ Destroy the GUI, not just a simple withdraw()."""
    #    if hasattr(self,'appfw'):
    #        if _in_maestro:
    #            maestro.tk_toplevel_remove(self.appfw) 
    #        self.appfw.destroy()
    #        delattr(self,'appfw')
    #    return

    #def write_job(self):
    #    """
    #    Callback for the Write dialog.  This function writesthis GUI's backend
    #    job input file.

    #    The application marshals all the GUI setting which we can parse/use
    #    for running the job as specified.

    #    """

    #def start_job(self):
    #    """
    #    Callback for the Start dialog.  Writes the current GUI settings to an
    #    input file, then starts the job under jobcontrol via 'launchBackend'.

    #    """
    #    # Write stage directives to disk
    #    inp_file = self.write_job()

    #    # Launch the job under jobcontrol
    #    jp = self.appfw.jobparam
    #    jobargs = []
    #    if jp.proj:
    #        jobargs.extend(("-PROJ",jp.proj))
    #    if jp.disp:
    #        jobargs.extend(("-DISP",jp.disp))
    #    if jp.host:
    #        if hasattr(jp,'cpus'):
    #            jobargs.extend(("-HOST",jp.host+":"+str(jp.cpus)))
    #        else:
    #            jobargs.extend(("-HOST",jp.host))
    #    if jp.user:
    #        jobargs.extend(("-USER",jp.user))
    #    job = self.launchBackend(["-i",inp_file]+jobargs)
    #    # Put up the monitor panel if we are under Maestro
    #    if _in_maestro:
    #        self.appfw.monitorJob(job.JobId)
    #    return job


################################################################################
# Main 
################################################################################

if __name__ == '__main__':
    # Run XGlide.
    # When run from the command line, create the App instance (via
    # start_app), which knows how to parse various command-line arguments
    # (-gui, -RESTART, -LOCAL, -NOJOBID).
    start_app(sys.argv[1:])


# EOF
