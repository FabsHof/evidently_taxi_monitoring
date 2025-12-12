step_1_download_data:
	@echo "Running step 1: Download Data"
	python3 -m src.step_1_download_data
	@echo "Step 1 completed."
step_2_load_and_process_data:
	@echo "Running step 2: Load and Process Data"
	python3 -m src.step_2_load_and_process_data
	@echo "Step 2 completed."