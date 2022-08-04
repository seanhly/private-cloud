name = private-cloud
build:
	(echo '#!/usr/bin/env python3' && (cd src/py && zip -r - * 2>/dev/null | cat)) > $(name) && chmod 755 $(name)
install: build
	sudo mv $(name) /usr/bin/; sudo chown root:root /usr/bin/$(name); sudo chmod +rx /usr/bin/$(name)
