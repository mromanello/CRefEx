from Crex.crex import FeatureExtractor as FE

class TestExample:
    def test_c(self):
        assert 'c' == 'c'
	def test_b(self):
		assert 'b' == 'b'
		
class TestEFeatureExtractor:
    def test(self):
		fe = FE()
		inp = "Hesiod is a Greek poet".split(" ")
		print fe.get_features(inp,outp_label=False)