import mdl
from display import *
from matrix import *
from draw import *

basename = ""

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """
def first_pass( commands ):
    
    num_frames = 0
    basename = "default"

    for cmd in commands:
        if cmd[0] == "frames":
            num_frames = cmd[1]
    
        if cmd[0] == "basename":
            basename = cmd[1] 
            

    if num_frames == 0:
        return 0
        
    if basename == "default":
        print "basename: default"
    print "first"
    return num_frames,basename,second_pass(commands, num_frames)
    

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):
    print "second"

    frames = []
    knobdict = {}
    i = 0
#    while i < 50:
    '''
    for cmd in commands:
        if cmd[0] == "vary":
            knobdict[cmd[1]] = 0;
    '''
    while i < num_frames:
#        print str(i)
        new_knob = {}
        for cmd in commands:
            if cmd[0] == "vary":
                knob = cmd[1]
                #print knob+" "+str(cmd[2])
                start = float(cmd[2])
                end = float(cmd[3])
                startval = float(cmd[4])
                endval = float(cmd[5])
#                print knob+" "+str(float((endval-startval)/(end-start))*(i-start))
                if i>=start and i<=end:                    
                    new_knob[knob] = startval + (endval-startval)/(end-start)*(i-start);
 #                   print knob + " " + str(startval + float((endval-startval)/(end-start))*(i-start))
        frames.append(new_knob)    
        i+=1
    return frames


def run(filename):
    """
    This function runs an mdl script
    """

    p = mdl.parseFile(filename)
    #print str(p)
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."

    (num_frames,basename,knob_vals) = first_pass(commands) 
    print str(num_frames)
    print basename
    i = 0
    while i < num_frames:
        parse(commands, basename,knob_vals[i],i)
        i+=1


def parse(commands,basename, knobs, i):
    print str(knobs)
    
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )
    
    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    
    for command in commands:
        #print command
        c = command[0]
        args = command[1:]

        if c == 'box':
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'sphere':
            add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'torus':
            add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'move':
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'scale':
            tmp = make_scale(args[0], knobs[args[3]]*args[1], knobs[args[3]]*args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'rotate':
            theta = knobs[args[2]]*args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        elif c == 'push':
            stack.append([x[:] for x in stack[-1]] )
        elif c == 'pop':
            stack.pop()
        elif c == 'display':
            display(screen)
        elif c == 'save':
            save_extension(screen, args[0])
    #print basename
    save_extension(screen, "anim/" + basename + "%03d"%i + ".png")

        
#    first_pass(commands)
