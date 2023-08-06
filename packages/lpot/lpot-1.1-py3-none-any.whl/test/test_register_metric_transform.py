"""Tests for lpot register metric and postprocess """
import numpy as np
import unittest
import os
import yaml
     
def build_fake_yaml():
    fake_yaml = '''
        model:
          name: resnet_v1_101
          framework: tensorflow
          inputs: input
          outputs: resnet_v1_101/predictions/Reshape_1
        device: cpu
        '''
    y = yaml.load(fake_yaml, Loader=yaml.SafeLoader)
    with open('fake_yaml.yaml',"w",encoding="utf-8") as f:
        yaml.dump(y,f)
    f.close()


class TestRegisterMetric(unittest.TestCase):
    model_url = 'https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_6/resnet101_fp32_pretrained_model.pb'
    jpg_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Doll_face_silver_Persian.jpg/1024px-Doll_face_silver_Persian.jpg"

    @classmethod
    def setUpClass(self):
        build_fake_yaml()
        os.system("wget {} -O model.pb".format(self.model_url))
        os.system("wget {} -O test.jpg".format(self.jpg_url))

    @classmethod
    def tearDownClass(self):
        os.remove('fake_yaml.yaml')
        os.remove('model.pb')
        os.remove('test.jpg')

    def test_register_metric_postprocess(self):
        import PIL.Image 
        image = np.array(PIL.Image.open('test.jpg'))
        resize_image = np.resize(image, (224, 224, 3))
        mean = [123.68, 116.78, 103.94]
        resize_image = resize_image - mean
        images = np.expand_dims(resize_image, axis=0)
        labels = [768]
        from lpot import Benchmark, Quantization
        from lpot.data.transforms.imagenet_transform import LabelShift
        from lpot.metric.metric import TensorflowTopK
        evaluator = Benchmark('fake_yaml.yaml')
        evaluator.postprocess('label_benchmark', LabelShift, label_shift=1) 
        evaluator.metric('topk_benchmark', TensorflowTopK)
        dataloader = evaluator.dataloader(dataset=list(zip(images, labels)))
        result = evaluator('model.pb', dataloader)
        acc, batch_size, result_list = result['accuracy']
        self.assertEqual(acc, 1.0)

        quantizer = Quantization('fake_yaml.yaml')
        quantizer.postprocess('label_quantize', LabelShift, label_shift=1) 
        quantizer.metric('topk_quantize', TensorflowTopK)

        evaluator = Benchmark('fake_yaml.yaml')
        evaluator.metric('topk_second', TensorflowTopK)
        dataloader = evaluator.dataloader(dataset=list(zip(images, labels)))
        result = evaluator('model.pb', dataloader)
        acc, batch_size, result_list = result['accuracy']
        self.assertEqual(acc, 0.0)

        

if __name__ == "__main__":
    unittest.main()
