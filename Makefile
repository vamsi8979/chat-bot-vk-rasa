.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config"
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data"
	@echo "    run-core"
	@echo "        Runs core server"
	@echo "    run-nlu"
	@echo "        Runs nlu server"
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

train-mms-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --data data/mms-nlu-data/ -o models --fixed_model_name nlu --project current --verbose
train-mms-core:
	python -m rasa_core.train -d domain.yml -s data/mms_stories.md -o models/current/dialogue -c policies.yml
action-server:
	python -m rasa_core_sdk.endpoint --actions actions
run-core:
	python -m rasa_core.run --enable_api --auth_token thisismysecret -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml -o out.log  --cors "*"
run-story-view:
	python -m rasa_core.visualize -d domain.yml -s data/mms_stories.md -o graph.html -c nlu_config.yml
run-core-debug:
	python -m rasa_core.run --enable_api --auth_token thisismysecret -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml -o out.log  --cors "*" --debug
run-interactive:
	python -m rasa_core.train \
  	interactive -o models/current/dialogue \
  	-d domain.yml -s data/mms_stories.md \
  	--nlu models/current/nlu \
  	--endpoints endpoints.yml
run-nlu:
	python -m rasa_nlu.server --path models
run-all-3-commands:
	python -m rasa_nlu.train -c nlu_config.yml --data data/mms-nlu-data/ -o models --fixed_model_name nlu --project current --verbose && \
	python -m rasa_core.train -d domain.yml -s data/mms_stories.md -o models/current/dialogue -c policies.yml && \
	python -m rasa_core.run --enable_api --auth_token thisismysecret -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml -o out.log  --cors "*" --debug