import re
import string
import subprocess
import os
import sys

from tools import killableprocess

from settings import PATH_BIN, PATH_TEMP, TIMEOUT
import numpy as np



def exec_fortran(bin):
    args = []
    if sys.platform != 'win32':
        #On any non-Windows system, we run binaries over wine
        args.append('wine')

    args.append( os.path.join(PATH_BIN, bin + '.exe'))

    return killableprocess.call(args, cwd=PATH_TEMP, timeout=TIMEOUT)    #kill if not return in TIMEOUT seconds



def get_numbers(data_raw, prefix=None):
    """recibes any string and return a list of founded numbers as strings"""

    re_float = re.compile("""[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?""")
    numbers = re.findall(re_float, data_raw)
    if prefix:
        numbers = [n for n in numbers if n.startswith(prefix)]
    return map(string.strip, numbers)



def write_conparin(sense, model, data):
    """Write the input file CONPARIN.DAT ". data could be EOS variables or 
        model paramater""" 

    filename = 'CONPARIN.DAT'
    template = "{0}  {1}\n {2}"
    output = template.format (sense, model, "  ".join( data )) 
    with open( os.path.join(PATH_TEMP, filename), 'w') as fh:
        fh.write(output)
        fh.close()
    

def write_gpecin(model, comp1, comp2, ncomb=0, ntdep=0, k12=0.0, l12=0.0, max_p=2000):
    """
    compX -> ('NAME', (const1, ..., constN), (param1, ... , paramM))
    """

    filename = 'GPECIN.DAT'
    template = "{0}\n{1} {2}\n%s" % "".join(['{%d}\n' % i for i in range(3, 12)])
    output = template.format(model, ncomb, ntdep, comp1[0], "  ".join(map(str, comp1[1])), 
                            "  ".join(map(str, comp1[2])), comp2[0], "  ".join(map(str, comp2[1])), 
                            "  ".join(map(str, comp2[2])), k12, l12, max_p)
    
    with open(os.path.join(PATH_TEMP, filename), 'w') as fh:     #writing in path_bin instead path_temp
        fh.write(output)
        fh.close()

def read_conparout(model_id):
    """COMPAROUT.DAT has two lines of data. First one is EOS vars and second 
        model parameters. """

    if model_id in (4,6):
        ret = exec_fortran('PCSAFT')
    else:
        ret = exec_fortran('ModelsParam')

    if ret == 0:
        filename = 'CONPAROUT.DAT'
        with open(os.path.join(PATH_TEMP, filename), 'r') as fh:
            output = [get_numbers(line) for line in fh.readlines()]
            fh.close()

        return output
                
        
def read_gpecout():
    """Parses an gpecout.dat, detects numeric blocks and create arrays with them"""

    ret = exec_fortran('GPEC')  #generate gpecout.dat
    

    filename = 'GPECOUT.DAT'
    curve_types = {'VAP':4, 'CRI':5, 'CEP':6, 'LLV':10 } #type:significatives columns

    tokens = {}         #{(begin,end):'type', ...}
    begin = end = 0
    
    with open(os.path.join(PATH_TEMP, filename), 'r') as fh:
        number_of_lines = len(fh.readlines())
        fh.seek(0)
        
        #give skip from header and skip from footer
        for line_number, line in enumerate(fh):
            if begin <= end:
                #print 'begin <= end'
                if line.strip() in curve_types:
                    begin = line_number + 1
                    curve_type = line.strip()
            else:
                if not line.strip():
                    end = line_number
                    tokens[(begin, end)] = curve_type
        
        curves = []
        token_keys = tokens.keys()
        token_keys.sort()

        for (begin, end) in token_keys:
            #print (begin,end)
            fh.seek(0)
            temp_file_path = os.path.join(PATH_TEMP, 'temp_gpecout.dat')            #TODO rethink this!
            with open(temp_file_path, 'w') as fho:
                #write lines just of the block between (begin,end)
                
                
                for l,line in enumerate(fh):
                    if begin <= l < end:
                        fho.write( line.strip('*') )		#sometimes there are "*" chars which must be removed
                fho.close()
            
            #retrieve significative columns from a dictionary. (begin,end)=>type=>num_cols 
            significatives_cols= range(curve_types[tokens[(begin, end)]])     

            curve = np.loadtxt(temp_file_path, usecols=significatives_cols)
            curves.append(curve)

        fh.close()
    return curves

