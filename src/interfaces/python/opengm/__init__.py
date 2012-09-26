#from opengmcore import _opengmcore.adder as adder
import opengmcore._opengmcore.adder as adder2
from opengmcore import *
#from opengmcore import *
#import version 
from __version__ import version

import inference
import hdf5
import sys
import types

configuration=OpengmConfiguration()


def graphicalModel(numberOfLabels,operator='adder'):
   """Factory function to construct a graphical model.

   Keyword arguments:
   
   numberOfLabels -- number of label sequence (can be a list or  a 1d numpy.ndarray)
   
   operator -- operator of the graphical model. Can be 'adder' or 'multiplier' (default 'adder')
   
   Construct a gm with ``\'adder\'`` as operator::
   
      gm=opengm.graphicalModel([2,2,2,2,2],operator='adder')
      # or just
      gm=opengm.graphicalModel([2,2,2,2,2])
      # or just
      
   Construct a gm with ``\'multiplier\'`` as operator::  
   
      gm=opengm.graphicalModel([2,2,2,2,2],operator='multiplier')
      
   """
   if operator=='adder' :
      return adder.GraphicalModel(numberOfLabels)
   elif operator=='multiplier' :
      return multiplier.GraphicalModel(numberOfLabels)
   else:
      raise NameError('operator must be \'adder\' or \'multiplier\'') 



def inferenceParameter(gm ,alg, accumulator=None):
   alg=alg.lower()
   #evaluate accumulator
   operator=gm.operator
   if accumulator is None :
      if operator=='adder' :
         accumulator='minimizer'
      elif operator=='multiplier':
         accumulator='maximizer'
      else :
         print operator
         raise NameError('operator must be \'adder\' or \'multiplier\'') 
   else:
      accumulator=accumulator.lower()
      if accumulator is 'min' or 'minimizer':
         accumulator='minimizer'
      elif accumulator is 'max' or 'maximizer':
         accumulator='maximizer'
      else :
         print operator
         raise NameError('operator must be \'minimizer\' or \'maximizer\' (or just \'min\' or \'max\' )')   
   #evaluate inference algorithm      
   name = 'inference.'+operator+'.'+accumulator
   #dirty hack!
   if alg=='bp' or alg=='beliefpropagation':
      return eval(name).BpParameter()
   elif alg=='trbp' or alg=='tr-beliefpropagation':
      return eval(name).TrBpParameter()
   elif alg=='icm':
      return eval(name).IcmParameter()
   elif alg=='gibbs':
      return eval(name).GibbsParameter()
   elif alg=='astar' or alg=='a-star':
      return eval(name).AStarParameter()
   elif alg=='loc':
      return eval(name).LOCParameter()
   elif alg=='lf' or alg=="lazyflipper" or alg=="lazy-flipper":
      return eval(name).LazyFlipperParameter()
   elif alg=='gc' or alg=='graphcut' or alg=='graph-cut':
      return eval(name).GraphCutBoostKolmogorovParameter()
   elif alg=='abs' or alg=='ab-swap' or alg=="alphabetaswap" or alg=="alpha-beta-swap" or alg=="alphabeta-swap":
      return eval(name).AlphaBetaSwapBoostKolmogorovParameter()
   elif alg=='ae' or alg=='a-expansion' or alg=="alphaexpansion" or alg=="alpha-expansion" :
      return eval(name).AlphaExpansionBoostKolmogorovParameter()
   elif configuration.withLibdai :
      if alg=='libdai-bp':
         return eval(name).LibDaiBpParameter()
      elif alg=='libdai-trbp' :
         return eval(name).LibDaiTrBpParameter()
      elif alg=='libdai-fbp' or alg=='libdai-fractional-bp':
         return eval(name).LibDaiFractionalBpParameter()
      elif alg=='libdai-jt' or alg=='libdai-junction-tree':
         return eval(name).LibDaiJunctionTreeParameter()
      elif alg=='libdai-dlgbp' or alg=='libdai-double-loop-generalized-bp':
         return eval(name).LibDaiDoubleLoopGbpParameter()
   else:
      raise NameError( 'alg \'' + alg + '\' is unknown') 

        
        
def inferenceAlgorithm(gm ,alg, accumulator=None,parameter=None):
   alg=alg.lower()
   #evaluate accumulator
   operator=gm.operator
   if accumulator is None :
      if operator=='adder' :
         accumulator='minimizer'
      elif operator=='multiplier':
         accumulator='maximizer'
      else :
         print operator
         raise NameError('operator must be \'adder\' or \'multiplier\'') 
   else:
      accumulator=accumulator.lower()
      if accumulator is 'min' or 'minimizer':
         accumulator='minimizer'
      elif accumulator is 'max' or 'maximizer':
         accumulator='maximizer'
      else :
         print operator
         raise NameError('operator must be \'minimizer\' or \'maximizer\' (or just \'min\' or \'max\' )')   
   #evaluate inference algorithm      
   name = 'inference.'+operator+'.'+accumulator
   #dirty hack!
   if alg=='bp' or alg=='beliefpropagation':
      if parameter is None: return eval(name).Bp(gm)
      else: return eval(name).Bp(gm,parameter)
   if alg=='trwbp' or alg=='trbp':
      if parameter is None: return eval(name).TrBp(gm)
      else: return eval(name).TrBp(gm,parameter)
   elif alg=='icm':
      if parameter is None:return eval(name).Icm(gm)
      else: return eval(name).Icm(gm,parameter)
   elif alg=='gibbs':
      if parameter is None:return eval(name).Gibbs(gm)
      else: return eval(name).Gibbs(gm,parameter)     
   elif alg=='astar' or alg=='a-star':
      if parameter is None:return eval(name).AStar(gm)
      else: return eval(name).AStar(gm,parameter) 
   elif alg=='loc':
      if parameter is None:return eval(name).LOC(gm)
      else: return eval(name).LOC(gm,parameter) 
   elif alg=='lf' or alg=="lazyflipper" or alg=="lazy-flipper":
      if parameter is None:return eval(name).LazyFlipper(gm)
      else: return eval(name).LazyFlipper(gm,parameter) 
   elif alg=='gc' or alg=='graphcut' or alg=='graph-cut':
      if parameter is None:return eval(name).GraphCutBoostKolmogorov(gm)
      else: return eval(name).GraphCutBoostKolmogorov(gm,parameter) 
   elif alg=='abs' or alg=='ab-swap' or alg=="alphabetaswap" or alg=="alpha-beta-swap" or alg=="alphabeta-swap":
      if parameter is None:return eval(name).AlphaBetaSwapBoostKolmogorov(gm)
      else: return eval(name).AlphaBetaSwapBoostKolmogorov(gm,parameter) 
   elif alg=='ae' or alg=='a-expansion' or alg=="alphaexpansion" or alg=="alpha-expansion" :
      if parameter is None:return eval(name).AlphaExpansionBoostKolmogorov(gm)
      else: return eval(name).AlphaExpansionBoostKolmogorov(gm,parameter) 
   elif configuration.withLibdai :
      if alg=='libdai-bp' or alg=='libdai-beliefpropagation':
         if parameter is None:return eval(name).LibDaiBp(gm)
         else: return eval(name).LibDaiBp(gm,parameter) 
      elif alg=='libdai-trbp' :
         if parameter is None:return eval(name).LibDaiTrBp(gm)
         else: return eval(name).LibDaiTrBp(gm,parameter) 
      elif alg=='libdai-fbp' or alg=='libdai-fractional-bp':
         if parameter is None:return eval(name).LibDaiFractionalBp(gm)
         else: return eval(name).LibDaiFractionalBp(gm,parameter) 
      elif alg=='libdai-jt' or alg=='libdai-junction-tree':
         if parameter is None:return eval(name).LibDaiJunctionTree(gm)
         else: return eval(name).LibDaiJunctionTree(gm,parameter) 
      elif alg=='libdai-dlgbp' or alg=='libdai-double-loop-generalized-bp':
         if parameter is None:return eval(name).LibDaiDoubleLoopGbp(gm)
         else: return eval(name).LibDaiDoubleLoopGbp(gm,parameter) 
   else:
      raise NameError( 'alg \'' + alg + '\' is unknown') 

      


