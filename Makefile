name = private-cloud
build:
	(echo '#!/usr/bin/env python3' && (cd src/py && zip -r - * 2>/dev/null | cat)) > $(name) && chmod 755 $(name)
install: build
	mkdir -p ${HOME}/Scripts/
	mv $(name) ${HOME}/Scripts/
	chmod +rx ${HOME}/Scripts/$(name)
