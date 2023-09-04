from recommender_system.logging import logger
from recommender_system.pipeline.stage_01_data_ingestion import DataIngestionPipeline

pipeline_configs = [("Data Ingestion", DataIngestionPipeline())]

for stage_name, pipeline in pipeline_configs:
    try:
        logger.info(f"===== Stage {stage_name} started =====")
        pipeline.main()
        logger.info(f"===== Stage {stage_name} completed =====")
    except Exception as e:
        logger.exception(f"Error occurred in stage {stage_name}: {str(e)}")
        raise e
