# Python Scripting in Abaqus


One of the main benefits of running simulations rather than physical experiments is the ability generate significantly larger numbers of results for less cost. With automation through coding, the ease at which larger numbers of simulations can be ran and the results processed increases. Python is a powerful and easy to learn scripting language that has been widely utilized by the scientific community for data processing, running calculations, and automation. Abaqus has a built in python API that offers many benefits when utilized. From easily extracting data from an Abaqus output database to full simulation automation, the tools offered are powerful. Presented here are example python scripts for interfacing with Abaqus that showcase some of the available features and benefits of using python scripting with Abaqus.

The scripts here are based on and use a simple single-element cube being pulled in tension with a linear-elastic material model shown below in Fig. 1. All of the scripts created were tested on Abaqus 2017.
200px-Model_Ex.PNG
Figure 1: Deformed cube being pulled in tension.
# Pre-processing and Running Simulations

When working in Abaqus CAE, there is a corresponding python command for every action performed. These commands are recorded in the .jnl file that is stored in the current working directory. To create a python script that can generate a model, mesh it, and run the simulation the model is first created in the CAE and then saved. From here the corresponding .jnl file can be saved as a python script with the .py extension. All of the required abaqus specific packages will be already imported at the top of the script. Keep in mind that the CAE appends to this file with every action taken in the CAE. Therefore these files can become quite long and messy. It is recommended to save the CAE file before performing actions that you want recorded, and then saving again when finished. There will be a commented out line in the .jnl file for every save instances. Anything outside of this block can be deleted. The scripts presented below have been sorted through with unnecessary lines deleted, and have been commented to explain what each sections does.

This script must be run with Abaqus CAE. There are two ways to do this: (i) in the Abaqus CAE GUI, go to file and then to Run Script (ii) to run outside of the GUI type the following command into a command line.
```
 abaqus cae -noGUI python_script.py
```

The model will be created and run with all relevant simulation files being generated in the current directory.

preprocess.py
```
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
```
To illustrate some of the automation capabilities of scripting with Abaqus, the next script presented has been created to show how a mesh convergence study can be quickly and easily performed. The previously presented script has been slightly modified to contain the meshing and boundary condition regions in a for loop to loop over a list of different mesh seed values. This allows for a number of different mesh densities to be generated, and ran sequentially just by running this one script. The script can be altered to only generate input files, to only run the simulations, or to perform both.

preprocess2.py
```
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


### Create multiple input files for varying mesh densities ##########################

seeds = [50, 30, 20, 10]

for seed_value in seeds:
	
	
	inp_name='SingleEl-%s'%str(seed_value)
	
	### Seed the instance and mesh the part #############################################
	mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
		minSizeFactor=0.1, regions=(
		mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=seed_value)  # This is where the seed_value is set
		
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
	mdb.models['Model-1'].rootAssembly.Set(faces=
		mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
		('[#10 ]', ), ), name='Nzdisped')
	mdb.models['Model-1'].rootAssembly.Set(faces=
		mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
		('[#20 ]', ), ), name='Nzfixed')
	mdb.models['Model-1'].rootAssembly.Set(faces=
		mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
		('[#4 ]', ), ), name='Nxfixed')
	mdb.models['Model-1'].rootAssembly.Set(faces=
		mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
		('[#2 ]', ), ), name='Nyfixed')
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
		'S','E','PE', 'PEMAG', 'U'))
	######################################################################################
		
	### Create the Job for submission ####################################################
	mdb.Job(name=inp_name,model='Model-1',description='',type=ANALYSIS)
	######################################################################################

	### Submit the job ###################################################################	
	mdb.jobs[inp_name].writeInput(consistencyChecking=OFF)
	
	# Comment out the following line to only generate the input files.
	mdb.jobs[inp_name].submit(consistencyChecking=OFF)
```
# Post-processing and Extracting Results

Arguably the most utility from python scripting in Abaqus can be seen when extracting and processing simulation results. Abaqus offers the ability to directly extract element, node, or integration point simulation results and post-processing these results as desired all from a single python script. The code presented extracts the S33 and E33 stress and strain values from the output database file generated in the first script presented and saves them to a tab delimited .txt file. To run this python script, either select Run Script under File in the CAE, or the following can be entered into the command line.

```
abaqus python python_script.py
```

postprocess.py
```
import sys
from odbAccess import *
from abaqusConstants import*
from types import IntType
import numpy as np

# *.odb means every .odb file in the directory. Add directory path to the beginning: 'C:\path\*.odb'
odb_name='SingleEl-50'

# desired name for the results file
results_name=odb_name+'S33VE33'

#Initializing Arrays
DAT = []
info = []



#Opening the odb
odb = openOdb(odb_name+'.odb', readOnly=True)
assembly = odb.rootAssembly
instance = assembly.instances.keys()[0]

#Extracting Step 1, this analysis only had one step
step1 = odb.steps.values()[0]


#Creating a for loop to iterate through all frames in the step
for x in odb.steps[step1.name].frames:


####Setting temporary array to empty
	temp = []


####Progress report
#	print('\nExtracting from Frame:\t'+str(j))


#####Reading stress and strain data from the model 
	odbSelectResults = x.fieldOutputs['S']
	odbSelectResults2 = x.fieldOutputs['E']

	field1 = odbSelectResults
	field2 = odbSelectResults2

####Reading COORDS data from the top node set

####Storing Stress and strain values for the current frame

	# stress values
	for s in field1.values:
		info = []
		temp.append(s.data[2]) # the values in s.data are organized as follows: [S11,S22,S33,S12,S13,S23]
	
	# strain values
	for e in field2.values:
		temp.append(e.data[2]) # the values here are organized similarly to the stress values. This grabs E33

	DAT.append(temp)
	
		
####Writing to a .csv file
with open(results_name+'.txt', 'w') as f:
	np.savetxt(f,DAT,delimiter='	')	



#Close the odb
odb.close()

The final example script presented here uses python with Abaqus CAE to create a video of the simulation results for the output database generated by the first script presented. Just as any action performed in the CAE is recorded in the .jnl file, any action performed in the Abaqus/Viewer (this is the GUI used to view .odb files) is recorded in the .rpy file. This file is also appended to with every action and the same preparation must be used as with the .jnl file. Run this script with Abaqus CAE with or without the GUI as described in the first section of this page.
The code below opens the .odb file, rotates the model, and saves an animation of the simulation results to a .avi file.

from abaqus import *
from abaqusConstants import *
from viewerModules import *
from driverUtils import executeOnCaeStartup
# Video file name and directory ################################################
filename='/cavs/projects/ARL.00/ARL.02/Priddy_Research_Group/Furr/ICME_2019/05_Contributions/ODB_Video'

executeOnCaeStartup()
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=301.153137207031, 
    height=205.33332824707)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()

### Open the odb #################################################################
o2 = session.openOdb(name='Job-1.odb')

session.viewports['Viewport: 1'].setValues(displayedObject=o2)

session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_UNDEF, CONTOURS_ON_DEF, ))
##################################################################################
	
### Rotate the part view in the viewport #########################################
session.viewports['Viewport: 1'].view.setValues(nearPlane=135.715, 
    farPlane=227.303, width=108.211, height=63.6861, cameraPosition=(38.7191, 
    -30.3183, 201.295), cameraUpVector=(-0.470794, 0.878981, -0.075794), 
    cameraTarget=(1.58932, 4.00627, 25.4952))
	
session.viewports['Viewport: 1'].view.setValues(nearPlane=129.662, 
    farPlane=236.327, width=103.385, height=60.8457, cameraPosition=(86.3827, 
    -129.827, 116.1), cameraUpVector=(-0.387921, 0.646482, 0.656946), 
    cameraTarget=(1.21705, 4.78346, 26.1606))
##################################################################################
### Set the ODB to display S33 stress ############################################	
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S33'), )
##################################################################################	
	
### Set the animation settings ###################################################
#: AVI Codec set to:Microsoft Video 1
session.aviOptions.setValues(
    codecOptions='[16]:enfdfgedbiaaaaaaaeaaaaaaelaaaaaa', 
    compressionQuality=100)
	
session.imageAnimationOptions.setValues(vpDecorations=ON, vpBackground=OFF, 
    compass=OFF, timeScale=1, frameRate=16)
	
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)

### Save the animation ############################################################
session.writeImageAnimation(
    fileName=filename, 
    format=AVI, canvasObjects=(session.viewports['Viewport: 1'], ))
session.animationController.setValues(animationType=NONE)
```

The python scripts that have been presented here are simple examples of what can be done with scripting in Abaqus. For further reading on the subject, see the Abaqus documentation.
Abaqus scripting user guide http://abaqus.software.polimi.it/v2016/books/cmd/default.htm?startat=pt01ch03s02.html
Abaqus scripting reference guide http://abaqus.software.polimi.it/v2016/books/ker/default.htm
A few points to keep in mind:

* Abaqus uses its own installation of python and proprietary python packages. These scripts cannot be directly run with a regular instillation of python
* The structure and coding of the extraction script is going to depend on how the model was structured when originally created. How and what kind of sets are created can change how certain results are stored.
* Take the time to read the documentation and test your code. 