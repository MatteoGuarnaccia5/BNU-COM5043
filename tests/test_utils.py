
from src.utils import Utils
from unittest.mock import patch

def test_display_menu(capsys):
    Utils().display_menu(
        'Test',
        {
            1: 'Option 1',
            2: 'Option 2'
        }
    )
    captured = capsys.readouterr()

    assert 'Test' in captured.out
    assert 'Option 1' in captured.out
    assert 'Option 2' in captured.out

def test_display_table(capsys):
    Utils().display_table(
        title='Test',
        header='This is a test header',
        data=["1", "2"],
        format_row=[
            lambda _: "test 1",
            lambda _: "test 2"
        ]
    )

    captured = capsys.readouterr()

    assert 'Test' in captured.out
    assert 'This is a test header' in captured.out
    assert '1' in captured.out
    assert 'test 1' in captured.out
    assert '2' in captured.out
    assert 'test 2' in captured.out


def test_validate_intput(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3")
    response = Utils().validate_user_intput(
        'Test',
        lower_bound=0,
        upper_bound=5,
        error_msg='Exceeded limit'
    )

    assert response == 3



