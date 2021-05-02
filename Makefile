run:
	python3 -m uvicorn app.main:app --reload --reload-dir ./app

install:
	python3 -m pip install -r requirements.txt
