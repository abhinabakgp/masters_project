import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
import scipy.linalg as la

num_sites = 3
U = 1.0
t_hop = 1.0
dt = 0.01
num_iterations = 6000
total_sites = 2 * num_sites
basis_states = [state for state in range(2**total_sites)]

def hamiltonian_matrix(basis_states, num_sites, U, t_hop):
    dim = len(basis_states)
    H = sp.lil_matrix((dim, dim))
    
    for i, state in enumerate(basis_states):
        for site in range(num_sites):
            spin_up = (state >> site) & 1
            spin_down = (state >> (site + num_sites)) & 1
            if spin_up and spin_down:
                H[i, i] += U

    for i, state in enumerate(basis_states):
        for site in range(num_sites - 1):
            if ((state >> site) & 1) != ((state >> (site + 1)) & 1):
                flipped_state = state ^ (1 << site) ^ (1 << (site + 1))
                j = basis_states.index(flipped_state)
                H[i, j] -= t_hop

        for site in range(num_sites, 2 * num_sites - 1):
            if ((state >> site) & 1) != ((state >> (site + 1)) & 1):
                flipped_state = state ^ (1 << site) ^ (1 << (site + 1))
                j = basis_states.index(flipped_state)
                H[i, j] -= t_hop

    return H.tocsr()

H = hamiltonian_matrix(basis_states, num_sites, U, t_hop)

Hamilton_new = H.toarray()


psi = np.zeros(len(basis_states))
psi[60] = 1

psi /= np.linalg.norm(psi)

print(psi)

xs,ys = [],[]

for step in range(num_iterations):
    psi = spla.expm_multiply(-dt*H, psi)
    psi /= np.linalg.norm(psi)

    energy = psi.conj().T @ H @ psi
    if step>3000:
        xs.append(step)
        ys.append(energy)

print("Ground state wavefunction:", psi.round(3))
print("Ground state energy:", energy)

plt.plot(xs,ys)
