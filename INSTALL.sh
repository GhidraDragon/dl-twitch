/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
# brew install python3
python3 -m pip install --upgrade pip
python3 -m pip install requests
python3 -m pip install selenium
echo "alias python='python3'" > ~/.zshrc
brew install yt-dlp
brew install ffmpeg
brew upgrade
open https://www.google.com/chrome/