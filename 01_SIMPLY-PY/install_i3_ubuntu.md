** Create autostart entry to replace mutter(ubuntu default window manager) with i3 window manager.**


((user installation and the wm maynot be loaded as mutter gets loaded after login, we need to load the i3 before login happens.))
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/i3-replace.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=i3 as WM
Exec=/usr/bin/i3 --replace #(kills mutter)
X-GNOME-Autostart-enabled=true
Comment=Replace Mutter (Unity’s WM) with i3 on login
EOF




((INSTALL I3 ALONGSIDE GNOME))
{{sudo apt install i3}}

((If get locked out))
{{rm ~/.config/autostart/i3-replace.desktop}}
reboot