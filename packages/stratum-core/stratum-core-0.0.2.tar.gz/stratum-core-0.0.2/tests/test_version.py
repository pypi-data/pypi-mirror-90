from pytest import raises
from src.version import Version
from src.exceptions import VersionError


def test_mmp():
    """Major, minor, patch.
        A normal version number MUST take the form X.Y.Z where
        X, Y, and Z are non-negative integers. X is the major
        version, Y is the minor version, and Z is the patch
        version. Each element MUST increase numerically by
        increments of one. For instance: 1.9.0 -> 1.10.0 ->
        1.11.0.
    """
    assert str(Version("0.0.0")) == "0.0.0"
    assert repr(Version("0.0.0")) == "Version(0.0.0)"
    assert str(Version("1.2.3")) == "1.2.3"
    assert repr(Version("1.2.3")) == "Version(1.2.3)"

    with raises(VersionError):
        Version("X.Y.Z")

    assert Version("1.2.3").major == 1
    assert Version("1.2.3").minor == 2
    assert Version("1.2.3").patch == 3

    assert Version("1.1.3") < Version("2.0.0")
    assert Version("2.1.7") < Version("10.11.20")
    assert Version("2.0.0") < Version("2.1.0") < Version("2.1.2")


def test_pre_release():
    """Pre-release version.
        A pre-release version MAY be denoted by appending a dash
        and a series of dot separated identifiers immediately
        following the patch version. Identifiers MUST be
        comprised of only ASCII alphanumerics and dash
        [0-9A-Za-z-]. Pre-release versions satisfy but have a
        lower precedence than the associated normal version.
        Examples: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7,
        1.0.0-x.7.z.92.
    """

    assert Version("1.0.0").pre_release == []
    assert Version("1.0.0-alpha").pre_release == ["alpha"]
    assert Version("1.0.0-alpha.1").pre_release == ["alpha", 1]
    assert Version("1.0.0-0.23.99").pre_release == [0, 23, 99]
    assert Version("1.0.0-x.7.z.92").pre_release == ["x", 7, "z", 92]
    assert Version("2.1.0-x.y.z.11").__str__() == "2.1.0-x.y.z.11"

    with raises(VersionError):
        Version("1.0.0-")

    with raises(VersionError):
        Version("1.0.0-$#%")

    assert Version("1.0.0") > Version("1.0.0-alpha")
    assert Version("1.0.0-alpha") < Version("1.0.0")


def test_build():
    """Build version.
        A build version MAY be denoted by appending a plus sign
        and a series of dot separated identifiers immediately
        following the patch version or pre-release version.
        Identifiers MUST be comprised of only ASCII
        alphanumerics and dash [0-9A-Za-z-]. Build versions
        satisfy and have a higher precedence than the associated
        normal version. Examples: 1.0.0+build.1,
        1.3.7+build.11.e0f985a.
    """
    assert Version('1.0.0+build.1').build == ['build', 1]
    assert Version('1.0.0+build.11.e0f985a').build == ['build', 11, 'e0f985a']


def test_rules():
    """Precedence rules.
        Precedence MUST be calculated by separating the version
        into major, minor, patch, pre-release, and build
        identifiers in that order. Major, minor, and patch
        versions are always compared numerically. Pre-release
        and build version precedence MUST be determined by
        comparing each dot separated identifier as follows:
        identifiers consisting of only digits are compared
        numerically and identifiers with letters or dashes are
        compared lexically in ASCII sort order. Numeric
        identifiers always have lower precedence than
        non-numeric identifiers. Example: 1.0.0-alpha <
        1.0.0-alpha.1 < 1.0.0-beta.2 < 1.0.0-beta.11 <
        1.0.0-rc.1 < 1.0.0-rc.1+build.1 < 1.0.0 < 1.0.0+0.3.7 <
        1.3.7+build < 1.3.7+build.2.b8f12d7 <
        1.3.7+build.11.e0f985a.
    """
    presorted = [
        '1.0.0-alpha',
        '1.0.0-alpha.1',
        '1.0.0-beta.2',
        '1.0.0-beta.11',
        '1.0.0-rc.1',
        '1.0.0-rc.1+build.1',
        '1.0.0',
        '1.0.0+0.3.7',
        '1.3.7+build',
        '1.3.7+build.2.b8f12d7',
        '1.3.7+build.11.e0f985a',
    ]
    from random import shuffle
    randomized = list(presorted)
    shuffle(randomized)
    fixed = list(map(str, sorted(map(Version, randomized))))
    assert fixed == presorted
