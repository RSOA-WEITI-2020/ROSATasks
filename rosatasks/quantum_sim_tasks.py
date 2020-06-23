
import numpy as np
import qiskit
from qiskit import (
    QuantumCircuit,
    execute,
    Aer,
)
from celery import shared_task


@shared_task
def simulate_code(id, code, shots):
    try:
        sim = Aer.get_backend('qasm_simulator')
        c = QuantumCircuit.from_qasm_str(code)
        job = execute(c, sim, shots=shots)
        res = job.result()
        counts = res.get_counts(c)
        res = {
            key: (count/SHOTS)*100
            for key, count in counts.items()
        }
        schema = str(c.draw())
        return (id, None, res, schema)

    except Exception as e:
        err = str(e).replace('\\n', '\n').replace('\"', '\n').replace('\'', '')
        return (id, err, None, None)
