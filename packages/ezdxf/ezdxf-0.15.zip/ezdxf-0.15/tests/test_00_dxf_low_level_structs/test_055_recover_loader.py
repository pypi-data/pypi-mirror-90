# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
import pytest
from io import BytesIO
from ezdxf.recover import bytes_loader, detect_encoding, synced_bytes_loader
from ezdxf.recover import _detect_dxf_version
from ezdxf.lldxf import const

HEADER = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1027
  9
$ACADMAINTVER
 70
105
  9
$DWGCODEPAGE
  3
ANSI_1252
  9
TEST
  1
ÄÖÜ
"""


class TestBytesLoader:
    @pytest.fixture(params=[bytes_loader, synced_bytes_loader])
    def loader(self, request):
        return request.param

    @pytest.fixture
    def data(self):
        return BytesIO(HEADER.encode('latin1'))

    def test_bytes_loader(self, data, loader):
        result = list(loader(data))
        assert len(result) == 10
        assert result[-1] == (1, b'\xc4\xd6\xdc')

    def test_encoding_detector(self, data, loader):
        assert detect_encoding(loader(data)) == 'utf8'

    def test_windows_line_endings_CR_LF(self, loader):
        tags = list(loader(BytesIO(b"0\r\n1\r\n0\r\n2\r\n")))
        assert tags == [(0, b'1'), (0, b'2')], \
            "Windows line endings CR/LF must be supported."

    def test_linux_and_macos_x_line_endings_LF(self, loader):
        tags = list(bytes_loader(BytesIO(b"0\n1\n0\n2\n")))
        assert tags == [(0, b'1'), (0, b'2')], \
            "Linux and MacOS X line endings LF must be supported."

    def test_line_endings_only_CR(self):
        with pytest.raises(const.DXFStructureError):
            list(bytes_loader(BytesIO(b"0\r1\r0\r2\r")))

        assert list(synced_bytes_loader(BytesIO(b"0\r1\r0\r2\r"))) == [], \
            "MacOS prior to MacOS X line endings CR are not supported."


OUT_OF_SYNC_TAGS = """
  0
SECTION
  2
HEADER

  9
$ACADVER
  1
AC1027
  9
$ACADMAINTVER
 70
105
  9
$DWGCODEPAGE

  3
ANSI_1252
  9
TEST
  1
test
"""


def test_out_of_sync_tags():
    result = list(synced_bytes_loader(
        BytesIO(OUT_OF_SYNC_TAGS.encode())))
    assert len(result) == 10


class TestDetectDXFVersion:
    def test_missing_dxf_version_is_r12(self):
        assert _detect_dxf_version([]) == 'AC1009'

    def test_detect_r12(self):
        assert _detect_dxf_version([(9, '$ACADVER'), (3, 'AC1009')]) == 'AC1009'

    @pytest.mark.parametrize('ver', list(const.acad_release.keys()))
    def test_detect_all_supported_versions(self, ver):
        assert _detect_dxf_version([(9, '$ACADVER'), (3, ver)]) == ver

    def test_detect_any_well_formed_version(self):
        assert _detect_dxf_version([(9, '$ACADVER'), (3, 'AC9999')]) == 'AC9999'

    @pytest.mark.parametrize('ver', [
        'AC10x9', 'XC1009', '0000', 'AC10240', 0, None
    ])
    def test_malformed_version_is_r12(self, ver):
        assert _detect_dxf_version([(9, '$ACADVER'), (3, ver)]) == 'AC1009'

    @pytest.mark.parametrize('ver', [
        ' AC1015', 'AC1015 ', '  AC1015  ',
    ])
    def test_strip_whitespace_from_version_string(self, ver):
        assert _detect_dxf_version([(9, '$ACADVER'), (3, ver)]) == 'AC1015'
