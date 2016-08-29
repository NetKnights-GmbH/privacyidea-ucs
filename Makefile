info:
	@echo "make clean        - remove all automatically created files"
	@echo "make builddeb     - build .deb file locally"
	
#VERSION=1.3~dev5
VERSION=2.13
SRCDIRS=deploy debian
SRCFILES=Makefile

clean:
	rm -fr DEBUILD
	rm -f meta/*~


builddeb:
	make clean
	mkdir -p DEBUILD/privacyidea-ucs.org
	cp -r ${SRCDIRS} ${SRCFILES} DEBUILD/privacyidea-ucs.org || true
	# We need to touch this, so that our config files 
	# are written to /etc
	cp LICENSE DEBUILD/privacyidea-ucs.org/debian/copyright
	(cd DEBUILD; tar -zcf privacyidea-ucs_${VERSION}.orig.tar.gz --exclude=privacyidea.org/debian privacyidea-ucs.org)
	################# Build
	(cd DEBUILD/privacyidea-ucs.org; debuild --no-lintian)

