from qiskit import QuantumCircuit, IBMQ, execute
from qiskit_aer import AerSimulator
from qiskit.providers.ibmq.api.exceptions import RequestsApiError
from qiskit.providers.ibmq.exceptions import IBMQAccountCredentialsInvalidToken
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math
from pprint import pprint

class DickeState:
    def __init__(self, n, k, token=None, backend="ibmq_qasm_simulator") -> None:
        self.__is_on_ibmq = self.__check_run_on_ibmq(token)

        if self.__is_on_ibmq:
            self.__provider = IBMQ.get_provider(group="open")
            self.__qcomp = self.__provider.get_backend(backend)
            self.__sim = self.__qcomp
        else:
            self.__sim = AerSimulator()

        self.__check_valid_nk(n, k)
        self.__n = n
        self.__k = k
        self.__qc = QuantumCircuit(self.__n, self.__n)
        self.__initial_state()
        self.__qc.append(self.__Unk(), range(n))
        self.__counts = None

    def __initial_state(self):
        for i in range(self.__n-1, self.__n-self.__k-1, -1):
            self.__qc.x(i)

    def __CU(self, theta_arg, phi_arg, lambda_arg):
        U = QuantumCircuit(1)
        U.u(theta_arg, phi_arg, lambda_arg, 0)
        U = U.to_gate()
        U.name = f'CU({theta_arg},{phi_arg},{lambda_arg})'
        C_U = U.control()
        return C_U

    def __CCU(self, theta_arg, phi_arg, lambda_arg):
        U = QuantumCircuit(3)
        U.append(self.__CU(theta_arg/2,  phi_arg, lambda_arg), [1,2])
        U.cx(0,1)
        U.append(self.__CU(-theta_arg/2,  phi_arg, lambda_arg), [1,2])
        U.cx(0,1)
        U.append(self.__CU(theta_arg/2,  phi_arg, lambda_arg), [0,2])
        
        U = U.to_gate()
        U.name = f'CCU({theta_arg},{phi_arg},{lambda_arg})'
        # print(U)
        return U

    def __SCS(self, n, k):
        U = QuantumCircuit(n)
        U.cx(n-2, n-1)
        U.append(self.__CU(2*math.acos(math.sqrt(1/n)), 0, 0), [n-1,n-2])
        U.cx(n-2, n-1)

        for i in range(2, k+1):
            U.cx(n-1-i, n-1)
            U.append(self.__CCU(2*math.acos(math.sqrt(i/n)), 0, 0), [n-1,n-i,n-1-i])
            U.cx(n-1-i, n-1)

        U = U.to_gate()
        U.name = f'SCS({n},{k})'
        
        # print(U)
        return U

    def __Unk(self):
        n, k = self.__n, self.__k
        U = QuantumCircuit(self.__n)

        while n > k:
            U.append(self.__SCS(n,k), range(n))
            n -= 1
        
        while k > 1:
            U.append(self.__SCS(k,k-1), range(k))
            k -= 1
        
        U.to_gate()
        U.name = f'U({self.__n},{self.__k})'

        return U
    
    def get_qc(self):
        print(self.__qc)
        return self.__qc

    def measure(self):
        self.__qc.measure(range(self.__n), range(self.__n))
        print(self.__qc)

    def count(self, shots=1000):
        job = execute(self.__qc, backend=self.__sim, shots=shots)
        result = job.result()
        self.__counts = result.get_counts(self.__qc)
        pprint(self.__counts)

    def draw_bar(self):
        counts = self.__counts
        for key in counts:
            counts[key] = counts[key] / 1000
        plot_histogram(self.__counts)
        plt.show()
    def __check_run_on_ibmq(self, token):
        try:
            IBMQ.save_account(token, overwrite=True)
            IBMQ.load_account()
            print("Running on IBMQ.")
            return True
        except RequestsApiError:
            print("Running on local.")
            return False
        except IBMQAccountCredentialsInvalidToken:
            print("Running on local.")
            return False

    def __check_valid_nk(self, n, k):
        if n < k:
            raise ValueError("The total number of bits N must be greater than the number of 1 bit K.")
        

