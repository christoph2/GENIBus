import pytest

from genibus import utils


def test_slicer_basic_chunks() -> None:
    result = utils.slicer([1, 2, 3, 4, 5], 2)

    assert result == [[1, 2], [3, 4], [5]]


def test_cygpath_snake_case_and_legacy_alias() -> None:
    cyg_path = "/cygdrive/c/temp/test"

    assert utils.cygpath_to_win(cyg_path) == "c:\\temp\\test"
    assert utils.cygpathToWin(cyg_path) == "c:\\temp\\test"


def test_run_command_snake_case_and_legacy_alias() -> None:
    output_new = utils.run_command('python -c "print(123)"')
    output_old = utils.runCommand('python -c "print(123)"')

    assert output_new.strip() == b"123"
    assert output_old.strip() == b"123"


def test_run_command_raises_on_failure() -> None:
    with pytest.raises(utils.CommandError):
        utils.run_command('python -c "import sys; sys.exit(2)"')

