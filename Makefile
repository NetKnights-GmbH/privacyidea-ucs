info:
	@echo "make clean        - remove all automatically created files"
	@echo "make builddeb     - build .deb file locally"
	@echo "make fetch-changelog"
	@echo "make convert-changelog"
	@echo "make package"
	
#VERSION=1.3~dev5
VERSION=2.21.4
SRCDIRS=deploy debian
SRCFILES=Makefile

package:
	tar -zcf pi-${VERSION}.tgz meta/ DEBUILD/privacyidea-ucs_${VERSION}-1_all.deb privacyidea-venv_${VERSION}-1_amd64.deb

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

fetch-changelog:
	curl https://raw.githubusercontent.com/privacyidea/privacyidea/master/Changelog -O .

convert-changelog:
	pandoc Changelog -o changelog.html -t html
