import brainpy as bp
import brainpy.numpy as np

def get_WilsonCowan(w_ee = ..., w_ei = ..., w_ie = ..., w_ii = ..., r_e = , r_i = ):

    ST = bp.types.NeuState(
        {...}
    )

    @bp.integrate
    def int_a_e(a_e, _t_, ...):

    
    @bp.integrate
    def int_a_i(a_i, _t_, ...):

    
    def update(ST, _t_, ...):



    return bp.NeuType(name='MilsonCowan_neuron',
                      requires=ST,
                      steps=update,
                      vector_based=False)