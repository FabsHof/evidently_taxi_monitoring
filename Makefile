step_1_download_data:
	@echo "Running step 1: Download Data"
	python3 -m src.step_1_download_data
	@echo "Step 1 completed."
step_2_load_and_process_data:
	@echo "Running step 2: Load and Process Data"
	python3 -m src.step_2_load_and_process_data
	@echo "Step 2 completed."
step_3_train_and_evaluate_model:
	@echo "Running step 3: Train and Evaluate Model"
	python3 -m src.step_3_train_and_evaluate_model
	@echo "Step 3 completed."
step_4_generate_report:
	@echo "Running step 4: Generate Report"
	python3 -m src.step_4_generate_report
	@echo "Step 4 completed."
pipeline:
	@echo "Running the complete pipeline"
	python3 -m src.main
	@echo "Pipeline completed."