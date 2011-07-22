import Crex
from Crex import Utils
from Crex.Utils import IO
from Crex.Utils import jstor

from jstor_corpus import models

#kw = models.JstorKeywords.objects.all()[0]
#print IO.parse_dfr_keyword_xml(kw.content)
#wc = models.JstorWordCounts.objects.all()[0]
#wcs = IO.parse_dfr_wordcount_xml(wc.content)
#words = [w[1] for w in wcs]
#print " ".join(words)

print len(models.JstorDoc.objects.all())
for t in models.JstorDoc.objects.all():
	print t.j_title