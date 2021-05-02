from transformers import (
  default_data_collator,
  AutoModelForQuestionAnswering,
  AutoTokenizer,
  Trainer,
)
import numpy as np
import pandas as pd
from datasets import load_dataset

model = AutoModelForQuestionAnswering.from_pretrained('./data/v3')
model_name = "wangchanberta-base-att-spm-uncased" 
tokenizer = AutoTokenizer.from_pretrained(
                f'airesearch/{model_name}',
                revision='main',
                model_max_length=416,)

data_collator = default_data_collator

trainer = Trainer(
  model,
  data_collator=data_collator,
  tokenizer=tokenizer,
)

def post_process(data, raw_predictions, tokenizer, n_best_size = 20, max_answer_length=50):
  all_start_logits, all_end_logits = raw_predictions
  predictions = []
  for start_logits, end_logits, example in zip(all_start_logits, all_end_logits, data):
    start_indexes = np.argsort(start_logits)[-1 : -n_best_size - 1 : -1].tolist()
    end_indexes = np.argsort(end_logits)[-1 : -n_best_size - 1 : -1].tolist()
    valid_answers = []
    for start_index in start_indexes:
      for end_index in end_indexes:
          # Don't consider answers with a length that is either < 0 or > max_answer_length.
          if end_index < start_index or end_index - start_index + 1 > max_answer_length:
              continue
          valid_answers.append(
              {
                  "score": start_logits[start_index] + end_logits[end_index],
                  "text": tokenizer.decode(example['input_ids'][start_index:end_index], skip_special_tokens=True)
              }
          )
    if len(valid_answers) > 0:
        best_answer = sorted(valid_answers, key=lambda x: x["score"], reverse=True)[0]
    else:
        # In the very rare edge case we have not a single non-null prediction, we create a fake prediction to avoid failure.
        best_answer = {"text": "", "score": 0.0} 
    predictions.append(best_answer["text"])
  return predictions
def predict(texts):
  inp_ids = tokenizer(texts, max_length=416, truncation=True, padding='max_length')['input_ids']
  att_mask = tokenizer(texts, max_length=416, truncation=True, padding='max_length')['attention_mask']
  res = pd.DataFrame(columns=['attention_mask', 'input_ids'])
  res = res.append({'attention_mask': att_mask, 
                    'input_ids': inp_ids}, ignore_index=True)
  res.to_json('text.json', orient='records', lines=True)
  dataset = load_dataset('json', data_files='text.json')
  raw_predictions = trainer.predict(dataset['train'])
  predictions = post_process(dataset['train'], raw_predictions[0], tokenizer)
  if ',' in predictions[0][:10]:
    return ''.join(predictions[0].split(',')[1:])
  return predictions[0]
