# A.Prochazka at gsi.de
# This is a small jupyter magic to execute ROOT scripts and plot the canvases.
# 
# installation: just copy this file to your ipynb directory
#
# last update: 16.8.2016
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
                                
import subprocess
from IPython.display import display, Image

@magic_arguments()
@argument('-c','--canvas',type=str,help='-c c1,c2 shows canvases from root macro, TCanvas variable has to be defined')
@argument('-i','--include',type=str,help='include header files before main function')
@argument('-f','--file',type=str,help='Save macro to file, extension .C is added automatically')
@argument('-l','--load',type=str,help='Load root file')
@argument('-e','--noerrors',action='store_true',help='do not output error and warning messages')
@argument('-s','--nostdout',action='store_true',help='do not output stdout')
@register_cell_magic
def rootc(line, cell):
    args = parse_argstring(rootc, line)
    funcname = "runrootc"
    filename = "runrootc.C"; # default name for file and function
    rootfile = ""
    canvases = []
    includes = []
    if(args.file):
        funcname = args.file
        filename = funcname + ".C"
    if(args.canvas):
        canvases = args.canvas.split(',')
    if(args.include):
        includes = args.include.split(',')    
    if(args.load):
        rootfile = args.load
    
    # write cell content to the file
    with open(filename,"w") as fw:
        for inc in includes:
            fw.write('#include "%s"\n'%inc);
        fw.write('void %s(){\n'%(funcname))  # wrap everything in function
        fw.write(cell)
        for canvas in canvases:  #  save canvases as images
            canvassave = "\n%s->Print(\"%s.png\");"%(canvas,canvas)
            fw.write(canvassave)
        fw.write('\n}\n')
    
    # run root macro
    r = subprocess.run(['root','-l','-q','-b',rootfile,'-x',filename],stdout=None if(args.nostdout) else subprocess.PIPE,stderr=None if(args.noerrors) else subprocess.STDOUT)
    if(not args.nostdout):
        print(r.stdout.decode())
    
    # show images of canvases
    if(len(canvases)):
        i1,*i2 = [Image(x+'.png') for x in canvases] 
        return display(i1,*i2)
