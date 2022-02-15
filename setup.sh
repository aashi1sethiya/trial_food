mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
primaryColor='#716657'
backgroundColor='#DAF2DA'
secondaryBackgroundColor='#544B35'
textColor='#1D1D1F'
font='serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml