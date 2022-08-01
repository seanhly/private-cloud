label=private-cloud
echo "Clone repository..."
/usr/bin/git clone https://github.com/seanhly/$label /$label
echo "Make..."
(cd /$label && make install)
echo "Install and start..."
$label install
