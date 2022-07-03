class Pendulum:
    def __init__(self, id):
        self.id = id
    def setRotationAtFrame(self, rotation, frame):
        theta = rotation
        bpy.context.scene.frame_current = frame
        bpy.ops.object.rotation_clear(clear_delta=False)
        bpy.data.objects['s'+self.id].select_set(True)
        bpy.ops.transform.rotate(value=theta, orient_axis='Y')
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        bpy.data.objects['m'+self.id].select_set(True)
        bpy.ops.transform.rotate(value=theta, orient_axis='Y')
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')


c = 0
gap = 0.1

def createPendulum(L):
    global c
    sw = 0.002
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, location=(0, gap*c, 0))
    bpy.ops.transform.resize(value=(sw/2, sw/2, sw/2))
    bpy.ops.transform.translate(value=(0, 0, -L/2))
    bpy.ops.transform.resize(value=(1, 1, L/sw))
    bpy.context.active_object.name = 's'+str(c)
    #bpy.data.objects['s'+str(j)].data.materials.append(bpy.data.materials['String'])
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, enter_editmode=False, location=(0, gap*c, -1*L))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.context.active_object.name = 'm'+str(c)
    bpy.data.objects['m'+str(c)].data.materials.append(bpy.data.materials['mass'])
    bpy.context.scene.frame_current = 0
    pendulum = Pendulum(str(c))
    c += 1
    return pendulum 
    
def getAmountOfFrames():
    return bpy.context.scene.frame_end

def getFPS():
    return bpy.context.scene.render.fps

def createAnimation():
    n = 15 #number of pendulums
    g = 9.8 #gravity
    s = 45 #The whole animation period in seconds
    for i in range(n): #repeats the following n times
        Q = 25 + i #Amount of oscilations in the animation period
        #Q increases by 1 unit, each time 1 pendulum is added
        w = (Q*2*pi)/s
        L = g/pow(w,2) #String Length
        pendulum = createPendulum(L) #Creates the 3D Object
        theta_max = theta=asin(0.1/L) #The max amount of degrees
        #that the pendulum will reach.
        for frame in range(getAmountOfFrames()): #for each video frame
            t = frame / getFPS() #converts the position of the frame
            #into the time
            theta = theta_max * cos(w*t) #then calculates
            #the angle for the pendulum at that time
            pendulum.setRotationAtFrame(theta, frame) #sets the rotation
   
createAnimation()
