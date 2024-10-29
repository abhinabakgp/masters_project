import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

num_sites = 3
U = 1.0
t_hop = 1.0
dtau = 0.01
num_iterations = 10000
total_sites = 2 * num_sites
basis_states = [state for state in range(2**total_sites)]

def hamiltonian_matrix(basis_states, num_sites, U, t_hop):
    dim = len(basis_states)
    H = sp.lil_matrix((dim, dim))

    for i, state in enumerate(basis_states):
        for site in range(num_sites):
            spin_up = (state >> site) & 1
            print(spin_up)
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

print(H.toarray())

# psi = np.random.rand(len(basis_states))
psi = np.zeros(len(basis_states))
psi[40] = 1
psi /= np.linalg.norm(psi)

print(psi)

for step in range(num_iterations):
    psi = spla.expm_multiply(-dtau*H, psi)
    psi /= np.linalg.norm(psi)

energy = psi.conj().T @ H @ psi

print("Ground state wavefunction:", psi.round(3))
print("Ground state energy:", energy)

