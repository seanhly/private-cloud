if [ -t 0 ]; then
	certbot_suffix=""
else
  read -r certbot_suffix
fi
label=private-cloud
echo "Clone repository..."
/usr/bin/git clone https://github.com/seanhly/$label /$label
echo "Make..."
(cd /$label && make install-prod)
echo "Install and start..."
if [ "$certbot_suffix" ]; then
    $label install --certbot-suffix "$certbot_suffix"
else
    $label install
fi
echo "Installed."