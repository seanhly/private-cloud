name = private-cloud
local_bin_dir = ${HOME}/Scripts
remote_bin_dir = /usr/bin
build:
	(echo '#!/usr/bin/env python3' && (cd src/py && zip -r - * 2>/dev/null | cat)) > $(name)
	chmod 755 $(name)
install-dev: build
	mkdir -p ${local_bin_dir}/
	mv $(name) ${local_bin_dir}/
	chmod +rx ${local_bin_dir}/$(name)
install-prod: build
	mkdir -p ${remote_bin_dir}/
	mv $(name) ${remote_bin_dir}/
	chmod +rx ${remote_bin_dir}/$(name)
