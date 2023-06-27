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