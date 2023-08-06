from optimaldesign import HelloWorld
import jax.numpy as jnp


class TestHelloWorld:
    def test_get_solution(self):
        helloworld = HelloWorld()
        assert jnp.abs(helloworld.get_solution() - 42) <= 1e-8
