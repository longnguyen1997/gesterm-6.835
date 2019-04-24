from imports import *
from GRTPy3.GRT import *

pipeline = GestureRecognitionPipeline()
pipeline.addPreProcessingModule(MovingAverageFilter(5, 1))
pipeline.addFeatureExtractionModule( FFT(512) );

# pipeline.addFeatureExtractionModule( MyOwnFeatureMethod() );

pipeline.setClassifier( ANBC() );

pipeline.addPostProcessingModule( ClassLabelTimeoutFilter(1000) );