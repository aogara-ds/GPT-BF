import csv
import json

def is_react(message):
    "Returns True if a given message is one of the five iMessage reacts."
    reacts = ['Liked ', 'Laughed at ', 'Loved ', 'Disliked ', 'Emphasized ']
    for react in reacts:
        if message[:len(react)]==react:
            return True
    return False


def process_imessage_csv(filename: str, username: str, partnername: str):
    """
    Takes three strings as input: filename, username, and partnername. 
    Returns a list of dictionaries containing prompts and completions
    for the OpenAI Fine-Tuning API. 
    """
    csvfile = open(filename, newline='')
    messages = csv.reader(csvfile, delimiter=',', quotechar='"')

    current_pair = [" ", f"{username}: "]
    prev_speaker = 0

    training_data = []

    for row in messages:
        # skips the header row
        try:
            curr_speaker = int(row[2])
        except:
            continue

        # we don't want the model to use reacts in text
        if is_react(row[1]):
            continue

        if curr_speaker == prev_speaker:
            # add the current message to the right field
            current_pair[curr_speaker] += row[1] + "\n"

        else:
            # if switching to aidan, keep going
            if curr_speaker == 0:
                current_pair[0] += row[1] + "\n"

            # if switching to regan, append and restart
            else:
                training_data.append({
                    'prompt': current_pair[1] + f"\n{partnername}: ",
                    'completion': current_pair[0]
                })
                current_pair = [" ", f"{username}: "]
                current_pair[1] += row[1] + "\n"
        
        prev_speaker = curr_speaker    

    return training_data    


def save_training_data(training_data: list, filename: str, save_every: int):
    """
    Saves the provided training data as a .jsonl file. 
    To save a subsample of the data, provide an integer for save_every. 
    """
    output_file = open(f'{filename}.jsonl', 'w', encoding='utf8')
    i = 0
    for pair in training_data:
        i+=1
        if i % save_every == 0:
            json.dump(pair, output_file, ensure_ascii=False)
            output_file.write('\n')


if __name__ == "__main__": 
    # process csv into prompt-completion pairs
    training_data = process_imessage_csv(
        filename = "messages.csv", 
        username = "Regan", 
        partnername = "AI-Dan"
    )

    # save as .jsonl file
    save_training_data(training_data, 'data', 1)