from recommender_system.pipeline.stage_01_data_ingestion import \
    DataIngestionPipeline
from recommender_system.pipeline.stage_02_data_preprocessing import \
    DataPreprocessingPipeline
from recommender_system.pipeline.stage_03_build_model import \
    ModelBuilderPipeline
from recommender_system.pipeline.stage_04_train_model import \
    ModelTrainerPipeline
from recommender_system.pipeline.stage_05_evaluate_model import \
    ModelEvaluationPipeline
from recommender_system.pipeline.stage_06_inference import RecommendProducts
