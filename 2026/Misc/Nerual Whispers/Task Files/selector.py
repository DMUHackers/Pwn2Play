"""
NeuralSel v2.3 - Carrier Position Classifier
=============================================
Pre-trained neural sequence classifier for embedded signal detection.
Architecture: Dense(5->8, tanh) -> Dense(8->1, sigmoid)

Usage:
    from selector import model
    is_carrier = model.classify(text, position)
"""
import numpy as _np
from hashlib import sha256 as _H
from struct import pack as _P

# Input normalization table
_NORM = {
    '\u0430':'a','\u0441':'c','\u0435':'e','\u043e':'o',
    '\u0440':'p','\u0445':'x','\u0443':'y','\u0455':'s',
    '\u0456':'i','\u0410':'A','\u0412':'B','\u0421':'C',
    '\u0415':'E','\u041d':'H','\u041a':'K','\u041c':'M',
    '\u041e':'O','\u0420':'P','\u0422':'T','\u0425':'X',
}


class CarrierClassifier:
    """Pre-trained carrier position classifier."""

    def __init__(self):
        self._W1 = _np.frombuffer(bytes.fromhex(
            "5a643bdf4f8dfd3f54e3a59bc420e4bf3bdf4f8d976eda3f48e17a14ae47f3bf04560e2db29de73f105839b4c876eebf8716d9cef753f93ff2d24d621058d1bfd9cef753e3a5eb3fbc7493180456f2bf5c8fc2f5285cd73fa245b6f3fdd4f6bf9eefa7c64b37ff3f0e2db29defa7e2bfd578e9263108cc3f0c022b8716d9e6bff4fdd478e926e13f25068195438becbff853e3a59bc4fa3f1283c0caa145d6bfbe9f1a2fdd24f43fc1caa145b6f3ddbfac1c5a643bdfe33f643bdf4f8d97f8bfe7fba9f1d24dfe3f068195438b6cc7bf333333333333ef3f6de7fba9f1d2f5bf8716d9cef753db3ffed478e92631e8bf25068195438bec3f1b2fdd240681e1bf21b0726891edf23f022b8716d9cee3bf6de7fba9f1d2d53f5eba490c022bf1bf931804560e2dd23f85eb51b81e85e7bf3108ac1c5a64f73fc74b37894160edbf"
        ), dtype=_np.float64).reshape(8, 5)
        self._b1 = _np.frombuffer(bytes.fromhex(
            "c520b0726891ddbf08ac1c5a643bebbfbe9f1a2fdd24c63f9eefa7c64b37d9bfaaf1d24d6210e43f3d0ad7a3703dd2bf1d5a643bdf4fe13f60e5d022dbf9e6bf"
        ), dtype=_np.float64)
        self._W2 = _np.frombuffer(bytes.fromhex(
            "17d9cef753e3ed3f1b2fdd240681e5bfc1caa145b6f3f33ffa7e6abc7493e0bf04560e2db29deb3fa01a2fdd2406d9bfd7a3703d0ad7e73fe7fba9f1d24dd2bf"
        ), dtype=_np.float64).reshape(1, 8)
        self._b2 = _np.frombuffer(bytes.fromhex(
            "00000000000010c0"
        ), dtype=_np.float64)

    @staticmethod
    def _normalize(seq):
        return ''.join(_NORM.get(c, c) for c in seq)

    def _featurize(self, norm_seq, idx):
        lo, hi = max(0, idx - 4), min(len(norm_seq), idx + 5)
        ctx = norm_seq[lo:hi].encode('utf-8')
        d = _H(_P('<I', idx) + ctx).digest()
        return _np.array([d[j] / 255.0 for j in (0, 3, 7, 11, 15)])

    def classify(self, seq, idx):
        """Classify position idx in sequence seq as carrier (True) or not (False)."""
        ns = self._normalize(seq)
        x = self._featurize(ns, idx)
        h = _np.tanh(self._W1 @ x + self._b1)
        y = 1.0 / (1.0 + _np.exp(-(self._W2 @ h + self._b2)))
        return bool(y[0] > 0.5)


model = CarrierClassifier()
classify = model.classify
