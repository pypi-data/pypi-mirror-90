#
#  Copyright (C) 2017, 2018, 2020  Smithsonian Astrophysical Observatory
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

"""
Should these tests be moved to test_astro_session.py?

This is almost a copy of sherpa/ui/tests/test_ui_unit.py, but
some of the answers are different. Is there a better way than
this duplication? Yes, we can parametrize by Session class
and run on both, to avoid duplication.
"""

import numpy as np

import pytest

from sherpa.astro import ui
from sherpa.utils import poisson_noise
from sherpa.utils.err import ArgumentTypeErr, DataErr, IdentifierErr, ModelErr


# This is part of #397
#
def test_list_samplers():
    """Ensure list_samplers returns a list."""

    samplers = ui.list_samplers()

    assert isinstance(samplers, list)
    assert len(samplers) > 0


def test_list_samplers_contents():
    """Are the expected values included"""

    # Test that the expected values exist in this list,
    # but do not enforce these are the only values. This is
    # a slightly-different return list to the non-astro version.
    #
    samplers = ui.list_samplers()
    for expected in ['mh', 'metropolismh', 'pragbayes', 'fullbayes']:
        assert expected in samplers


def test_all_has_no_repeated_elements():
    """Ensure __all__ does not contain repeated elements.

    It is not actually a problem if this happens, but it does
    indicate the possibility of confusion over what functionality
    the repeated symbol has (originally noticed with erf, which
    could be either sherpa.utils.erf or the ModelWrapper version
    of sherpa.models.basic.Erf). See
    https://github.com/sherpa/sherpa/issues/502
    """

    n1 = len(ui.__all__)
    n2 = len(set(ui.__all__))
    assert n1 == n2


def setup_data1d_fit():
    """Create a 1D dataset for fitting a gaussian-like profile.

    This sets the random seed to a fixed value, so use the
    reset_seed fixture.
    """

    x = np.linspace(2300, 2400, 51)

    cpt = ui.voigt1d('cpt')
    cpt.pos = 2345
    cpt.fwhm_g = 20
    cpt.fwhm_l = 15
    cpt.ampl = 480

    np.random.seed(72383)
    y = poisson_noise(cpt(x))

    ui.load_arrays(1, x, y, ui.Data1D)
    ui.set_stat('leastsq')
    ui.set_method('simplex')
    ui.delete_model_component('cpt')


@pytest.mark.parametrize("model,stat,pars",
                         [(ui.gauss1d, 168.05369410194248,
                           [33.39014224934166, 2343.993186258643, 10.837604379839043]),
                          (ui.normgauss1d, 168.05369410194248,
                           [33.39014225250392, 2343.9931862492167, 385.19777742500384]),
                          (ui.lorentz1d, 175.07991080617057,
                           [27.355631135552674, 2342.94368338116, 504.57588886948827]),
                          (ui.pseudovoigt1d, 163.17653966109435,
                           [0.5253350907054826, 31.35910472670331, 2343.6786455810307, 440.7219934649222]),
                          (ui.voigt1d, 162.4321009471359,
                           [24.290859063445527, 12.35931466539915, 2343.751436403753, 437.0342780289447])
                         ])
def test_fit_profile(model, stat, pars, reset_seed, clean_astro_ui):
    """Regression test simple 1D fits"""

    setup_data1d_fit()
    ui.set_source(model('mdl'))
    ui.guess()
    ui.fit()

    assert ui.calc_stat() == pytest.approx(stat)
    assert np.asarray(mdl.thawedpars) == pytest.approx(np.asarray(pars))


@pytest.mark.parametrize("func", [ui.notice_id, ui.ignore_id])
def test_check_ids_not_none(func):
    """Check they error out when id is None"""

    with pytest.raises(ArgumentTypeErr) as exc:
        func(None)

    assert str(exc.value) == "'ids' must be an identifier or list of identifiers"


@pytest.mark.parametrize("f", [[False, True], np.asarray([False, True])])
@pytest.mark.parametrize("bid", [None, 1])
def test_set_filter_mismatch(f, bid):
    """Does set_filter error when there's a mis-match?
    """

    ui.load_arrays(1, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(bkg)
    with pytest.raises(DataErr) as exc:
        ui.set_filter(f, bkg_id=bid)

    assert str(exc.value) == 'size mismatch between 3 and 2'


@pytest.mark.parametrize("f", [[False, True], np.asarray([False, True])])
@pytest.mark.parametrize("bid", [None, 1])
def test_set_filter_mismatch_with_filter(f, bid):
    """Does set_filter error when there's a mis-match after a filter?

    test_set_filter_mismatch checks when .mask is a scalar,
    so now check when it's a NumPy array.
    """

    ui.load_arrays(1, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(bkg)

    ui.ignore(3, None)  # set the .mask attribute to an array

    with pytest.raises(DataErr) as exc:
        ui.set_filter(f, bkg_id=bid)

    assert str(exc.value) == 'size mismatch between 3 and 2'


@pytest.mark.parametrize("bid", [None, 1])
def test_get_syserror_missing(bid):
    """Does get_syserror error out?"""

    ui.load_arrays(1, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(bkg)
    with pytest.raises(DataErr) as exc:
        ui.get_syserror(bkg_id=bid)

    assert str(exc.value) == "data set '1' does not specify systematic errors"


@pytest.mark.parametrize("bid", [None, 1])
def test_save_filter_ignored(bid):
    """Does save_filter error out if everything is masked?

    We should be able to write out the filter in this case,
    as it's easy (all False).
    """

    ui.load_arrays(1, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(bkg)

    ui.ignore(None, None)

    with pytest.raises(DataErr) as exc:
        ui.save_filter("temp-file-that-should-not-be-created",
                       bkg_id=bid)

    assert str(exc.value) == "mask excludes all data"


@pytest.mark.parametrize("func,emsg",
                         [(ui.save_filter, "data set '1' has no filter"),
                          (ui.save_grouping, "data set '1' does not specify grouping flags"),
                          (ui.save_quality, "data set '1' does not specify quality flags")])
@pytest.mark.parametrize("bid", [None, 1])
def test_save_xxx_nodata(func, emsg, bid):
    """Does save_xxx error out if there's no data to save?
    """

    ui.load_arrays(1, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(bkg)

    with pytest.raises(DataErr) as exc:
        func("temp-file-that-should-not-be-created", bkg_id=bid)

    assert str(exc.value) == emsg


def test_delete_bkg_model(clean_astro_ui):
    """Check we can delete a background model"""

    channels = np.arange(1, 5)
    counts = np.zeros(channels.size)
    d = ui.DataPHA('src', channels, counts)
    b = ui.DataPHA('bkg', channels, counts)
    d.set_background(b, id=2)
    ui.set_data(d)

    ui.set_bkg_source(ui.const1d.bmdl + ui.gauss1d.gmdl, bkg_id=2)
    assert ui.get_bkg_source(bkg_id=2) is not None

    ui.delete_bkg_model(bkg_id=2)

    # Expression has been removed
    #
    with pytest.raises(ModelErr) as exc:
        ui.get_bkg_source(bkg_id=2)

    assert str(exc.value) == 'background model 2 for data set 1 has not been set'

    # components still exist
    mdls = ui.list_model_components()
    assert set(mdls) == set(['bmdl', 'gmdl'])


def test_default_background_issue(clean_astro_ui):
    """Test issue #943"""

    ui.set_default_id('x')

    # use least-square as we don't really care about the fit
    ui.set_stat('leastsq')

    ui.load_arrays('x', [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    arf = ui.create_arf(np.asarray([0.1, 0.2, 0.3]), np.asarray([0.2, 0.3, 0.4]))
    bkg.set_arf(arf)
    ui.set_bkg(bkg)

    ui.set_bkg_source(ui.const1d.mdl2)

    # Ensure we can fit the background model. Prior to #943 being
    # fixed the fit_bkg call would error out.
    #
    ui.fit_bkg()
    assert mdl2.c0.val == pytest.approx(2 / 3 / 0.1)


def test_show_bkg_model_issue943(clean_astro_ui):
    """Test issue #943

    We do not check that show_bkg_model is creating anything
    useful, just that it can be called.

    See https://github.com/sherpa/sherpa/issues/943#issuecomment-696119982
    """

    ui.set_default_id('x')

    ui.load_arrays('x', [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    arf = ui.create_arf(np.asarray([0.1, 0.2, 0.3]), np.asarray([0.2, 0.3, 0.4]))
    bkg.set_arf(arf)
    ui.set_bkg(bkg)

    ui.set_bkg_source(ui.const1d.mdl2)
    ui.show_bkg_model()


def test_default_background_issue_fit(clean_astro_ui):
    """Test issue #943 with fit

    See https://github.com/sherpa/sherpa/issues/943#issuecomment-696119982
    """

    ui.set_default_id('x')

    # use least-square as we don't really care about the fit
    ui.set_stat('leastsq')

    ui.load_arrays('x', [1, 2, 3, 4], [5, 4, 3, 4], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3, 4]), [1, 1, 0, 1])
    arf = ui.create_arf(np.asarray([0.1, 0.2, 0.3, 0.4]),
                        np.asarray([0.2, 0.3, 0.4, 0.5]))
    ui.set_arf(arf)
    bkg.set_arf(arf)
    ui.set_bkg(bkg)

    # The model being fitted is a constant to 1,1,0,1 for
    # the background, so that should be 0.75 / 0.1 (as the
    # bin width is constant), and for the source it is
    # 5,4,3,4 - <0.75> [here ignoring the bin-width],
    # so [4.25,3.25,2.25,3.25] -> 13 / 4 -> 3.25
    #
    ui.set_source(ui.const1d.mdl1)
    ui.set_bkg_source(ui.const1d.mdl2)

    # Prior to #943 this would give a confusing error.
    #
    ui.fit()
    assert mdl1.c0.val == pytest.approx(3.25 / 0.1)
    assert mdl2.c0.val == pytest.approx(0.75 / 0.1)


def test_bkg_id_get_bkg_source(clean_astro_ui):
    """Check the error message when the background model has not been set (issue #943)"""

    ui.set_default_id('x')

    ui.load_arrays('x', [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(bkg)

    with pytest.raises(ModelErr) as exc:
        ui.get_bkg_source()

    assert str(exc.value) == 'background model 1 for data set x has not been set'


def test_fix_background_id_error_checks1():
    """Check error handling of background id"""

    ui.load_arrays(2, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(2, bkg)

    with pytest.raises(ArgumentTypeErr) as exc:
        ui.get_bkg_source(id=2, bkg_id=bkg)

    assert str(exc.value) == 'identifiers must be integers or strings'


def test_fix_background_id_error_checks2():
    """Check error handling of background id"""

    ui.load_arrays(2, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(2, bkg)

    with pytest.raises(IdentifierErr) as exc:
        ui.get_bkg_source(id=2, bkg_id='bkg')

    assert str(exc.value) == "identifier 'bkg' is a reserved word"


@pytest.mark.parametrize("id", [1, 'x'])
def test_delete_bkg_model_with_bkgid(id, clean_astro_ui):
    """Check we call delete_bkg_model with non-default bkg_id"""

    ui.load_arrays(id, [1, 2, 3], [5, 4, 3], ui.DataPHA)
    bkg = ui.DataPHA('bkg', np.asarray([1, 2, 3]), [1, 1, 0])
    ui.set_bkg(id, bkg, bkg_id=2)

    ui.set_bkg_source(id, ui.const1d.bmdl, bkg_id=2)
    assert ui.list_model_components() == ['bmdl']
    assert ui.get_bkg_source(id, 2).name == 'const1d.bmdl'

    ui.delete_bkg_model(id, bkg_id=2)
    assert ui.list_model_components() == ['bmdl']

    with pytest.raises(ModelErr) as exc:
        ui.get_bkg_source(id, 2)

    emsg = 'background model 2 for data set {} has not been set'.format(id)
    assert str(exc.value) == emsg
