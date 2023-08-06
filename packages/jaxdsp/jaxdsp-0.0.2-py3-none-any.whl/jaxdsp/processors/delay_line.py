# Fractional delay line using linear interpolation

# The `delay_samples` param cannot be optimized outside of the +/- 1 sample range between
# init and target.
# This is because the param maps directly to an `index_update` operation,
# which requires converting the parameter to an integer, which is a non-differentiable operation.
# Linear interpolation helps by allowing successful optimization within the +/- 1 sample
# range, but I have not found a solution that allows the gradient signal to propagate
# across the entire indexing range.
# (See "Differentiable array indexing" notebook for more details.)


import jax.numpy as jnp
import numpy as np
from jax import jit, lax
from jax.ops import index, index_update

NAME = 'Delay Line'

MAX_DELAY_LENGTH_SAMPLES = 44_100

def init_params(wet_amount=1.0, delay_samples=9.2):
    return {
        'wet_amount': wet_amount,
        'delay_samples': delay_samples,
    }

def init_state():
    return {
        'delay_line': jnp.zeros(MAX_DELAY_LENGTH_SAMPLES),
        'read_sample': 0.0,
        'write_sample': 0.0,
    }

def default_target_params():
    return init_params(0.5, 10.0)

@jit
def tick(carry, x):
    params = carry['params']
    state = carry['state']

    write_sample = state['write_sample']
    read_sample = state['read_sample']

    state['delay_line'] = index_update(state['delay_line'], index[write_sample].astype('int32'), x)

    read_sample_floor = read_sample.astype('int32')
    interp = read_sample - read_sample_floor
    y = (1 - interp) * state['delay_line'][read_sample_floor]
    y += (interp) * state['delay_line'][(read_sample_floor + 1) % MAX_DELAY_LENGTH_SAMPLES]

    state['write_sample'] += 1
    state['write_sample'] %= MAX_DELAY_LENGTH_SAMPLES
    state['read_sample'] += 1
    state['read_sample'] %= MAX_DELAY_LENGTH_SAMPLES

    out = x * (1 - params['wet_amount']) + y * params['wet_amount']
    return carry, out

@jit
def tick_buffer(carry, X):
    state = carry['state']
    params = carry['params']
    state['read_sample'] = (state['write_sample'] - jnp.clip(params['delay_samples'], 0, MAX_DELAY_LENGTH_SAMPLES)) % MAX_DELAY_LENGTH_SAMPLES
    return lax.scan(tick, carry, X)
