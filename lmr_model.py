import json, re, torch
from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
from transformers import DataCollatorForTokenClassification

def predict_loc(text):

    """
        Predicts location in texts and
        returns their mentioned location
    """

    tokenizer = AutoTokenizer.from_pretrained('./un-ner.model/')

    tokens = tokenizer(text)
    torch.tensor(tokens['input_ids']).unsqueeze(0).size()

    model = AutoModelForTokenClassification.from_pretrained('./un-ner.model/', num_labels=len(label_list))
    predictions = model.forward(input_ids=torch.tensor(tokens['input_ids']).unsqueeze(0), attention_mask=torch.tensor(tokens['attention_mask']).unsqueeze(0))
    predictions = torch.argmax(predictions.logits.squeeze(), axis=1)
    predictions = [label_list[i] for i in predictions]

    words = tokenizer.batch_decode(tokens['input_ids'])
    out_labeled = {x:y for x,y in zip(words, predictions)}

    return out_labeled


def load_input_tweets(input_path):
    """function that reads the inputed tweets"""
    tweets = {}
    for line in open(input_path, encoding='utf-8').read().splitlines(): 
        tweet = json.loads(line)
        tweets[tweet["tweet_id"]] = tweet["text"]
    return tweets


def model_output(tweets, path):
    """
       writes the model output to a json file
    """
    with open('output.json', 'w') as file:
        
        for i in range(len(tweets)):
            output = {}
            output["tweet_id"] = list(tweets.keys())[i]
            text = tweets[list(tweets.keys())[i]]
            prediction = predict_loc(text)
            locations = []
            for i in range(len(prediction)):
                if list(prediction.values())[i] != 'O':
                    word = list(prediction.keys())[i]
                    if word not in text.lower():
                        continue
                    start, end = re.search(word, text.lower()).span()
                    locations.append({"text":text[start:end], "start_offset": start, "end_offset": end})
            output["location_mentions"] = locations
            file.write(json.dumps(output) + "\n")


def predict(input_path, output_path):
    """
        make the lmr prediction
    """
    tweets = load_input_tweets(input_path)

    model_output(tweets, output_path)

    print("Model finished predictions!!!")

if __name__ == "__main__":

	predict('/geoai/input.json', "/geoai/output.json")
	
	
