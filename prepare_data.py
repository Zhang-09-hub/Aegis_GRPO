import os
import pandas as pd
from datasets import load_dataset
from transformers import AutoTokenizer
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
def main():
    print("Loading Tokenizer...")
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    print("Loading Ageis...")
    dataset = load_dataset('nvidia/Aegis-AI-Content-Safety-Dataset-2.0',split='train')
    unsafe_data = dataset.filter(lambda x:x["prompt_label"]=="unsafe" and x["prompt"]!="REDACTED")
    unsafe_data = unsafe_data.shuffle(seed=42).select(range(1000))
    print(f"Successfully loaded {len(unsafe_data)} unsafe samples.")

    processed_data = []
    for idx,example in enumerate(unsafe_data):
        prompt_message=[
            {"role":"user","content":example["prompt"]}
        ]
        verl_data={
            "data_source": "Ageis",
            "prompt":prompt_message,
            "ability":"safety",
            "reward_model":{
                "style":"model",
                "ground_truth":""
            },
            "extra_info":{
                "index":idx,
                "original_category":example.get("risk_category","unknown")
            }
        }
        processed_data.append(verl_data)
    
    os.makedirs("data",exist_ok=True)
    df = pd.DataFrame(processed_data)
    save_path =  "data/train_safety.parquet"
    df.to_parquet(save_path)
    print(f"Successfully saved processed data to {save_path}")
if __name__ == "__main__":
    main()