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

def informUser  ( msg
                , prefix = ""
                , newLine = "\n"
                , marginTop = 0
                , marginBot = 0
                , end = "\n"
                ):
    for i in range(marginTop): print()
    print(prefix + msg.replace(newLine,newLine+prefix), end=end)
    for i in range(marginBot): print()
    return None

####################################################################################################################################

def note( msg
        , methodName = ""
        , newLine = "\n"
        , marginTop = 0
        , marginBot = 0
        , end = "\n"
        ):
    informUser  ( msg
                , prefix = methodName + " - NOTE: "
                , newLine = newLine
                , marginTop = marginTop
                , marginBot = marginBot
                , end = end
                )
    return None

####################################################################################################################################

def warn( msg
        , methodName = ""
        , newLine = "\n"
        , marginTop = 0
        , marginBot = 0
        , end = "\n"
        ):
    informUser  ( msg
                , prefix = methodName + " - WARNING: "
                , newLine = newLine
                , marginTop = marginTop
                , marginBot = marginBot
                , end = end
                )
    return None

####################################################################################################################################

def abort   ( msg
            , methodName = ""
            , newLine = "\n"
            , marginTop = 0
            , marginBot = 0
            , end = "\n"
            ):
    informUser  ( msg
                , prefix = methodName + " - FATAL: "
                , newLine = newLine
                , marginTop = marginTop
                , marginBot = marginBot
                , end = end
                )
    raise Exception( "Fatal error occurred. Gracefully exiting." )

####################################################################################################################################
