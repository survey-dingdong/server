from core.exceptions import CustomException


def test_custom_exception():
    # Given
    message = "dingdong-survey"

    # When
    exc = CustomException(message=message)

    # Then
    assert exc.message == message
