import maya.cmds as cmds

def createHelicalGear(numTeeth, gearHeight, gearRadius, gearThickness, teethHeight, rotationSpeed, scale=1, initialRotation=0):
    '''Create a helical gear model with specified parameters.'''
    # Creates the gear model
    gear = cmds.polyPipe(sa=numTeeth * 2, h=gearHeight, r=gearRadius, t=gearThickness, name="gear")
    intStartFace = numTeeth * 2 * 2
    intEndFace = numTeeth * 2 * 3 - 1

    # Selects faces for extrusion
    cmds.select(clear=True)
    for i in range(intStartFace, intEndFace, 2):
        cmds.select(gear[0] + ".f[%d]" % i, add=True)

    # Extrudes the selected faces
    cmds.polyExtrudeFacet(ltz=teethHeight * 0.2, lsx=1)
    cmds.polyExtrudeFacet(ltz=teethHeight * 0.8, lsx=0.5)

    # Sets attributes and clean up history
    cmds.select(gear[0])
    cmds.addAttr(longName='gearRadius', shortName='gr', attributeType='float')
    cmds.addAttr(longName='teeth', shortName='tee', attributeType='short')
    cmds.setAttr(gear[0] + '.gr', gearRadius)
    cmds.setAttr(gear[0] + '.tee', numTeeth)

    # Scales the gear
    cmds.scale(scale, scale, scale, gear[0])
    
    # Sets initial rotation
    cmds.setAttr(gear[0] + ".rotateY", initialRotation)

    return gear

def animateGears(gear1, gear2, gear3, gear4, rotationSpeed):
    '''Animate the rotation of gears.'''
    cmds.expression(name="gear1RotationExp", alwaysEvaluate=True, s="{0}.rotateY = time * {1}".format(gear1, rotationSpeed))
    cmds.expression(name="gear2RotationExp", alwaysEvaluate=True, s="{0}.rotateY = -time * {1}".format(gear2, rotationSpeed))
    cmds.expression(name="gear3RotationExp", alwaysEvaluate=True, s="{0}.rotateY = time * {1}".format(gear3, rotationSpeed))
    cmds.expression(name="gear4RotationExp", alwaysEvaluate=True, s="{0}.rotateY = -time * {1}".format(gear4, rotationSpeed))

def createUI():
    '''Simple UI for controlling gear animation.'''
    if cmds.window("gearAnimationUI", exists=True):
        cmds.deleteUI("gearAnimationUI")

    cmds.window("gearAnimationUI", title="Gear Animation UI")
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Animation Settings", align="center")

    cmds.separator(style="none", height=10)

    cmds.intFieldGrp("rotationSpeedField", label="Rotation Speed", value1=10)
    cmds.intFieldGrp("durationField", label="Animation Duration", value1=10)
    cmds.colorSliderGrp("gearColorSlider", label="Gear Color")

    cmds.separator(style="none", height=10)

    cmds.button(label="Animate", command=animateGearsCmd)
    cmds.showWindow("gearAnimationUI")

def animateGearsCmd(*args):
    '''Callback function for animating gears.'''
    rotationSpeed = cmds.intFieldGrp("rotationSpeedField", query=True, value1=True)
    duration = cmds.intFieldGrp("durationField", query=True, value1=True)
    gearColor = cmds.colorSliderGrp("gearColorSlider", query=True, rgb=True)

    # Creates gears with different scales
    gear1 = createHelicalGear(20, 1, 10, 3, 0.5, rotationSpeed, scale=1)
    gear2 = createHelicalGear(20, 1, 10, 3, 0.5, -rotationSpeed, scale=0.8, initialRotation=180)
    gear3 = createHelicalGear(20, 1, 10, 3, 0.5, rotationSpeed, scale=0.6)
    gear4 = createHelicalGear(20, 1, 10, 3, 0.5, -rotationSpeed, scale=0.4, initialRotation=180)

    # Positions the gears closer together, considering their scales and radii
    radius1 = 10 * 1  # gearRadius * scale
    radius2 = 10 * 0.8
    radius3 = 10 * 0.6
    radius4 = 10 * 0.4

    # Calculates positions based on gear radii
    gap = 0.2  # small gap to prevent overlap
    cmds.move(0, 0, 0, gear1[0])
    cmds.move(radius1 + radius2 + gap, 0, 0, gear2[0])  # Adjust position of the second gear
    cmds.move(radius1 + 2 * radius2 + radius3 + 2 * gap, 0, 0, gear3[0])  # Adjust position of the third gear
    cmds.move(radius1 + 2 * radius2 + 2 * radius3 + radius4 + 3 * gap, 0, 0, gear4[0])  # Adjust position of the fourth gear

    # Sets gear color
    for gear in [gear1, gear2, gear3, gear4]:
        cmds.setAttr(gear[0] + '.overrideEnabled', 1)
        cmds.setAttr(gear[0] + '.overrideRGBColors', 1)
        cmds.setAttr(gear[0] + '.overrideColorRGB', *gearColor)

    animateGears(gear1[0], gear2[0], gear3[0], gear4[0], rotationSpeed)

createUI()