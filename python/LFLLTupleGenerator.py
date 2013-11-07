#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import argparse
import sys
import os.path
import errno

from string import Template

LFLLTUPLE_NAME = 'LFLLTuple.h'
LFLLTUPLEDETAIL_NAME = 'LFLLTupleDetail.h'

LFLLTUPLE_DIR = 'lfll/engine/'
LFLLTUPLEDETAIL_DIR = 'lfll/engine/detail/'

LFLL_DEFAULT_EXPORT_DIR = './'


LFLLTUPLE_MAIN_STR_TEMPLATE = """\
/*
The MIT License (MIT)

Copyright (c) 2013 Nicolas Pauss

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#ifndef ${headerGuard}
#define ${headerGuard}


// This file is automatically generated by python/LFLLTupleGenerator.py

#include <lfll/engine/LFLLDefinitions.h>
#include <${lfllTupleDetailDir}${lfllTupleDetailName}>


LFLL_BEGIN_NAMESPACE

/**
 * \\brief Tuple of pointers.
 *
 * This tuple hold pointers of given values.
 * If you want a real tuple, use std::tuple (C++11) or boost::tuple
 * You can create this tuple more easily by using makeLFLLTuple()
 */
template <${defClassAll}>
class LFLLTuple
{
	/**
	 * \\brief Get element at index I
	 * \\tparam I Index of element
	 * \\param tuple Tuple
	 * \\return Pointer to element
	 */
    template <size_t I, ${defClassAlter}>
    friend
    typename detail::LFLLTupleValueTypes<I, $useClassAlter>::type*
    getLFLLTuple(LFLLTuple<$useClassAlter>& tuple);
    
	/**
	 * \\brief Get element at index I
	 * \\tparam I Index of element
	 * \\param tuple Tuple
	 * \\return Pointer to element
	 */
    template <size_t I, ${defClassAlter}>
    friend
    const typename detail::LFLLTupleValueTypes<I, $useClassAlter>::type*
    getLFLLTuple(const LFLLTuple<$useClassAlter>& tuple);

public:
	/// Static tuple size
    static const size_t tupleSize = detail::LFLLTupleImpl<$useClassAll>::tupleSize;

public:
	/**
	 * \\brief Constructor with value pointers
	 */
    LFLLTuple($argsPtrWithTypeAndDefault)
        : m_impl($argsPtrAll)
    {}
	
	/**
	 * \\brief Get tuple size
	 * \\return Tuple size
	 */
    size_t size() const
    {
        return tupleSize;
    }

	/**
	 * \\brief Get element at index I
	 * \\tparam I Index of element
	 * \\return Pointer to element
	 */
    template <size_t I>
    typename detail::LFLLTupleValueTypes<I, $useClassAll>::type*
    get()
    {
        typedef detail::LFLLTupleElementTypes<I, I, $useClassAll>
            ElementTypes;

        return static_cast<typename ElementTypes::type&>(m_impl).get();
    }

	/**
	 * \\brief Get element at index I
	 * \\tparam I Index of element
	 * \\return Pointer to element
	 */
    template <size_t I>
    const typename detail::LFLLTupleValueTypes<I, $useClassAll>::type*
    get() const
    {
        typedef detail::LFLLTupleElementTypes<I, I, $useClassAll>
            ElementTypes;

        return static_cast<const typename ElementTypes::type&>(m_impl).get();
    }

private:
    detail::LFLLTupleImpl<$useClassAll>
        m_impl;
};

/**
 * \\brief Get element at index I
 * \\tparam I Index of element
 * \\param tuple Tuple
 * \\return Pointer to element
 */
template <size_t I, $defClassAll>
inline
typename detail::LFLLTupleValueTypes<I, $useClassAll>::type*
getLFLLTuple(LFLLTuple<$useClassAll>& tuple)
{
    typedef detail::LFLLTupleElementTypes<I, I, $useClassAll>
        ElementTypes;

    return static_cast<typename ElementTypes::type&>(tuple.m_impl).get();
}

/**
 * \\brief Get element at index I
 * \\tparam I Index of element
 * \\param tuple Tuple
 * \\return Pointer to element
 */
template <size_t I, $defClassAll>
inline
const typename detail::LFLLTupleValueTypes<I, $useClassAll>::type*
getLFLLTuple(const LFLLTuple<$useClassAll>& tuple)
{
    typedef detail::LFLLTupleElementTypes<I, I, $useClassAll>
        ElementTypes;

    return static_cast<const typename ElementTypes::type&>(tuple.m_impl).get();
}

// Create a new tuple with object reference
// LFLLTuple<T0, T1, ...> makeLFLLTuple(T0& v0, T1& v1, ...);

"""

LFLLTUPLE_END_STR_TEMPLATE = """\

LFLL_END_NAMESPACE

#endif // ${headerGuard}

"""

LFLLTUPLE_MAKETUPLE_STR_TEMPLATE = """\

/**
 * \\brief Create a new tuple with objects reference
 * \\return New tuple
 */
template <$defClass>
inline
LFLLTuple<$useClass>
makeLFLLTuple($argsRefWithType)
{
    return LFLLTuple<$useClass>($argsPtr);
}

"""

LFLLTUPLEDETAIL_STR_TEMPLATE = """\
/*
The MIT License (MIT)

Copyright (c) 2013 Nicolas Pauss

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#ifndef ${headerGuard}
#define ${headerGuard}

/**
 * This file is automatically generated by python/LFLLTupleGenerator.py
 * You shouldn't use this file directly but rather use ${lfllTupleDir}${lfllTupleName}.
 */


#include <cstring>

#include <lfll/engine/LFLLDefinitions.h>
#include <lfll/engine/LFLLStaticAssert.h>

LFLL_BEGIN_NAMESPACE

namespace detail {
class null_type {};

template<class T> struct isNonNullType { enum {value = true}; };
template<> struct isNonNullType<null_type> { enum {value = false}; };
}

template <$defClassAllWithDefaultDetail>
class LFLLTuple;


namespace detail {


// LFLLTupleValueTypes, retrieve type of the value of the nth element.

template <size_t I, $defClassAllWithDefault>
class LFLLTupleValueTypes
{
public:
    typedef typename LFLLTupleValueTypes<I-1, $useClassWithoutFirst, null_type>::type
        type;
};


template <$defClassAll>
class LFLLTupleValueTypes<0, $useClassAll>
{
    LFLL_STATIC_ASSERT((isNonNullType<T0>::value), non_accessible_element);
public:
    typedef T0 type;
};


// LFLLTupleElement

template <size_t I, $defClassAll>
class LFLLTupleElement : public LFLLTupleElement<I+1, $useClassWithoutFirst, null_type>
{
public:
    static const size_t tupleSize = 1 + LFLLTupleElement<I+1, $useClassWithoutFirst, null_type>::tupleSize;
public:
    LFLLTupleElement($argsPtrWithType)
        : LFLLTupleElement<I+1, $useClassWithoutFirst, null_type>(
              $argsPtrWithoutFirst, 0)
        , m_val(v0)
    {}

    T0* get()
    {
        return m_val;
    }

    const T0* get() const
    {
        return m_val;
    }

private:
    T0* m_val;
};

template <size_t I, $defClassWithoutFirst>
class LFLLTupleElement<I, null_type, $useClassWithoutFirst>
{
public:
    static const size_t tupleSize = 0;
public:
    LFLLTupleElement(null_type*, $argsTypeWithoutFirst)
    {}
};

// LFLLTupleElementTypes, retrieve type of the nth element.

template <size_t I, size_t EI, $defClassAllWithDefault>
class LFLLTupleElementTypes
{
public:
    typedef typename LFLLTupleElementTypes<I-1, EI, $useClassWithoutFirst, null_type>::type
        type;
};

template <size_t EI, $defClassAll>
class LFLLTupleElementTypes<0, EI, $useClassAll>
{
    LFLL_STATIC_ASSERT((isNonNullType<T0>::value), non_accessible_element);
public:
    typedef LFLLTupleElement<EI, $useClassAll> type;
};



// LFLLTupleImpl

template <$defClassAll>
class LFLLTupleImpl : public LFLLTupleElement<0, $useClassAll>
{
public:
    static const size_t tupleSize = LFLLTupleElement<0, $useClassAll>::tupleSize;

public:
    LFLLTupleImpl($argsPtrWithType)
        : LFLLTupleElement<0, $useClassAll> (
            $argsPtrAll)
    {}
};

}

LFLL_END_NAMESPACE

#endif // ${headerGuard}

"""

if sys.hexversion > 0x03000000:
    _range = range
    _input = input
    _makedirs = lambda p : os.makedirs(p, exist_ok=True)
else:
    _range = xrange
    _input = raw_input
    def _makedirs(path) :
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise



    
class StdoutOutputHandler:
    def __init__(self, filePaths):
        self._filePaths = filePaths
        pass
    def write(self, str):
        sys.stdout.write(str)
    def debug(self, str):
        sys.stderr.write(str)
        sys.stderr.write("\n")
    def startFile(self, fileVal):
        filePath = self._filePaths[fileVal]
        sys.stdout.write("--------- start of ")
        sys.stdout.write(filePath)
        sys.stdout.write("\n")
    def endFile(self, fileVal):
        filePath = self._filePaths[fileVal]
        sys.stdout.write("--------- end of ")
        sys.stdout.write(filePath)
        sys.stdout.write("\n\n")
        
class FileOutputHandler:
    def __init__(self, filePaths):
        self._filePaths = filePaths
        self._file = None
    def write(self, str):
        if self._file is None:
            return
        self._file.write(str)
    def debug(self, str):
        print(str)
    def startFile(self, fileVal):
        filePath = self._filePaths[fileVal]
        if self._file is not None:
            self._file.close()
        try:
            self._file = open(filePath, 'w')
        except IOError:
            self._file.close()
            print("File error")
            exit(-3)
    def endFile(self, fileVal):
        if self._file is not None:
            self._file.close()
            self._file = None

def create_template_args(args):
    return {
        'nbArgs': args.nbArgs,
        
        'defClassAllWithDefault': ", ".join(["class T{} = null_type".format(x) for x in _range(0, args.nbArgs)]),
        'defClassWithoutFirstWithDefault': ", ".join(["class T{} = null_type".format(x) for x in _range(1, args.nbArgs)]),
        
        'defClassAllWithDefaultDetail': ", ".join(["class T{} = detail::null_type".format(x) for x in _range(0, args.nbArgs)]),
        
        'defClassAll': ", ".join(["class T{}".format(x) for x in _range(0, args.nbArgs)]),
        'defClassWithoutFirst': ", ".join(["class T{}".format(x) for x in _range(1, args.nbArgs)]),
        
        'useClassAll': ", ".join(["T{}".format(x) for x in _range(0, args.nbArgs)]),
        'useClassWithoutFirst': ", ".join(["T{}".format(x) for x in _range(1, args.nbArgs)]),
        
        
        'defClassAlter': ", ".join(["class T_{}".format(x) for x in _range(0, args.nbArgs)]),
        'useClassAlter': ", ".join(["T_{}".format(x) for x in _range(0, args.nbArgs)]),
        
        
        'argsPtrWithTypeAndDefault': ", ".join(["T{0}* v{0} = 0".format(x) for x in _range(0, args.nbArgs)]),
        'argsPtrWithType': ", ".join(["T{0}* v{0}".format(x) for x in _range(0, args.nbArgs)]),
        'argsPtrAll': ", ".join(["v{}".format(x) for x in _range(0, args.nbArgs)]),
        'argsPtrWithoutFirst': ", ".join(["v{}".format(x) for x in _range(1, args.nbArgs)]),
        'argsTypeWithoutFirst': ", ".join(["T{}*".format(x) for x in _range(1, args.nbArgs)])
    }
        

def create_header_guard(fileName):
    return '_'.join(fileName.upper().split('.'))


LFLLTUPLE_FILE_VAL = 0;
LFLLTUPLEDETAIL_FILE_VAL = 1;
    
def create_output_handler(args):
    if args.stdout:
        tupleFileRelPath = os.path.join(LFLLTUPLE_DIR, LFLLTUPLE_NAME)
        tupleDetailFileRelPath = os.path.join(LFLLTUPLEDETAIL_DIR, LFLLTUPLEDETAIL_NAME)
        filePaths = {LFLLTUPLE_FILE_VAL: tupleFileRelPath, 
                    LFLLTUPLEDETAIL_FILE_VAL: tupleDetailFileRelPath}
        return StdoutOutputHandler(filePaths)

    tupleFileAbsDir = os.path.abspath(os.path.join(args.outputDir, LFLLTUPLE_DIR))
    tupleDetailFileAbsDir = os.path.abspath(os.path.join(args.outputDir, LFLLTUPLEDETAIL_DIR))

    tupleFileAbsPath = os.path.join(tupleFileAbsDir, LFLLTUPLE_NAME)
    tupleDetailFileAbsPath = os.path.join(tupleDetailFileAbsDir, LFLLTUPLEDETAIL_NAME)

    _makedirs(tupleFileAbsDir)
    _makedirs(tupleDetailFileAbsDir)
        
    # Test if file exists and if it's a file
    tupleFileExists = os.path.exists(tupleFileAbsPath)
    tupleFileIsFile = os.path.isfile(tupleFileAbsPath)
    tupleDetailFileExists = os.path.exists(tupleDetailFileAbsPath)
    tupleDetailFileIsFile = os.path.isfile(tupleDetailFileAbsPath)
    
    if (tupleFileExists or tupleDetailFileExists):
        if ((tupleFileExists and not tupleFileIsFile) or
            (tupleDetailFileExists and not tupleDetailFileIsFile)):
            print("Files are not writable at location")
            exit(-4)
        else:
            var = _input("Files are already present, do you want to overwrite them? [y/(n)] ")
            if not (var == "y" or var == "Y"):
                exit(0)


    filePaths = {LFLLTUPLE_FILE_VAL: tupleFileAbsPath, 
                LFLLTUPLEDETAIL_FILE_VAL: tupleDetailFileAbsPath}
        
    return FileOutputHandler(filePaths)      
        

def create_lfll_tupple(outputHandler, templateArgs):
    headerGuard = create_header_guard(LFLLTUPLE_NAME)

    outputHandler.debug("Start creating {0}".format(LFLLTUPLE_NAME))
    outputHandler.startFile(LFLLTUPLE_FILE_VAL)
    
    outputHandler.write(Template(LFLLTUPLE_MAIN_STR_TEMPLATE).substitute(
        templateArgs, headerGuard=headerGuard, 
        lfllTupleDetailDir=LFLLTUPLEDETAIL_DIR,
        lfllTupleDetailName=LFLLTUPLEDETAIL_NAME))
    
    for i in _range(1, templateArgs['nbArgs']+1):
        defClass = ", ".join(["class T{}".format(x) for x in _range(0, i)])
        useClass = ", ".join(["T{}".format(x) for x in _range(0, i)])
        argsRefWithType = ", ".join(["T{0}& v{0}".format(x) for x in _range(0, i)])
        argsPtr = ", ".join(["&v{}".format(x) for x in _range(0, i)])
        outputHandler.write(Template(LFLLTUPLE_MAKETUPLE_STR_TEMPLATE).substitute(
            defClass=defClass, 
            useClass=useClass,
            argsRefWithType=argsRefWithType,
            argsPtr=argsPtr))
        
    
    
    outputHandler.write(Template(LFLLTUPLE_END_STR_TEMPLATE).substitute(
        templateArgs, headerGuard=headerGuard, 
        lfllTupleDetailDir=LFLLTUPLEDETAIL_DIR,
        lfllTupleDetailName=LFLLTUPLEDETAIL_NAME))
    
    
    outputHandler.endFile(LFLLTUPLE_FILE_VAL)
    
    
def create_lfll_tupple_detail(outputHandler, templateArgs):
    headerGuard = create_header_guard(LFLLTUPLEDETAIL_NAME)

    outputHandler.debug("Start creating {0}".format(LFLLTUPLEDETAIL_NAME))
    outputHandler.startFile(LFLLTUPLEDETAIL_FILE_VAL)
    
    outputHandler.write(Template(LFLLTUPLEDETAIL_STR_TEMPLATE).substitute(
        templateArgs, headerGuard=headerGuard, 
        lfllTupleDir=LFLLTUPLE_DIR,
        lfllTupleName=LFLLTUPLE_NAME))
    
    outputHandler.endFile(LFLLTUPLEDETAIL_FILE_VAL)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create ' + LFLLTUPLE_NAME \
        + ' and ' + LFLLTUPLEDETAIL_NAME)
    parser.add_argument('-n', dest='nbArgs',
                   default=50,
                   type=int,
                   help='max number of template arguments (default is 50)')

    parser.add_argument('-', dest='stdout', action='store_true',
                   help='print output in stdout instead of files (debug messages will be sent to stderr)')

    parser.add_argument('-d', dest='outputDir', default=LFLL_DEFAULT_EXPORT_DIR,
                   help=('output directory (default is "' + LFLL_DEFAULT_EXPORT_DIR + '")'))

    args = parser.parse_args()
    if args.nbArgs < 1:
        print('Error: number of template arguments must be superior or equal to 1')
        exit(-1)
    
    
    outputHandler = create_output_handler(args)
    templateArgs = create_template_args(args)
    
    create_lfll_tupple(outputHandler, templateArgs)
    create_lfll_tupple_detail(outputHandler, templateArgs)
    
    outputHandler.debug("\nFiles are placed as follow:")
    outputHandler.debug("{0} ->  {1}{0}".format(LFLLTUPLE_NAME, LFLLTUPLE_DIR))
    outputHandler.debug("{0} ->  {1}{0}".format(LFLLTUPLEDETAIL_NAME, LFLLTUPLEDETAIL_DIR))
    
    
    