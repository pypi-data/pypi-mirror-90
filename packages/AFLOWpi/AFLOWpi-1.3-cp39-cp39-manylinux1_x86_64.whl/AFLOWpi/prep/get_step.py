# ***************************************************************************
# *                                                                         *
# *          AFLOWpi - Central Michigan University University, 2017         *
# *                                                                         *
# ***************************************************************************
#
#  Copyright 2017 - Andrew Supka and Marco Fornari - AFLOW.ORG consortium
#
#  This file is part of AFLOWpi software.
#
#  AFLOWpi is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ***************************************************************************

import AFLOWpi

def _get_step(oneCalc,ID,step_type=None,last=True):

    if step_type is None:
        return 0
    try:
        workflow = oneCalc['_AFLOWPI_WORKFLOW_']

    except:
        return 0


    try:

        chain_index=oneCalc['__chain_index__']


        occ_list=[]
        current_step_type=workflow[chain_index-1]
        for i in reversed(list(range(0,chain_index))):

            if workflow[i]==step_type:


                occ_list.append(i+1)
                    
        if len(occ_list)!=0:
            return occ_list
        else:
            return 0


    except Exception as e:
        print(e)
        AFLOWpi.run._fancy_error_log(e)
        return 0
        


import numpy

def _return_ID(oneCalc,ID,step_type=None,last=True,straight=False):
    index =AFLOWpi.prep._get_step(oneCalc,ID,step_type=step_type,last=last)
    
    prefix = oneCalc['_AFLOWPI_PREFIX_'][1:]

    prefix_first = prefix.split('_')[0]



    if type(index)==type([1,2,3]):



        index = numpy.asarray(index)

        splits=numpy.split(index, numpy.where(numpy.diff(index) != -1)[0]+1)
        if last==True:
            chain_ind_list=splits[0].tolist()
            if straight==True:
                step_ID = ['%s_%02d'%(prefix_first,i) for i in chain_ind_list]
#                print step_type,step_ID
                return step_ID
            else:
                step_ID = ['%s_%02d'%(prefix_first,i) for i in chain_ind_list][0]
#                print step_type,step_ID
                return step_ID
        else:
            if straight==True:
                step_ID = ['%s_%02d'%(prefix_first,i) for i in index]
#                print step_type,step_ID
                return step_ID
            else:
                step_ID = ['%s_%02d'%(prefix_first,i) for i in index[0]]
#                print step_type,step_ID
                return step_ID

