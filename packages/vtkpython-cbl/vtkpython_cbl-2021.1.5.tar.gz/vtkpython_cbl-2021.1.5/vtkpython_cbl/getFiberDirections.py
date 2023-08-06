#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2019                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
########################################################################

from builtins import range

import math
import random
import numpy

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

import vtkpython_cbl as cbl

########################################################################

def getFiberDirections(
        farray_eRR,
        farray_eCC,
        farray_eLL,
        farray_angle_helix,
        angles_in_degrees=True,
        use_new_definition=False,
        shuffle_vectors=False,
        verbose=1):

    mypy.my_print(verbose, "*** getFiberDirections ***")

    n_tuples = farray_angle_helix.GetNumberOfTuples()

    farray_eF = myvtk.createFloatArray("eF", 3, n_tuples)
    farray_eS = myvtk.createFloatArray("eS", 3, n_tuples)
    farray_eN = myvtk.createFloatArray("eN", 3, n_tuples)

    eRR = numpy.empty(3)
    eCC = numpy.empty(3)
    eLL = numpy.empty(3)
    for k_tuple in range(n_tuples):
        farray_eRR.GetTuple(k_tuple, eRR)
        farray_eCC.GetTuple(k_tuple, eCC)
        farray_eLL.GetTuple(k_tuple, eLL)

        assert (round(numpy.linalg.norm(eRR),1) == 1.0),\
            "|eRR| = "+str(numpy.linalg.norm(eRR))+"≠ 1. Aborting"
        assert (round(numpy.linalg.norm(eCC),1) == 1.0),\
            "|eCC| = "+str(numpy.linalg.norm(eCC))+"≠ 1. Aborting"
        assert (round(numpy.linalg.norm(eLL),1) == 1.0),\
            "|eLL| = "+str(numpy.linalg.norm(eLL))+"≠ 1. Aborting"

        angle_helix = farray_angle_helix.GetTuple1(k_tuple)
        if (angles_in_degrees): angle_helix = angle_helix*math.pi/180
        eF = math.cos(angle_helix) * eCC + math.sin(angle_helix) * eLL
        #print("eF = "+str(eF))
        if (shuffle_vectors):
            eF *= random.choice([-1,+1])
            #print("eF = "+str(eF))
        if (use_new_definition):
            eN = eRR
            if (shuffle_vectors):
                eN *= random.choice([-1,+1])
                assert (abs(numpy.dot(eN,eRR)) > 0.999)
            eS = numpy.cross(eN, eF)
        else:
            eS = eRR
            if (shuffle_vectors): eS *= random.choice([-1,+1])
            eN = numpy.cross(eF, eS)

        assert (round(numpy.linalg.norm(eF),1) == 1.0),\
            "|eF| = "+str(numpy.linalg.norm(eF))+"≠ 1. Aborting"
        assert (round(numpy.linalg.norm(eS),1) == 1.0),\
            "|eS| = "+str(numpy.linalg.norm(eS))+"≠ 1. Aborting"
        assert (round(numpy.linalg.norm(eN),1) == 1.0),\
            "|eN| = "+str(numpy.linalg.norm(eN))+"≠ 1. Aborting"

        farray_eF.SetTuple(k_tuple, eF)
        farray_eS.SetTuple(k_tuple, eS)
        farray_eN.SetTuple(k_tuple, eN)

    return (farray_eF,
            farray_eS,
            farray_eN)

########################################################################

def addFiberDirections(
        ugrid,
        type_of_support="cell",
        ref_basis="PPS",
        angles_in_degrees=True,
        use_new_definition=False,
        shuffle_vectors=False,
        verbose=1):

    mypy.my_print(verbose, "*** addFiberDirections ***")

    if (type_of_support == "cell"):
        ugrid_data = ugrid.GetCellData()
    elif (type_of_support == "point"):
        ugrid_data = ugrid.GetPointData()

    if (ref_basis == "PPS"):
        farray_eRR = ugrid_data.GetArray("eRR")
        farray_eCC = ugrid_data.GetArray("eCC")
        farray_eLL = ugrid_data.GetArray("eLL")
    elif (ref_basis == "CYL"):
        farray_eRR = ugrid_data.GetArray("eR")
        farray_eCC = ugrid_data.GetArray("eC")
        farray_eLL = ugrid_data.GetArray("eL")

    farray_angle_helix = ugrid_data.GetArray("angle_helix")

    (farray_eF,
     farray_eS,
     farray_eN) = getFiberDirections(
        farray_eRR=farray_eRR,
        farray_eCC=farray_eCC,
        farray_eLL=farray_eLL,
        farray_angle_helix=farray_angle_helix,
        angles_in_degrees=angles_in_degrees,
        use_new_definition=use_new_definition,
        shuffle_vectors=shuffle_vectors,
        verbose=verbose-1)

    ugrid_data.AddArray(farray_eF)
    ugrid_data.AddArray(farray_eS)
    ugrid_data.AddArray(farray_eN)

    return (farray_eF,
            farray_eS,
            farray_eN)
