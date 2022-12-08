import os
import openai

openai.api_key = os.environ.get('OpenAI_API_Key')

def fine_tune(filename, model):
  # upload training data to OAI server
  file = open(filename, "rb")
  file_upload_response = openai.File.create(
    file=file,
    purpose='fine-tune'
  )

  print(f"File Upload Response: {file_response}")

  # schedule fine tuning job
  ft_response = openai.FineTune.create(
      training_file=file_response['id'],
      model=model
  )

  print(f"Fine Tuning Scheduler Response: {ft_response}")

if __name__ == "__main__":
  fine_tune("data.jsonl", "curie")