
import numpy as np
import qiskit
import time
from qiskit import (
    QuantumCircuit,
    execute,
    Aer,
)
from celery import (shared_task, current_task)


@shared_task
def simulate_code(id, code, shots):
    second_counter = 0
    try:
        sim = Aer.get_backend('qasm_simulator')
        c = QuantumCircuit.from_qasm_str(code)
        job = execute(c, sim, shots=shots)
        while not job.in_final_state():
            time.sleep(1)
            second_counter += 1
            current_task.update_state(state='PROGRESS', meta={
                                      'seconds': second_counter})
        res = job.result()
        counts = res.get_counts(c)
        res = {
            key: (count/shots)*100
            for key, count in counts.items()
        }
        schema = str(c.draw())
        return (id, None, res, schema)

    except Exception as e:
        err = str(e).replace('\\n', '\n').replace('\"', '\n').replace('\'', '')
        return (id, err, None, None)
