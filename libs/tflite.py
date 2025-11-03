# import tensorflow as tf
from ai_edge_litert.interpreter import Interpreter
# from tflite_runtime.interpreter import Interpreter
import numpy as np
import time


class TfliteHelper:
    def __init__(self, model_path, labels):
        self.model_path = model_path if model_path.endswith(".tflite") \
            else f"{model_path}.tflite"
        self.interpreter = None
        self.labels = labels

    def load_model(self):
        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_detail = self.interpreter.get_input_details()[0]
        self.output_detail = self.interpreter.get_output_details()[0]

    def inference(self, input, label=True):
        if self.interpreter is None:
            self.load_model()
        self.interpreter.set_tensor(
            self.input_detail['index'],
            np.astype(input[np.newaxis,], np.float32))
        self.interpreter.invoke()
        start_time = time.perf_counter()
        output = self.interpreter.get_tensor(self.output_detail['index'])[0]
        end_time = time.perf_counter()
        diff_time = end_time - start_time
        output = self.label_result(output) if label else output
        return dict(output=output, elapsed=diff_time)

    def label_result(self, result):
        result = [float(val) for val in result]
        if self.labels is None:
            return dict(zip(range(len(result), result)))
        return dict(zip(self.labels, result))


if __name__ == "__main__":
    model = TfliteHelper("heart.tflite", ["NEGATIVE", "POSITIVE"])
    model.load_model()
    print(model.input_detail, model.output_detail)
    input = np.random.rand(8)
    output = model.inference(input)
    print(output)
