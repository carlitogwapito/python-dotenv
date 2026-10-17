import io
import os
from unittest import mock

import pytest

from dotenv import dotenv_values, load_dotenv


@pytest.mark.parametrize("override", [False, True])
@pytest.mark.parametrize(
    "content,value",
    [
        ("DOTENV_RESULT_KEY=new\nDOTENV_RESULT_KEY\n", None),
        ("DOTENV_RESULT_KEY\nDOTENV_RESULT_KEY=new\n", "new"),
        ("DOTENV_RESULT_KEY=\n", ""),
        ("DOTENV_RESULT_KEY=${DOTENV_RESULT_MISSING}\n", ""),
    ],
    ids=["final-bare", "final-valued", "explicit-empty", "interpolated-empty"],
)
def test_load_result_after_resolving_values(override, content, value):
    before = dict(os.environ)
    seed = {"DOTENV_RESULT_KEY": "existing", "DOTENV_RESULT_KEEP": "untouched"}
    expected = dict(seed)
    if override and value is not None:
        expected["DOTENV_RESULT_KEY"] = value

    with mock.patch.dict(os.environ, seed, clear=True):
        assert dotenv_values(stream=io.StringIO(content)) == {
            "DOTENV_RESULT_KEY": value
        }
        assert load_dotenv(stream=io.StringIO(content), override=override) is (
            value is not None
        )
        assert dict(os.environ) == expected

    assert dict(os.environ) == before
