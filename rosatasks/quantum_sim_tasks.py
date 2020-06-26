
import numpy as np
import qiskit
import time
from qiskit import (
    QuantumCircuit,
    execute,
    Aer,
)
from qiskit.providers import JobStatus
from celery import (shared_task, current_task)


@shared_task
def simulate_code(id, code, shots):
    second_counter = 0
    elapsed_time = 0
    try:
        sim = Aer.get_backend('qasm_simulator')
        c = QuantumCircuit.from_qasm_str(code)

        job = execute(c, sim, shots=shots)

        start_time = time.time()
        while not job.in_final_state():
            elapsed_time = time.time() - start_time
            current_task.update_state(state='PROGRESS', meta={
                                      'seconds': second_counter, 'time': elapsed_time})
            time.sleep(1)

        elapsed_time = time.time() - start_time
        res = job.result()

        counts = res.get_counts(c)
        res = {
            key: (count/shots)*100
            for key, count in counts.items()
        }
        schema = str(c.draw())
        return (id, None, res, schema, elapsed_time, second_counter)

    except Exception as e:
        err = str(e).replace('\\n', '\n').replace('\"', '\n').replace('\'', '')
        return (id, err, None, None, elapsed_time, second_counter)
