import numpy as np

from qiskit import QuantumCircuit
# from qiskit.quantum_info import Operator

# from scipy.sparse import csc_array as spcsc
# from scipy.sparse import kron as spkrn
# from scipy.sparse.linalg import expm
from qiskit.circuit.library import GlobalPhaseGate
# from tqdm import tqdm

import CNOT_connection as CNOT_conc



def qubit_ckt_diag(theta, qno):
    qc = QuantumCircuit(qno)
    qc.rx(theta, 0)
    return qc


def qubit_ckt_diag_for_I_only(theta, qno):
    qc = QuantumCircuit(qno)
    qc.append(GlobalPhaseGate(theta))
    return qc


def XX_Block_diag(input_str, q_no, my_str):

    qc = QuantumCircuit(q_no)
    if input_str[:-1] == 'I' * (len(input_str) - 1) and input_str[-1] == my_str:
        return qc

    b_val = CNOT_conc.op_cnot(input_str, q_no)[0]
    cnot_arr = CNOT_conc.output_cnot(input_str, q_no)
    
    
    if b_val % 2 == 0: 
        qc.cx(max(cnot_arr), 0)
        
        for posn in cnot_arr:
            qc.cx(0, posn)
        
        qc.cx(max(cnot_arr), 0)
        
    else:
        for posn in cnot_arr:
            qc.cx(0, posn)
    
    return qc

def start_cir(q_no,input_str):

    qc = QuantumCircuit(q_no)

    for ind in range(len(input_str)):

        if input_str[ind] == 'Z':
            qc.h(q_no-ind-1)

        if input_str[ind] == 'Y':
            qc.rz(np.pi/4,q_no-ind-1)
    
    return qc

def end_cir(q_no,input_str):

    qc = QuantumCircuit(q_no)

    for ind in range(len(input_str)):

        if input_str[ind] == 'Z':
            qc.h(q_no-ind-1)

        if input_str[ind] == 'Y':
            qc.rz(-np.pi/4,q_no-ind-1)
    
    return qc


def ckt_diag(input_str, q_no, argm, time_step):


    my_first = start_cir(q_no,input_str)
    my_end = end_cir(q_no,input_str)

    if 'X' in input_str:
        my_ckt = XX_Block_diag(input_str,q_no,'X').compose(qubit_ckt_diag(-2*argm*time_step, q_no)).compose(XX_Block_diag(input_str,q_no,'X'))
        return my_ckt

    elif 'Z' in input_str:
        my_ckt = XX_Block_diag(input_str,q_no,'Z').compose(qubit_ckt_diag(-2*argm*time_step, q_no)).compose(XX_Block_diag(input_str,q_no,'Z'))
    
    elif 'Y' in input_str:
        my_ckt = XX_Block_diag(input_str,q_no,'Y').compose(qubit_ckt_diag(-2*argm*time_step, q_no)).compose(XX_Block_diag(input_str,q_no,'Y'))
        
    else:
        my_ckt = qubit_ckt_diag_for_I_only(-argm*time_step, q_no)

    poli = my_first.compose(my_ckt)
    ffffol = poli.compose(my_end)

    return ffffol

my_circ = ckt_diag('III',3,1.0,1.0)
my_circ.draw("mpl")