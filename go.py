import whisper
import torch
import torchaudio
import json
import os
import time

model = whisper.load_model('large-v2')

def transcribe_chunks():
	start_time = time.time()
	audio_chunks = sorted([x for x in os.listdir('chunks') if x.endswith('.wav')])
	count = len(audio_chunks)

	transcript = []
	for i, chunk in enumerate(audio_chunks):
	  if i < 1000:
	    out_file = "chunks/{0}".format(chunk)
	    print("\r\nExporting >>", out_file, " - ", i, "/", count)

	    # get duration of wav file
	    # info = torchaudio.info(out_file)
	    duration = 10.0
	    # duration = info.num_frames / info.sample_rate

	    # Transcribe chunk
	    result = model.transcribe(out_file, language='es',verbose=True)

	    for seg in result['segments']:
	      seg['start'] += duration*i
	      seg['end'] += duration*i

	    result['id'] = i

	    transcript.append(result)

	transcript_filename = f"whisper.json"
	f = open(transcript_filename, "w" , encoding='utf-8')

	json.dump(transcript, f, indent=2)

	f.close()
	print(f"Whisper file saved to {f.name} \n")

	end_time = time.time()
	elapsed_time = end_time - start_time

	print(f"Elapsed time: {elapsed_time:.2f} seconds")

def format_time(seconds):
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)

  return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', ',')

def whisper_to_srt(whisper_data, silence_thresh=0.5):
  i=1
  srt = ''
  for trans in whisper_data:
    if not trans['segments']:
      continue

    for segment in trans['segments']:
      if segment['no_speech_prob'] > silence_thresh:
        continue

      start = format_time(segment['start'])
      end = format_time(segment['end'])
      text = segment['text'].strip()

      srt += """{0}
{1} --> {2}
{3}

""".format(i, start, end, text)

      i+=1

  with open('Subtitles.srt', 'w', encoding='utf-8') as f:
    f.write(srt)