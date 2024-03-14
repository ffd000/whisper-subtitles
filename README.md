Install

`pip install git+https://github.com/openai/whisper.git pydub`

Chunkize

`ffmpeg -i <in>.mp4 -f segment -segment_time 00:10 chunks/%03d.wav`
