SHELL := /bin/bash

.PHONY: all frontend backend static run prometheus grafana up stop

frontend:
	cd frontend && npm install && npm run build

backend:
	cd backend && \
	if [ ! -d ".venv" ]; then python3 -m venv .venv; fi && \
	source .venv/bin/activate && pip install -r requirements.txt

static:
	cd frontend && npm install && npm run build
	mkdir -p backend/app/static
	cp -r frontend/dist/* backend/app/static/

run: static
	cd backend && \
	if [ ! -d ".venv" ]; then python3 -m venv .venv; fi && \
	source .venv/bin/activate && pip install -r requirements.txt && \
	.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 4200

prometheus:
	docker run -d \
		--name prometheus \
		-p 9090:9090 \
		-v $(PWD)/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
		prom/prometheus

grafana:
	docker run -d \
		--name grafana \
		-p 3000:3000 \
		-v $(PWD)/monitoring/grafana:/etc/grafana/provisioning \
		grafana/grafana-oss

up: frontend backend prometheus grafana

stop:
	docker stop prometheus grafana || true
	docker rm prometheus grafana || true

