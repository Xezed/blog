from posts.utils import random_word


class TestUtils:
    def test_random_work(self):
        assert len(random_word(3)) == 3
        assert len(random_word(20)) == 20