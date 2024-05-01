import whisperx
import gc
import os

device = "cpu"
batch_size = 4  # reduce if low on GPU mem
compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)

audio_file = "/home/nashtech/PycharmProjects/POC_for_triggering_email/sample-1.mp3"

audio = whisperx.load_audio(audio_file)

model = whisperx.load_model("large-v2", device, compute_type=compute_type)

result = model.transcribe(audio, batch_size=batch_size)

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

#print(result)

cleaned_data = []
for segment in result['segments']:
    text = segment['text']
    # Removing occurrences of double quotes or single quotes
    text = text.replace('"', '')
    cleaned_data.append(text)

# Printing the cleaned text
print(''.join(cleaned_data))


def startfile(fn):
    os.system('open %s' % fn)


def create_and_open_txt(filename, text):
    try:
        # Create and write the text to a txt file
        with open(filename, "w") as file:
            file.write(text)
        startfile(filename)
        return True
    except Exception as e:
        print("Error:", e)
        return False


result = create_and_open_txt("output" + "_en" + ".txt", str(cleaned_data))

if result:
    import smtp
    smtp.send_email(smtp.sender_email, smtp.receiver_emails, smtp.password, smtp.message)
    os.remove("output_en.txt")
