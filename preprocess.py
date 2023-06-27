from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

### Create the model and the part #####################################################
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-35.0, 25.0), 
    point2=(15.0, -15.0))
	
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-25.0, 20.0), 
    point2=(15.0, -20.0))
	
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -36.0299377441406, 7.33676910400391), value=50.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1])
	
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -5.48028182983398, 32.9954109191895), value=50.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[3], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0])
	
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    31.5213394165039, 3.8087043762207), value=50.0, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[2], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[3])
	
mdb.models['Model-1'].sketches['__profile__'].undo()

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
	
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=50.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
	
del mdb.models['Model-1'].sketches['__profile__']
##########################################################################################

### Create the material and section ######################################################
mdb.models['Model-1'].Material(name='Material-1')

mdb.models['Model-1'].materials['Material-1'].Elastic(table=((113.8, 0.342), ))

mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
##########################################################################################

### Create a set for section assignment, and then assign to previously created section ###
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.getSequenceFromMask(('[#1 ]', 
    ), ), name='Set-1')
	
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)
	
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
####################################################################################

### Add the part to assembly as an instance #########################################
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
#####################################################################################

### Seed the instance and mesh the part #############################################
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=50.0)
	
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
	
mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=C3D8R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT, 
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].cells.getSequenceFromMask(
    ('[#1 ]', ), ), ))
#####################################################################################

### Create the node sets from nodes selected in cae GUI #############################
mdb.models['Model-1'].rootAssembly.Set(name='Nxfixed', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].nodes.getSequenceFromMask(
    mask=('[#f ]', ), ))
	
mdb.models['Model-1'].rootAssembly.Set(name='Nyfixed', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].nodes.getSequenceFromMask(
    mask=('[#55 ]', ), ))
	
mdb.models['Model-1'].rootAssembly.Set(name='Nzfixed', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].nodes.getSequenceFromMask(
    mask=('[#cc ]', ), ))
	
mdb.models['Model-1'].rootAssembly.Set(name='Nzdisped', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].nodes.getSequenceFromMask(
    mask=('[#33 ]', ), ))
######################################################################################	

### Create fixed boundary conditions #################################################
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Nxfixed'], u1=SET, u2=UNSET
    , u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
	
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Nyfixed'], u1=UNSET, u2=SET
    , u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
	
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-3', 
    region=mdb.models['Model-1'].rootAssembly.sets['Nzfixed'], u1=UNSET, u2=
    UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
######################################################################################

	
### Create the step and adjust the prescribed time step ##############################
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

mdb.models['Model-1'].steps['Step-1'].setValues(initialInc=0.01, noStop=OFF, 
    timeIncrementationMethod=FIXED)
######################################################################################	

### Create the displacement boundary condition #######################################
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-4', region=mdb.models['Model-1'].rootAssembly.sets['Nzdisped'], u1=
    UNSET, u2=UNSET, u3=0.3, ur1=UNSET, ur2=UNSET, ur3=UNSET)
######################################################################################
	
### Edit the default output requests #################################################
del mdb.models['Model-1'].historyOutputRequests['H-Output-1']
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEMAG', 'U'))
######################################################################################
	
### Create the Job for submission ####################################################
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
    ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
######################################################################################

### Submit the job ###################################################################	
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)