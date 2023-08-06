# This file is part of xrayutilities.
#
# xrayutilities is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2019 Dominik Kriegner <dominik.kriegner@gmail.com>

import unittest

import numpy
import xrayutilities as xu

try:
    import lmfit
except ImportError:
    lmfit = None


@unittest.skipIf(lmfit is None, "the lmfit Python package is needed")
class Test_DynamicalModel(unittest.TestCase):
    # define used layer stack
    sub = xu.simpack.Layer(xu.materials.GaAs, numpy.inf)
    lay = xu.simpack.Layer(xu.materials.AlGaAs(0.75), 995.64, relaxation=0.0)
    pls = xu.simpack.PseudomorphicStack001('AlGaAs on GaAs', sub, lay)
    hkl = (0, 0, 4)

    # simulation parameters
    kwargs = dict(I0=1e6, background=0, resolution_width=1e-5)

    @classmethod
    def setUpClass(cls):
        cls.sdyn = xu.simpack.SimpleDynamicalCoplanarModel(cls.pls,
                                                           **cls.kwargs)
        cls.dyn = xu.simpack.DynamicalModel(cls.pls, **cls.kwargs)
        cls.fms = xu.simpack.FitModel(cls.sdyn)
        cls.fmd = xu.simpack.FitModel(cls.dyn)
        qz = numpy.linspace(4.40, 4.50, 2000)
        cls.ai = xu.simpack.coplanar_alphai(0, qz)

    def test_Calculation(self):
        sim = self.dyn.simulate(self.ai, hkl=self.hkl)
        self.assertEqual(len(sim), len(self.ai))
        self.assertTrue(numpy.all(sim >= self.kwargs['background']))
        self.assertTrue(numpy.all(sim <= self.kwargs['I0']))

    def test_FitModel_eval(self):
        sim1 = self.sdyn.simulate(self.ai, hkl=self.hkl)
        p = self.fms.make_params()
        sim2 = self.fms.eval(p, x=self.ai, hkl=self.hkl)
        for v1, v2 in zip(sim1, sim2):
            self.assertAlmostEqual(v1, v2, places=10)

    def test_FitModel_eval_dyn(self):
        sim1 = self.dyn.simulate(self.ai, hkl=self.hkl)
        p = self.fmd.make_params()
        sim2 = self.fmd.eval(p, x=self.ai, hkl=self.hkl)
        for v1, v2 in zip(sim1, sim2):
            self.assertAlmostEqual(v1, v2, places=10)

    def test_Consistency(self):
        sim1 = self.sdyn.simulate(self.ai, hkl=self.hkl)
        sim2 = self.dyn.simulate(self.ai, hkl=self.hkl)
        self.assertEqual(len(sim1), len(sim2))
        self.assertEqual(numpy.argmax(sim1), numpy.argmax(sim2))
        self.assertAlmostEqual(xu.math.fwhm_exp(self.ai, sim1),
                               xu.math.fwhm_exp(self.ai, sim2), places=4)
        self.assertTrue(xu.math.fwhm_exp(self.ai, sim1) >=
                        self.kwargs['resolution_width'])


if __name__ == '__main__':
    unittest.main()
