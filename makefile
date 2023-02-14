# goal: run demo for CallMine

INPUT_DIR=INPUT_DATA
TINY=$(INPUT_DIR)/tiny_graph.csv
TINY_TEMPORAL=$(INPUT_DIR)/tiny_graph_temporal.csv
DEMO_DATASET=$(INPUT_DIR)/sample_raw_data.csv
FAKE=$(INPUT_DIR)/fake.csv
NODEVEC=nodeVectors.csv
NODEVEC_TEMPORAL=t_nodeVectors.csv
NODEVEC_ALL_FEATURES=allFeatures_nodeVectors.csv
NODEVEC_LABELS=$(INPUT_DIR)/nodeLabels.csv

prep: requirements.txt
	pip3 install -r requirements.txt

demo: tgraph/static_graph.py tgraph/temporal_graph.py tgraph/join_feature_files.py callmine_focus/run_callmine_focus.py
	python3 tgraph/static_graph.py -v -v $(DEMO_DATASET);
	python3 tgraph/temporal_graph.py -v -v $(DEMO_DATASET);
	python3 tgraph/join_feature_files.py -v $(NODEVEC) $(NODEVEC_TEMPORAL);
	python3 callmine_focus/run_callmine_focus.py $(NODEVEC_ALL_FEATURES) 1 10 5 2 "outputs/"
	python3 callmine_focus/run_callmine_focus.py $(NODEVEC_ALL_FEATURES) 1 10 5 3 "outputs/"

demo_avalanche: tgraph/static_graph.py tgraph/temporal_graph.py tgraph/join_feature_files.py tgraph/nd_cloud.py tgraph/nd_cloud_labeled.py callmine_focus/run_callmine_focus.py
	python3 tgraph/static_graph.py -v -v $(TINY);
	python3 tgraph/temporal_graph.py -v -v $(TINY_TEMPORAL);
	python3 tgraph/join_feature_files.py -v $(NODEVEC) $(NODEVEC_TEMPORAL);
	python3 tgraph/nd_cloud.py -v -v -v $(NODEVEC_ALL_FEATURES);
	python3 tgraph/nd_cloud_labeled.py -v -v -v -v $(NODEVEC_ALL_FEATURES) $(NODEVEC_LABELS).gz;
	python3 callmine_focus/run_callmine_focus.py $(NODEVEC_ALL_FEATURES) 1 10 5 2 "outputs/"
	python3 callmine_focus/run_callmine_focus.py $(NODEVEC_ALL_FEATURES) 1 10 5 3 "outputs/"

tst:
	@echo "run test"
	@python3 -m unittest discover -s tgraph/tests -p *test*.py -v

clean:
	\rm -f nodeVectors.csv
	\rm -f t_nodeVectors.csv
	\rm -f allFeatures_nodeVectors.csv
	\rm -rf __pycache__
	\rm -rf tgraph/__pycache__
	\rm -rf tgraph/tests/__pycache__
	\rm -rf callmine_focus/__pycache__
	\rm -rf callmine_focus/gen2Out/__pycache__
	\rm -rf callmine_focus/LookOut/__pycache__
	\rm -rf outputs/
	\rm -f log_CallMine-Focus.txt
	mkdir outputs
	cd INPUT_DATA; make clean

spotless: clean
	cd INPUT_DATA; make spotless
