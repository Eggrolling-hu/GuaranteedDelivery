from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

# path to directory containing local model
quantized_model_dir = "/media/shadowmotion/0CD113590CD11359/code/llm/vicuna/TheBloke_Wizard-Vicuna-30B-Uncensored-GPTQ"

model_basename = "Wizard-Vicuna-30B-Uncensored-GPTQ-4bit.act.order"

use_triton = False

tokenizer = AutoTokenizer.from_pretrained(quantized_model_dir, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(quantized_model_dir,
                                           use_safetensors=True,
                                           model_basename=model_basename,
                                           device_map="auto",
                                           use_triton=use_triton,
                                           quantize_config=None)

# Prevent printing spurious transformers error when using pipeline with AutoGPTQ
logging.set_verbosity(logging.CRITICAL)

prompt = "Tell me about AI"
prompt_template = f'''### Human: {prompt}
### Assistant:'''

print("*** Pipeline:")
pipe = pipeline("text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=512,
                temperature=0.1,
                top_p=0.95,
                repetition_penalty=1.15)

respond = pipe(prompt_template)[0]['generated_text']

print("\n\n*** Generate:")

input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
output = model.generate(inputs=input_ids, temperature=0.7, max_new_tokens=512)
print(tokenizer.decode(output[0]))
