from mozi_cross_val.models.objmodel import MosesModel

__author__ = 'Abdulrahman Semrie<xabush@singularitynet.io>'

import os
import unittest

from mozi_cross_val.main.model_evaluator import ModelEvaluator
from mozi_cross_val.utils.config import TEST_DATA_DIR


class TestModelEvaluator(unittest.TestCase):
    def setUp(self):
        self.test_combo = [MosesModel("or(and(!$AQP3 $ARHGAP18) !$ANKRD46)", 3),
                           MosesModel("or(and($APLNR !$AQP3) !$ANKRD46)", 4),
                           MosesModel("and(!$ANKRD46 $APLNR)", 5)]
        self.input_file = os.path.join(TEST_DATA_DIR, "bin_truncated.csv")

    def test_run_eval_happy_path(self):
        model_eval = ModelEvaluator("case")

        matrix = model_eval.run_eval(self.test_combo, self.input_file)

        self.assertEqual(matrix.shape[0], 3)

    def test_score_models(self):
        model_eval = ModelEvaluator("case")
        matrix = model_eval.run_eval(self.test_combo, self.input_file)

        scored_matrix = model_eval.score_models(matrix, self.input_file)

        self.assertEqual(len(scored_matrix), 3)


if __name__ == '__main__':
    unittest.main()
