import unittest

from rwth_nb.misc.signals import *
from rwth_nb.misc.transforms import *


# Axes
t = np.linspace(-5, 5, 10001)  # continuous time
n = np.linspace(-5, 5, 11)  # discrete time
f = np.linspace(-5, 5, 10001)  # frequency


def mse(x0, x1):
    return np.sum(np.abs(x0 - x1) ** 2)


class TestLaplaceTransform(unittest.TestCase):
    # TODO - Add more test cases
    def single_pole_order_n(self, H0=1, alpha=2, n=3):
        # single pole at -alpha with order n
        # Direct implementation in time domain
        s_c = H0 * unitstep(t) * np.exp(-alpha * t) * t ** (n - 1) / np.math.factorial(n - 1)
        s_ac = H0 * -unitstep(-t - 0.0001) * np.exp(-alpha * t) * t ** (n - 1) / np.math.factorial(n - 1)

        # Inverse transform from Laplace to time domain
        poles = np.array([-alpha])
        zeros = np.array([])
        ord_p = np.array([n])
        ord_z = np.array([])

        # Causal
        roc = np.array([-alpha, np.inf])  # region of convergence
        s_c_est, td_c, sd_c = ilaplace_ht(t, H0, poles, zeros, ord_p, ord_z, roc)

        # Anticausal
        roc = np.array([-np.inf, -alpha])  # region of convergence
        s_ac_est, td_ac, sd_ac = ilaplace_ht(t, H0, poles, zeros, ord_p, ord_z, roc)

        return s_c, s_ac, s_c_est, s_ac_est

    def cos_sin(self, omega0, cossin=0):
        if cossin == 0:  # return cosine
            s_c = np.cos(omega0 * t) * unitstep(t)
            s_ac = -np.cos(omega0 * t) * unitstep(-t - 0.0001)
        else:  # return sine
            s_c = np.sin(omega0 * t) * unitstep(t)
            s_ac = -np.sin(omega0 * t) * unitstep(-t - 0.0001)

        # Inverse transform from Laplace to time domain
        poles = np.array([1j * omega0]);
        ord_p = np.array([1]);

        if cossin == 0:
            H0 = 1
            zeros = np.array([0])  # Poles and Zeros
            ord_z = np.array([1])  # Poles' and Zeros' orders
        else:
            H0 = omega0
            zeros = np.array([])  # Poles and Zeros
            ord_z = np.array([])  # Poles' and Zeros' orders

        # Causal
        roc = np.array([0, np.inf])  # region of convergence
        s_c_est, td_c, sd_c = ilaplace_ht(t, H0, poles, zeros, ord_p, ord_z, roc)

        # Anticausal
        roc = np.array([-np.inf, 0])  # region of convergence
        s_ac_est, td_ac, sd_ac = ilaplace_ht(t, H0, poles, zeros, ord_p, ord_z, roc)

        return s_c, s_ac, s_c_est, s_ac_est

    def test_single_pole_order(self):
        for alpha in [-2, -0.5, 0, 0.5, 2]:
            for n in range(1, 5):
                with self.subTest(alpha=alpha, n=n):
                    (s_causal, s_anticausal, s_causal_est, s_anticausal_est) = self.single_pole_order_n(alpha, 1, n)
                    self.assertAlmostEqual(mse(s_causal, s_causal_est), 0)
                    self.assertAlmostEqual(mse(s_anticausal, s_anticausal_est), 0)

    def test_cos_sin(self):
        for omega0 in [0.5, 1, 2, 3, 4]:
            for cossin in [0, 1]:
                with self.subTest(omega0=omega0, cossin=cossin):
                    (s_causal, s_anticausal, s_causal_est, s_anticausal_est) = self.cos_sin(omega0, cossin)
                    self.assertAlmostEqual(mse(s_causal, s_causal_est), 0)
                    self.assertAlmostEqual(mse(s_anticausal, s_anticausal_est), 0)


class TestZTransform(unittest.TestCase):
    # TODO - Add more test cases
    def single_pole_order_m(self, H0=1, b=2, m=3):
        # Direct implementation in discrete time domain
        coeff = 1
        for i in range(1, m):
            coeff *= (n + i) / factorial(m - 1)
        coeff = H0 * coeff * b ** n

        s_c = coeff * unitstep(n)
        s_ac = (-1) * coeff * unitstep(-n - m)

        # Inverse transform from z to time domain
        poles = np.array([b])
        zeros = np.array([0])  # Poles and Zeros
        ord_p = np.array([m])
        ord_z = np.array([m])  # Poles' and Zeros' orders

        # Causal
        roc = np.array([b, np.inf])  # region of convergence
        s_c_est = iz_hn(n, H0, poles, zeros, ord_p, ord_z, roc)

        # Anticausal
        roc = np.array([0, b])  # region of convergence
        s_ac_est = iz_hn(n, H0, poles, zeros, ord_p, ord_z, roc)

        return s_c, s_ac, s_c_est, s_ac_est

    def cos(self, omega1):
        s_c = np.cos(omega1 * n) * unitstep(n)
        s_ac = -np.cos(omega1 * n) * unitstep(-n-1)

        # Inverse transform from z to time domain
        poles = np.array([np.cos(omega1) + 1j*np.sin(omega1)])
        ord_p = np.array([1])

        H0 = 1
        zeros = np.array([0, np.cos(omega1)])  # Poles and Zeros
        ord_z = np.array([1, 1])  # Poles' and Zeros' orders

        # Causal
        roc = np.array([np.abs(poles[0]), np.inf])  # region of convergence
        s_c_est = iz_hn(n, H0, poles, zeros, ord_p, ord_z, roc)

        # Anticausal
        roc = np.array([0, np.abs(poles[0])])  # region of convergence
        s_ac_est = iz_hn(n, H0, poles, zeros, ord_p, ord_z, roc)

        return s_c, s_ac, s_c_est, s_ac_est

    def test_single_pole_order(self):
        for H0 in range(1, 5):
            for b in [-2, -0.5, 0.5, 2]:
                for m in range(1, 5):
                    with self.subTest(H0=H0, b=b,  m=m):
                        (s_causal, s_anticausal, s_causal_est, s_anticausal_est) = self.single_pole_order_m(H0, b, m)
                        self.assertAlmostEqual(mse(s_causal, s_causal_est), 0)
                        self.assertAlmostEqual(mse(s_anticausal, s_anticausal_est), 0)

    def test_cos(self):
        for omega1 in [np.pi/4, 3*np.pi/4]:
            with self.subTest(omega1=omega1):
                (s_causal, s_anticausal, s_causal_est, s_anticausal_est) = self.cos(omega1)
                self.assertAlmostEqual(mse(s_causal, s_causal_est), 0)
                self.assertAlmostEqual(mse(s_anticausal, s_anticausal_est), 0)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False);
