from recommender_system.logging import logger
from recommender_system.pipeline import (DataIngestionPipeline,
                                         DataPreprocessingPipeline)

pipeline_configs = [
    ("Data Ingestion", DataIngestionPipeline()),
    ("Data Preprocessing", DataPreprocessingPipeline())
]

for stage_name, pipeline in pipeline_configs:
    try:
        logger.info(f"===== Stage {stage_name} started =====")
        pipeline.main()
        logger.info(f"===== Stage {stage_name} completed =====")
    except Exception as e:
        logger.exception(f"Error occurred in stage {stage_name}: {str(e)}")
        raise e
