####################################################################################################################################
####################################################################################################################################
####
####   MIT License
####
####   ParaMonte: plain powerful parallel Monte Carlo library.
####
####   Copyright (C) 2012-present, The Computational Data Science Lab
####
####   This file is part of the ParaMonte library.
####
####   Permission is hereby granted, free of charge, to any person obtaining a 
####   copy of this software and associated documentation files (the "Software"), 
####   to deal in the Software without restriction, including without limitation 
####   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
####   and/or sell copies of the Software, and to permit persons to whom the 
####   Software is furnished to do so, subject to the following conditions:
####
####   The above copyright notice and this permission notice shall be 
####   included in all copies or substantial portions of the Software.
####
####   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
####   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
####   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
####   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
####   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
####   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
####   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
####
####   ACKNOWLEDGMENT
####
####   ParaMonte is an honor-ware and its currency is acknowledgment and citations.
####   As per the ParaMonte library license agreement terms, if you use any parts of 
####   this library for any purposes, kindly acknowledge the use of ParaMonte in your 
####   work (education/research/industry/development/...) by citing the ParaMonte 
####   library as described on this page:
####
####       https://github.com/cdslaborg/paramonte/blob/main/ACKNOWLEDGMENT.md
####
####################################################################################################################################
####################################################################################################################################

import numpy as np
from _SpecBase import inputFileDelim

####################################################################################################################################
#### SpecDRAM specification type-checking class
####################################################################################################################################

def adaptiveUpdateCount(adaptiveUpdateCount):
    if isinstance(adaptiveUpdateCount,int):
        return "adaptiveUpdateCount=" + str(adaptiveUpdateCount) + inputFileDelim
    else:
        raise TypeError("The input specification, adaptiveUpdateCount, must be of type int.")

####################################################################################################################################

def adaptiveUpdatePeriod(adaptiveUpdatePeriod):
    if isinstance(adaptiveUpdatePeriod,int):
        return "adaptiveUpdatePeriod=" + str(adaptiveUpdatePeriod) + inputFileDelim
    else:
        raise TypeError("The input specification, adaptiveUpdatePeriod, must be of type int.")

####################################################################################################################################

def greedyAdaptationCount(greedyAdaptationCount):
    if isinstance(greedyAdaptationCount,int):
        return "greedyAdaptationCount=" + str(greedyAdaptationCount) + inputFileDelim
    else:
        raise TypeError("The input specification, greedyAdaptationCount, must be of type int.")

####################################################################################################################################

def delayedRejectionCount(delayedRejectionCount):
    if isinstance(delayedRejectionCount,int):
        return "delayedRejectionCount=" + str(delayedRejectionCount) + inputFileDelim
    else:
        raise TypeError("The input specification, delayedRejectionCount, must be of type int.")

####################################################################################################################################

def burninAdaptationMeasure(burninAdaptationMeasure):
    if isinstance(burninAdaptationMeasure,(int,float)):
        return "burninAdaptationMeasure=" + str(burninAdaptationMeasure) + inputFileDelim
    else:
        raise TypeError("The input specification, burninAdaptationMeasure, must be of type float.")

####################################################################################################################################

def delayedRejectionScaleFactorVec(delayedRejectionScaleFactorVec):
    if isinstance(delayedRejectionScaleFactorVec,(list,tuple,np.ndarray)):
        return "delayedRejectionScaleFactorVec=" + str(np.array(list(delayedRejectionScaleFactorVec)).flatten()).strip('[]') + inputFileDelim
    else:
        raise TypeError("The input specification, delayedRejectionScaleFactorVec must be list, tuple, or numpy vector of ndim or less elements of type float.")

####################################################################################################################################

def helpme(specification = ""):
    """
    |
    Return help on the input ParaDRAM specification.
    If no input is provided, then the web-link to the 
    entire list of ParaDRAM specifications will be output.

        **Parameters**

            specification
                A string that can take be any of the simulation 
                specifications of a ParaDRAM object, such as, 
                ``"chainSize"``, ``"sampleSize"``, ...

        **Returns**

            None

    """
    import _paramonte as pm
    if isinstance(specification,str):
        if specification!="": specification = "#" + specification.lower()
    else:
        pm.abort( msg   = "The input argument to helpme() function must be a string whose value \n"
                        + "can be the name of one of the specifications of the ParaDRAM sampler.\n"
                        + "For example, to get information about the variable `chainSize`, try:\n\n"
                        + "    pmpd.spec.helpme(\"chainSize\")\n\n"
                        + "where ``pmpd`` is the name of the ParaDRAM sampler object.\n"
                        + "For more information and examples on the usage, visit:\n\n"
                        + "    " + pm.website.home.url
                , methodName = pm.names.paradram
                , marginTop = 1
                , marginBot = 1
                )

    print("Visit: " + pm.website.home.usage.paradram.specifications.url + specification)

####################################################################################################################################
