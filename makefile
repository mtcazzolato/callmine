# goal: run demo for graph.py

INPUT_DIR=INPUT_DATA
TINY=$(INPUT_DIR)/tiny_graph.csv
TINY_TEMPORAL=$(INPUT_DIR)/tiny_graph_temporal.csv
FAKE=$(INPUT_DIR)/fake.csv
NODEVEC=nodeVectors.csv
NODEVEC_TEMPORAL=t_nodeVectors.csv
NODEVEC_ALL_FEATURES=allFeatures_nodeVectors.csv
NODEVEC_LABELS=$(INPUT_DIR)/nodeLabels.csv

prep: requirements.txt
	pip3 install -r requirements.txt

demo: static_graph.py temporal_graph.py join_feature_files.py nd_cloud.py nd_cloud_labeled.py
	python3 static_graph.py -v -v $(TINY);
	python3 temporal_graph.py -v -v $(TINY_TEMPORAL);
	python3 join_feature_files.py -v $(NODEVEC) $(NODEVEC_TEMPORAL);
	python3 nd_cloud.py -v -v -v $(NODEVEC_ALL_FEATURES);
	python3 nd_cloud_labeled.py -v -v -v -v $(NODEVEC_ALL_FEATURES) $(NODEVEC_LABELS).gz

demos: static_graph.py
	python3 static_graph.py -v -v $(TINY)

demot: temporal_graph.py
	python3 temporal_graph.py -v -v $(TINY_TEMPORAL)

demo_nd_cloud: nd_cloud.py
	python3 nd_cloud.py -v -v -v $(FAKE).gz

demo_nd_cloud_labeled: nd_cloud_labeled.py
	python3 static_graph.py -v -v $(TINY)
	python3 nd_cloud_labeled.py -v -v -v -v $(NODEVEC) $(NODEVEC_LABELS).gz

demo_driver: driver.py static_graph.py nd_cloud.py
	python3 driver.py -v -v -v  $(TINY)

demo_large:
	cd INPUT_DATA; make
	python3 driver.py -v -v -v  INPUT_DATA/large.csv

tst:
	@echo "run test"
	@python3 -m unittest discover -s tests -p *test*.py -v

clean:
	\rm -f nodeVectors.csv
	\rm -f t_nodeVectors.csv
	\rm -f allFeatures_nodeVectors.csv
	\rm -rf __pycache__
	\rm -rf tests/__pycache__
	cd INPUT_DATA; make clean

spotless: clean
	cd INPUT_DATA; make spotless
