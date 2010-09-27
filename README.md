USAGE
=====

[needs update]

(1) to prepare an XML file for the manual tagging
	/usr/local/bin/python2.5 /56k/phd/code/python/crfx.py prep_tag /56k/phd/code/python/10.2307_40236128.xml

(2) to prepare the output of (1) to train the CRF++ model
	/usr/local/bin/python2.5 /56k/phd/code/python/crfx.py prep_train /56k/phd/code/python/10.2307_40236128.safe > /56k/phd/code/python/doc1.train

(3) to create the CRF++ model starting from the output of (2)
	crf_learn -t /56k/phd/code/python/crfx.tpl /56k/phd/code/python/doc1.train /56k/phd/code/python/crfx.mdl