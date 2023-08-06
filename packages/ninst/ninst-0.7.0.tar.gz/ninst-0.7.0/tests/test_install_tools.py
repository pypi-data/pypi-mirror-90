from io import StringIO

import pytest

from niftypet.ninst import install_tools as tls


def test_query(capsys, monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("y"))
    assert tls.query_yesno("hello")
    out, _ = capsys.readouterr()
    assert "hello [Y/n]" in out
    assert "Please respond with" not in out

    monkeypatch.setattr("sys.stdin", StringIO("N"))
    assert not tls.query_yesno("hello")
    out, _ = capsys.readouterr()
    assert "Please respond with" not in out

    monkeypatch.setattr("sys.stdin", StringIO("what\ny"))
    assert tls.query_yesno("hello")
    out, _ = capsys.readouterr()
    assert "Please respond with" in out


def test_check_platform():
    tls.check_platform()


def test_check_depends():
    deps = tls.check_depends()
    assert not {"cmake", "ninja", "cuda", "git"} - deps.keys()
    assert any(isinstance(i, tuple) for i in deps.values())


def test_check_version():
    deps = tls.check_version({})
    assert not {"RESPATH", "REGPATH", "DCM2NIIX", "HMUDIR"} - deps.keys()


def test_install_tool(tmp_path, monkeypatch):
    dname = tmp_path / "install_tool"
    monkeypatch.setenv("PATHTOOLS", str(dname))
    Cnt = {"DIRTOOLS": "NiftyPET_tools_test"}
    assert not dname.exists()
    with pytest.raises(ValueError):
        tls.install_tool("", Cnt)
    assert (dname / Cnt["DIRTOOLS"]).is_dir()


def test_urlopen_cached(tmp_path):
    dname = tmp_path / "urlopen_cached"
    assert not dname.exists()
    url = "https://github.com/NiftyPET/NInst/raw/master/README.rst"
    with tls.urlopen_cached(url, dname, mode="r") as fd:
        assert "NiftyPET Installation Tools" in fd.read()

    assert (dname / "README.rst").is_file()
    assert (dname / "README.rst.url").read_text() == url


def test_extractall(tmp_path):
    dname = tmp_path / "extractall"
    assert not dname.exists()
    url = "https://github.com/NiftyPET/NInst/archive/v0.6.0.zip"
    with tls.urlopen_cached(url, dname) as fd:
        tls.extractall(fd, dname)

    assert (dname / "NInst-0.6.0" / "README.rst").is_file()
    assert (
        "NiftyPET Installation Tools"
        in (dname / "NInst-0.6.0" / "README.rst").read_text()
    )
