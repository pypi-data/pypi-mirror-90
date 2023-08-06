from jax import grad
import jax.numpy as jnp


class HelloWorld:
    def get_solution(self):
        return grad(jnp.tanh)(0.9999599) * 100.0
