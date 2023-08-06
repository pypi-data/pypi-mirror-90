#
#  Copyright (C) 2020
#        Smithsonian Astrophysical Observatory
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

"""Continued testing of sherpa.astro.data."""

import logging

import numpy as np

import pytest

from sherpa.astro.data import DataIMG, DataPHA
from sherpa.astro.utils._region import Region
from sherpa.utils.err import DataErr
from sherpa.utils.testing import requires_data, requires_fits


def test_can_not_group_ungrouped():
    """Does setting the grouping setting fail with no data?"""

    pha = DataPHA('name', [1, 2, 3], [1, 1, 1])
    assert not pha.grouped
    with pytest.raises(DataErr) as exc:
        pha.grouped = True

    assert str(exc.value) == "data set 'name' does not specify grouping flags"


def test_get_mask_is_none():

    pha = DataPHA('name', [1, 2, 3], [1, 1, 1])
    assert pha.mask is True
    assert pha.get_mask() is None


def test_get_filter_expr_channel():
    """Check get_filter_expr is called"""

    pha = DataPHA('name', np.asarray([1, 2, 3]), [1, 1, 1])
    assert pha.get_filter_expr() == '1-3 Channel'

    pha.ignore(None, 1)
    assert pha.get_filter_expr() == '2-3 Channel'


def test_get_filter_is_empty():

    # Need to send in numpy arrays otherwise the code fails as it
    # assumes a numpy array. This should be addressed upstream.
    #
    # pha = DataPHA('name', [1, 2, 3], [1, 1, 1])
    pha = DataPHA('name', np.asarray([1, 2, 3]), [1, 1, 1])
    assert pha.get_filter() == '1:3'
    pha.ignore()
    assert pha.get_filter() == 'No noticed bins'


@pytest.mark.xfail
def test_need_numpy_channels():
    """We need to convert the  input to NumPy arrrays.

    This should be done in the constructor to DataPHA, but
    for now error out if not set.
    """

    pha = DataPHA('name', [1, 2, 3], [1, 1, 1])
    assert pha.get_filter() == '1:3'
    # This errors out with a TypeError on 'elo = self.channel - 0.5'
    pha.ignore()
    assert pha.get_filter() == 'No noticed bins'


@pytest.mark.parametrize("chan", [0, -1, 4])
def test_error_on_invalid_channel_ungrouped(chan):
    """Does channel access fail when outside the bounds?

    For ungrouped data it currently does not, but just
    acts as an identity function.
    """

    pha = DataPHA('name', [1, 2, 3], [1, 1, 1])
    assert pha._to_channel(chan) == chan
    assert pha._from_channel(chan) == chan


@pytest.mark.parametrize("chan,exp1,exp2",
                         [(0, 1, 3),
                          (-1, 1, 1)])
def test_error_on_invalid_channel_grouped(chan, exp1, exp2):
    """Does channel access fail when outside the bounds?

    It is not clear what _from_channel is doing here, so
    just check the responses.
    """

    pha = DataPHA('name', [1, 2, 3], [1, 1, 1],
                  grouping=[1, -1, 1])
    assert pha.grouped
    assert pha._to_channel(chan) == exp1
    assert pha._from_channel(chan) == exp2


@pytest.mark.parametrize("chan", [-2, 4])
def test_error_on_invalid_channel_grouped2(chan):
    """Does channel access fail when outside the bounds?

    This one does error out in _from_channel.
    """

    pha = DataPHA('name', [1, 2, 3], [1, 1, 1],
                  grouping=[1, -1, 1])
    assert pha.grouped
    with pytest.raises(DataErr) as exc:
        pha._from_channel(chan)

    # The error message is wrong
    # assert str(exc.value) == 'invalid group number: {}'.format(chan)
    assert str(exc.value) == 'invalid group number: {}'.format(chan - 1)


def test_288_a():
    """The issue from #288 which was working"""

    channels = np.arange(1, 6)
    counts = np.asarray([5, 5, 10, 10, 2])
    grouping = np.asarray([1, -1, 1, -1, 1], dtype=np.int16)
    pha = DataPHA('x', channels, counts, grouping=grouping)

    assert pha.mask
    pha.ignore(3, 4)

    # I use approx because it gives a nice answer, even though
    # I want eqiuality not approximation in this test. Fortunately
    # with bools the use of approx is okay (it can tell the
    # difference between 0 and 1, aka False and True).
    #
    assert pha.mask == pytest.approx([True, False, True])


def test_288_b():
    """The issue from #288 which was failing"""

    channels = np.arange(1, 6)
    counts = np.asarray([5, 5, 10, 10, 2])
    grouping = np.asarray([1, -1, 1, -1, 1], dtype=np.int16)
    pha = DataPHA('x', channels, counts, grouping=grouping)

    assert pha.mask
    pha.ignore(3.1, 4)

    assert pha.mask == pytest.approx([True, False, True])


@pytest.mark.xfail
def test_grouping_non_numpy():
    """Historically the group* calls will fail oddly if y is not numpy

    TypeError: grpNumCounts() Could not parse input arguments, please check input for correct type(s)
    """

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [0, 0, 0, 2, 1, 1, 0, 0, 0, 0]

    pha = DataPHA('416', x, y)
    pha.group_counts(3)

    grouping = [1, -1, -1, -1, -1,  1, -1, -1, -1, -1.]
    assert pha.grouping == pytest.approx(grouping)

    quality = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
    assert pha.quality == pytest.approx(quality)


def test_416_a():
    """The first test case from issue #416"""

    # if y is not a numpy array then group_counts errors out
    # with a strange error. Another reason why DataPHA needs
    # to validate input
    #
    x = np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.asarray([0, 0, 0, 2, 1, 1, 0, 0, 0, 0])

    pha = DataPHA('416', x, y)
    pha.notice(3.5, 6.5)

    mask = [False, False, False, True, True, True, False, False, False, False]
    assert pha.mask == pytest.approx(mask)

    pha.group_counts(3)

    # We have a simplified mask
    mask = [True, True]
    assert pha.mask == pytest.approx(mask)

    # the "full" mask can be retrieved with get_mask
    mask = [True] * 10
    assert pha.get_mask() == pytest.approx(mask)

    grouping = [1, -1, -1, -1, -1,  1, -1, -1, -1, -1.]
    assert pha.grouping == pytest.approx(grouping)

    quality = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
    assert pha.quality == pytest.approx(quality)

    dep = pha.get_dep(filter=True)
    assert dep == pytest.approx([3, 1])


def test_416_b(caplog):
    """The second test case from issue #416

    This is to make sure this hasn't changed.
    """

    x = np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.asarray([0, 0, 0, 2, 1, 1, 0, 0, 0, 0])

    pha = DataPHA('416', x, y)
    pha.notice(3.5, 6.5)
    pha.group_counts(3)

    with caplog.at_level(logging.INFO, logger='sherpa'):
        pha.ignore_bad()

    # It's not obvious why this has switched to a boolean
    assert pha.mask

    # Mask is also interesting (currently just reporting
    # this behavior)
    mask = [True] * 5 + [False] * 5
    assert pha.get_mask() == pytest.approx(mask)

    grouping = [1, -1, -1, -1, -1,  1, -1, -1, -1, -1.]
    assert pha.grouping == pytest.approx(grouping)

    quality = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
    assert pha.quality == pytest.approx(quality)

    dep = pha.get_dep(filter=True)
    assert dep == pytest.approx([3])

    # check captured log
    #
    emsg = 'filtering grouped data with quality flags, previous filters deleted'
    assert caplog.record_tuples == [
        ('sherpa.astro.data', logging.WARNING, emsg)
        ]


def test_416_c():
    """The third test case from issue #416
    """

    x = np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.asarray([0, 0, 0, 2, 1, 1, 0, 0, 0, 0])

    pha = DataPHA('416', x, y)
    pha.notice(3.5, 6.5)

    # this should be ~pha.mask
    tabstops = [True] * 3 + [False] * 3 + [True] * 4
    assert ~pha.mask == pytest.approx(tabstops)

    pha.group_counts(3, tabStops=~pha.mask)
    pha.ignore_bad()

    grouping = [0] * 3 + [1, -1, 1] + [0] * 4
    assert pha.grouping == pytest.approx(grouping)

    # the second grouped bin has a quality of 2 as
    # it only contains 1 count
    quality = np.zeros(10, dtype=np.int)
    quality[5] = 2
    assert pha.quality == pytest.approx(quality)

    dep = pha.get_dep(filter=False)
    assert dep == pytest.approx(y)

    # It is not at all obvious why we get 8 bins returned
    # here. The ignore_bad has removed any existing
    # filters, but why do we get 8, not 10, values?
    # Well, one bin has been removed (quality=2)
    # and two bins have merged into 1. Hence the 8.
    #
    dep = pha.get_dep(filter=True)
    exp = np.zeros(8)
    exp[3] = 3
    assert dep == pytest.approx(exp)


@pytest.fixture
def make_test_image():
    """A simple image

    Note that normally you'd have logical axes of 1:31,
    1:21 here and then a WCS, but I've decided to number
    the axes differently (in physical units) as there is
    no requirement that the logical units are 1:nx/ny.
    """

    x1, x0 = np.mgrid[3830:3850, 4245:4275]

    # What is the ordering of shape? At the moment going for
    # NumPy style (ny, nx), but there is no credible documentation
    # (any documentation was added to describe the behavior we
    # have now).
    #
    shape = x0.shape

    x0 = x0.flatten()
    x1 = x1.flatten()
    y = np.ones(x0.size)
    return DataIMG('d', x0, x1, y, shape=shape)


def test_img_set_coord_invalid(make_test_image):
    """An invalid coord setting"""
    d = make_test_image
    assert d.coord == 'logical'

    with pytest.raises(DataErr) as exc:
        d.set_coord('bob')

    emsg = "unknown coordinates: 'bob'\n"
    emsg += "Valid options: logical, image, physical, world, wcs"
    assert str(exc.value) == emsg

    assert d.coord == 'logical'


@pytest.mark.parametrize('coord,expected',
                         [('physical', 'physical'),
                          ('world', 'world'),
                          ('wcs', 'world')])
def test_img_set_coord_notset(coord, expected, make_test_image):
    """A valid coord setting but we don't have the data"""

    d = make_test_image
    with pytest.raises(DataErr) as exc:
        d.set_coord(coord)

    emsg = "data set 'd' does not contain a {} coordinate system".format(expected)
    assert str(exc.value) == emsg

    assert d.coord == 'logical'


@pytest.mark.parametrize('coord,expected',
                         [('physical', 'physical'),
                          ('world', 'world'),
                          ('wcs', 'world')])
def test_img_get_coord_notset(coord, expected, make_test_image):
    """Check get_physical/world fail when there's no WCS"""
    d = make_test_image

    meth = getattr(d, 'get_{}'.format(coord))
    with pytest.raises(DataErr) as exc:
        meth()

    emsg = "data set 'd' does not contain a {} coordinate system".format(expected)
    assert str(exc.value) == emsg


def test_img_set_coord_image(make_test_image):
    """Can set to image though"""
    d = make_test_image
    assert d.coord == 'logical'

    d.set_coord('image')
    assert d.coord == 'logical'


def test_img_get_coord_image(make_test_image):
    """Can call get_image though"""
    d = make_test_image

    cs = d.get_image()

    x1, x0 = np.mgrid[3830:3850, 4245:4275]
    x0 = x0.flatten()
    x1 = x1.flatten()

    assert cs[0] == pytest.approx(x0)
    assert cs[1] == pytest.approx(x1)
    assert len(cs) == 2


@pytest.fixture
def read_test_image(make_data_path):
    from sherpa.astro.io import read_image
    filename = 'acisf07999_000N001_r0035_regevt3_srcimg.fits'
    d = read_image(make_data_path(filename))
    d.name = 'test.img'
    return d


@requires_fits
@requires_data
@pytest.mark.parametrize('coord,expected',
                         [('logical', 'logical'),
                          ('image', 'logical'),
                          ('physical', 'physical'),
                          ('world', 'world'),
                          ('wcs', 'world')])
def test_img_file_set_coord(coord, expected, read_test_image):
    """call set_coord with an image with WCS"""
    d = read_test_image
    assert d.coord == 'logical'
    d.set_coord(coord)
    assert d.coord == expected


@requires_fits
@requires_data
@pytest.mark.parametrize('coord', ['logical', 'image', 'physical', 'world', 'wcs'])
def test_img_file_get_logical(coord, read_test_image):
    """get_logical when coord is set"""
    d = read_test_image
    d.set_coord(coord)

    yexp, xexp = np.mgrid[1:378, 1:170]
    xexp = xexp.flatten()
    yexp = yexp.flatten()

    x, y = d.get_logical()
    assert x == pytest.approx(xexp)
    assert y == pytest.approx(yexp)


@requires_fits
@requires_data
@pytest.mark.parametrize('coord', ['logical', 'image', 'physical', 'world', 'wcs'])
def test_img_file_get_physical(coord, read_test_image):
    """get_physical when coord is set"""
    d = read_test_image
    d.set_coord(coord)

    yexp, xexp = np.mgrid[4333.1298828125:4710:1, 3062.3100585938:3231:1]
    xexp = xexp.flatten()
    yexp = yexp.flatten()

    x, y = d.get_physical()
    assert x == pytest.approx(xexp)
    assert y == pytest.approx(yexp)


@requires_fits
@requires_data
@pytest.mark.parametrize('coord', ['logical', 'image', 'physical', 'world', 'wcs'])
def test_img_file_get_world(coord, read_test_image):
    """get_world when coord is set"""
    d = read_test_image
    d.set_coord(coord)

    # Since the pixel size isn't guaranteed to be constant
    # just check the corners. Note that this is not a
    # check from first principles: it just checks that we
    # get the same answer as previous calls to this routine.
    #
    x, y = d.get_world()

    # BL
    assert x[0] == pytest.approx(150.02683651815326)
    assert y[0] == pytest.approx(2.6402818651328728)

    # TR
    assert x[-1] == pytest.approx(150.00385708212673)
    assert y[-1] == pytest.approx(2.6916707654223244)

    # BR
    assert x[168] == pytest.approx(150.00385224075313)
    assert y[168] == pytest.approx(2.640284264823834)

    # TL
    assert x[169 * 377 - 169] == pytest.approx(150.0268422985145)
    assert y[169 * 377 - 169] == pytest.approx(2.691668318963721)


def test_img_get_axes_logical(make_test_image):
    """Does get_axes work?"""
    d = make_test_image
    x, y = d.get_axes()

    assert x == pytest.approx(np.arange(1, 31, 1))
    assert y == pytest.approx(np.arange(1, 21, 1))


@requires_fits
@requires_data
@pytest.mark.parametrize('coord', ['logical', 'image'])
def test_img_file_get_axes_logical(coord, read_test_image):
    """get_axes when coord is set: logical"""
    d = read_test_image
    d.set_coord(coord)
    x, y = d.get_axes()

    assert x == pytest.approx(np.arange(1, 170, 1))
    assert y == pytest.approx(np.arange(1, 378, 1))


@requires_fits
@requires_data
@pytest.mark.parametrize('coord', ['physical'])
def test_img_file_get_axes_physical(coord, read_test_image):
    """get_axes when coord is set: physical"""
    d = read_test_image
    d.set_coord(coord)
    x, y = d.get_axes()

    assert x == pytest.approx(np.arange(3062.3100585938, 3231, 1))
    assert y == pytest.approx(np.arange(4333.1298828125, 4710, 1))


@requires_fits
@requires_data
@pytest.mark.parametrize('coord', ['world', 'wcs'])
def test_img_file_get_axes_world(coord, read_test_image):
    """get_axes when coord is set: world"""
    d = read_test_image
    d.set_coord(coord)
    x, y = d.get_axes()

    assert x.size == 169
    assert y.size == 377

    # This is an interesting combination of the corners from
    # test_img_file_get_world
    assert x[0] == pytest.approx(150.02683651815326)
    assert y[0] == pytest.approx(2.6402818651328728)
    assert x[-1] == pytest.approx(150.00385224075313)
    assert y[-1] == pytest.approx(2.691668318963721)


@requires_fits
@requires_data
@pytest.mark.parametrize('coord,expected',
                         [('logical', 'x0'),
                          ('image', 'x0'),
                          ('physical', 'x0 (pixels)'),
                          ('world', 'RA (deg)'),
                          ('wcs', 'RA (deg)')])
def test_img_file_get_xlabel(coord, expected, read_test_image):
    """get_x0label"""
    d = read_test_image
    d.set_coord(coord)
    assert d.get_x0label() == expected


@requires_fits
@requires_data
@pytest.mark.parametrize('coord,expected',
                         [('logical', 'x1'),
                          ('image', 'x1'),
                          ('physical', 'x1 (pixels)'),
                          ('world', 'DEC (deg)'),
                          ('wcs', 'DEC (deg)')])
def test_img_file_get_ylabel(coord, expected, read_test_image):
    """get_x1label"""
    d = read_test_image
    d.set_coord(coord)
    assert d.get_x1label() == expected


def test_img_get_bounding_mask_nofilter(make_test_image):
    """get_bounding_mask with no filter"""
    d = make_test_image
    ans = d.get_bounding_mask()
    assert len(ans) == 2
    assert ans[0]
    assert ans[1] is None


def test_img_get_bounding_mask_nodata(make_test_image):
    """get_bounding_mask with all data masked"""
    d = make_test_image
    d.notice2d(ignore=True)
    ans = d.get_bounding_mask()
    assert len(ans) == 2
    assert not ans[0]
    assert ans[1] is None


def test_img_get_bounding_mask_filtered(make_test_image):
    """get_bounding_mask with data partially filtered"""
    d = make_test_image
    d.notice2d('ellipse(4260,3840,3,2,0)')
    ans = d.get_bounding_mask()
    print(np.where(ans[0]))

    mask = np.zeros(5 * 7, dtype=np.bool)
    for i in [ 3,  8,  9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 31]:
        mask[i] = True

    assert len(ans) == 2
    assert ans[0] == pytest.approx(mask)
    assert ans[1] == (5, 7)


def test_img_get_filter(make_test_image):
    """Simple get_filter check on an image."""
    d = make_test_image
    assert d.get_filter() == ''

    shape = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape)
    assert d.get_filter() == shape.capitalize()


def test_img_get_filter_exclude(make_test_image):
    """Simple get_filter check on an image."""
    d = make_test_image
    assert d.get_filter() == ''

    shape = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape, ignore=True)

    expected = '!' + shape.capitalize()
    assert d.get_filter() == expected


def test_img_get_filter_none(make_test_image):
    """Simple get_filter check on an image: no data"""
    d = make_test_image

    shape = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape)
    d.notice2d(ignore=True)

    # It's not clear what the filter should be here
    assert d.get_filter() == ''


def test_img_get_filter_combined(make_test_image):
    """Simple get_filter check on an image."""
    d = make_test_image
    assert d.get_filter() == ''

    shape1 = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape1)

    shape2 = 'rect(4258,3830,4264,3841)'
    d.notice2d(shape2)

    shape2 = shape2.replace('rect', 'rectangle')
    shape = shape1.capitalize() + '&' + shape2.capitalize()
    assert d.get_filter() == shape


def test_img_get_filter_excluded(make_test_image):
    """Simple get_filter check on an image."""
    d = make_test_image
    assert d.get_filter() == ''

    shape1 = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape1)

    shape2 = 'rect(4258,3830,4264,3841)'
    d.notice2d(shape2, ignore=True)

    shape2 = shape2.replace('rect', 'rectangle')
    shape = shape1.capitalize() + '&!' + shape2.capitalize()
    assert d.get_filter() == shape


def check_ignore_ignore(d):
    """Check removing the shapes works as expected."""

    shape1 = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape1, ignore=True)

    mask1 = ~Region(shape1).mask(d.x0, d.x1).astype(np.bool)
    assert d.mask == pytest.approx(mask1)

    shape2 = 'rect(4258,3830,4264,3841)'
    d.notice2d(shape2, ignore=True)

    mask2 = ~Region(shape2).mask(d.x0, d.x1).astype(np.bool)
    assert d.mask == pytest.approx(mask1 & mask2)

    shape2 = shape2.replace('rect', 'rectangle')
    expected = '!' + shape1.capitalize() + '&!' + shape2.capitalize()
    assert d.get_filter() == expected


def check_ignore_ignore2(d):
    """Check removing the shapes works as expected."""

    shape1 = 'ellipse(4260,3840,3,2,0)'
    d.notice2d(shape1, ignore=True)

    mask1 = ~Region(shape1).mask(d.x0, d.x1).astype(np.bool)
    assert d.mask == pytest.approx(mask1)

    shape2 = 'rect(4258,3830,4264,3841)'
    d.notice2d(shape2, ignore=True)

    mask2 = ~Region(shape2).mask(d.x0, d.x1).astype(np.bool)
    assert d.mask == pytest.approx(mask1 & mask2)

    shape2 = shape2.replace('rect', 'rectangle')
    expected = '!' + shape1.capitalize() + '&!' + shape2.capitalize()
    assert d.get_filter() == expected


def test_img_get_filter_included_excluded(make_test_image):
    """Simple get_filter check on an image.

    Just to match test_img_get_filter_excluded_excluded.
    """
    d = make_test_image
    check_ignore_ignore(d)


def test_img_get_filter_excluded_excluded(make_test_image):
    """Simple get_filter check on an image.

    Here we want to check the behavior when d.mask is False.
    I am not sure this makes sense, but this is done to
    show the current behavior.
    """
    d = make_test_image

    assert d.mask
    d.notice2d(ignore=True)
    assert not d.mask

    # It is not at all obvious to me that we should get the
    # same results as test_img_get_filter_included_excluded,
    # as we start with ignoring all points.
    #
    # However, this is just to check the existing behavior,
    # which was not changed in #968.
    #
    check_ignore_ignore(d)


def test_img_get_filter_compare_filtering(make_test_image):
    """Check calling notice2d(ignore=True) with 2 shapes is same as once.

    """
    d = make_test_image

    shape1 = 'ellipse(4260,3840,3,2,0)'
    shape2 = 'rect(4258,3830,4264,3841)'
    d.notice2d(shape1, ignore=True)
    d.notice2d(shape2, ignore=True)
    assert d._region is not None

    maska = d.mask.copy()

    d.notice2d()
    assert d._region is None
    assert d.mask is True

    exc = "field()-{}-{}".format(shape1, shape2)
    d.notice2d(exc)

    maskb = d.mask.copy()
    assert maskb == pytest.approx(maska)

    # just check we have some True and False values
    assert maska.min() == 0
    assert maska.max() == 1
