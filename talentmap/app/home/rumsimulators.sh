streamlit run simul.py --server.baseUrlPath="/simulador/axo" --server.enableXsrfProtection=false server.enableCORS=false --server.address=127.0.0.1 &
streamlit run simulglob.py --server.baseUrlPath="/simulador/axo/glob" --server.enableXsrfProtection=false server.enableCORS=false --server.address=127.0.0.1 --server.port 8502&
streamlit run simulbpu.py --server.baseUrlPath="/simulador/axo/bu" --server.enableXsrfProtection=false server.enableCORS=false --server.address=127.0.0.1 --server.port 8601&

