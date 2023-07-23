import warnings  # noqa: E501
warnings.filterwarnings('ignore')  # noqa: E501

from jina import DocumentArray, Executor, requests, Flow
from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM
import time
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"


class Vaccuna(Executor):
    def __init__(
            self,
            quantized_model_dir,
            model_basename,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # path to directory containing local model
        # quantized_model_dir="/media/shadowmotion/0CD113590CD11359/code/llm/vicuna/TheBloke_Wizard-Vicuna-30B-Uncensored-GPTQ",
        # model_basename="Wizard-Vicuna-30B-Uncensored-GPTQ-4bit.act.order",

        use_triton = False

        self.tokenizer = AutoTokenizer.from_pretrained(
            quantized_model_dir, use_fast=True)

        self.model = AutoGPTQForCausalLM.from_quantized(quantized_model_dir,
                                                        use_safetensors=True,
                                                        model_basename=model_basename,
                                                        device_map="auto",
                                                        use_triton=use_triton,
                                                        quantize_config=None)

        self.model.seqlen = 8192

    @requests
    def chat(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            s = time.time()

            prompt = doc.text

            print('---------prompt----------')

            print(prompt)

            prompt_template = f'''### Human: {prompt}
            ### Assistant:'''

            input_ids = self.tokenizer(
                prompt_template, return_tensors='pt').input_ids.cuda()

            # pipe = pipeline("text-generation",
            #                 model=self.model,
            #                 tokenizer=self.tokenizer,
            #                 max_new_tokens=512,
            #                 temperature=0.0,
            #                 top_p=0.95,
            #                 repetition_penalty=1.15)

            # generated_text = pipe(prompt_template)[0]['generated_text']

            output = self.model.generate(
                inputs=input_ids, temperature=0.0, max_new_tokens=512)

            generated_text = self.tokenizer.decode(output[0])

            e = time.time()

            print("generated length: {}".format(len(generated_text)))
            print("generated speed: {:.2f} per secomd".format(
                len(generated_text)/(e-s)))
            print("consumed duration: {:.2f}s".format(e-s))

            respond = generated_text.replace(prompt_template, "")

            doc.text = respond

            print('--------response---------')

            print(respond)

            print('----------end------------')


if __name__ == "__main__":
    port = 50003

    # model_dirs = "/media/shadowmotion/0CD113590CD11359/code/llm/vicuna/vicuna-13b-8k-gptq"
    # model_name = "wizard-vicuna-13b-uncensored-superhot-8k-GPTQ-4bit-128g.no-act.order"

    model_dirs = "/media/shadowmotion/0CD113590CD11359/code/llm/vicuna/vicuna-30b-8k-gpqt"
    model_name = "vicuna-33b-1.3-superhot-8k-GPTQ-4bit--1g.act.order"

    f = Flow(port=port).add(
        uses=Vaccuna,
        uses_with={
            "quantized_model_dir": model_dirs,
            "model_basename": model_name,
        },
        gpus='device=0,device=1,device=2,device=3',
    )

    with f:
        # start server, backend server forever
        f.block()
