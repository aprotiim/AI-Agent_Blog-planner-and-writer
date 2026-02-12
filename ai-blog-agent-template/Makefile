setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

run:
	streamlit run app/streamlit_app.py

lint:
	python -m pip install ruff && ruff check .

test:
	python -m pip install pytest && pytest -q
