from core.exceptions import CustomException


def test_custom_exception():
    # Given
    message = "survey-dingdong"

    # When
    exc = CustomException(message=message)

    # Then
    assert exc.message == message
