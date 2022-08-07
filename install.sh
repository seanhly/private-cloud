if [ -t 0 ]; then
	input_data=""
else
  read -r input_data
fi
label=private-cloud
echo "Clone repository..."
/usr/bin/git clone https://github.com/seanhly/$label /$label
echo "Make..."
(cd /$label && make install-prod)
echo "Install and start..."
if [ "$input_data" ]; then
    $label install --input-data "$input_data"
else
    $label install
fi
echo "Installed."