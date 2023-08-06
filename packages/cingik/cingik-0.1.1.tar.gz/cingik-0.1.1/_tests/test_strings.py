from cingik.cingik import strings


def test_answer():
    input_string = 'The     quick brown    fox'
    assert strings.multiple_strip(input_string, " ") == "The quick brown fox"
    assert strings.multiple_strip(input_string, "a") == "The     quick brown    fox"
