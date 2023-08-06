#
#  Copyright (C) 2007, 2016, 2018, 2020
#      Smithsonian Astrophysical Observatory
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import numpy as np

import sherpa.models.basic as basic
from sherpa.utils import SherpaFloat, _utils
from sherpa.models.model import ArithmeticModel, RegriddableModel1D, RegriddableModel2D


def userfunc(pars, x, *args, **kwargs):
    return x


EXCLUDED_MODELS = (ArithmeticModel, RegriddableModel1D, RegriddableModel2D, basic.Const)

def test_create_and_evaluate():

    x = np.arange(1.0, 5.0)
    count = 0

    for cls in dir(basic):
        clsobj = getattr(basic, cls)

        if not isinstance(clsobj, type) \
            or not issubclass(clsobj, ArithmeticModel) \
            or clsobj in EXCLUDED_MODELS:
            continue

        # These have very different interfaces than the others
        if cls == 'Integrator1D' or cls == 'Integrate1D':
            continue

        m = clsobj()
        if isinstance(m, basic.TableModel):
            m.load(x,x)
        if isinstance(m, basic.UserModel):
            m.calc = userfunc
        assert type(m).__name__.lower() == m.name
        count += 1

        try:
            if m.name.count('2d'):
                pt_out  = m(x, x)
                int_out = m(x, x, x, x)
            else:
                if m.name in ('log', 'log10'):
                    xx = -x
                else:
                    xx = x
                pt_out  = m(xx)
                int_out = m(xx, xx)
        except ValueError:
            assert False, "evaluation of model '{}' failed".format(cls)

        for out in (pt_out, int_out):
            assert out.dtype.type is SherpaFloat
            assert out.shape == x.shape

    assert count == 32
