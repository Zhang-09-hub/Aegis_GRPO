import pandas as pd
from transformers import AutoTokenizer

# 1. 设置路径（指向 ModelScope 的缓存目录）
input_file = "data/train_safety.parquet"
output_file = "data/train_safety_cleaned.parquet"
# 重点修改这里！
model_path = "/mnt/workspace/.cache/modelscope/models/Qwen/Qwen2.5-0.5B-Instruct" 

# 2. 加载分词器
try:
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    print("✅ 分词器加载成功！")
except Exception as e:
    print(f"❌ 分词器加载失败，请检查路径: {e}")
    exit()

# 3. 加载数据
df = pd.read_parquet(input_file)
initial_count = len(df)

# 4. 长度过滤逻辑
def is_valid(prompt):
    if not prompt or len(str(prompt).strip()) == 0:
        return False
    # 计算实际的 Token 数量
    tokens = tokenizer.encode(str(prompt))
    # 限制在 480 以内（为后续训练留出余量）
    return len(tokens) <= 480

print(f"开始清洗... 原始数据: {initial_count} 条")
df_cleaned = df[df['prompt'].apply(is_valid)].copy()

# 5. 去重并保存
df_cleaned = df_cleaned.drop_duplicates(subset=['prompt'])
df_cleaned.to_parquet(output_file)

print(f"✅ 清洗完成！剩余数据: {len(df_cleaned)} 条。")
print(f"新文件已保存至: {output_file}")