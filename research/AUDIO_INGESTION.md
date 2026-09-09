# SoundCloud audio fallback

On September 9, 2026, CQ 280 had a publisher audio enclosure but no entry in the retrieved YouTube episode inventory. Its full 2:40:16 recording was downloaded from the enclosure in the show's [RSS feed](https://feeds.soundcloud.com/users/soundcloud:users:183077381/sounds.rss) and transcribed locally. [Publisher episode](https://soundcloud.com/collectors-quest/cq-280-video-games-fell-off).

The successful run used faster-whisper 1.2.1, the Systran conversion of Whisper large-v3, CUDA with int8_float16 computation, batch size 8, beam size 5, English, and voice activity detection. The model ran on the local GPU. No API key or paid transcription API was used. A small English CPU model was tried first; its incomplete output was replaced by the completed large-v3 run and was not published as a full transcript. [faster-whisper documentation](https://github.com/SYSTRAN/faster-whisper), [model](https://huggingface.co/Systran/faster-whisper-large-v3).

The final output contains 347 timed segments and 27,158 words. Its last segment ends at 9,616.53 seconds against a decoded source duration of 9,616.59 seconds. The opening and closing text were inspected, and the opening was compared with the small-model test. This establishes successful acquisition through the end; it is not a measured word-error rate or a full manual transcription audit.

The text has no reliable speaker labels. Names, games, prices, and exact quotations still require source verification. The public episode page and manifest identify this as newly generated audio transcription, separate from the existing YouTube and Airtable text.

Local working files reside outside the public repository in `../research-local`: `cq280.mp3`, `cq280-local-whisper.json`, and the completed-source registry `audio-transcripts.json`. The registry records the model and settings, original publisher URL, duration, and audio SHA-256. The one-off local runner is `transcribe_cq280.py`, using an isolated `transcription-env` environment. It requires the model and faster-whisper dependencies; it is not required for searching or rebuilding the existing public corpus.

`scripts/build_library.py` imports completed records from `audio-transcripts.json`, retains their provenance, and uses them to fill otherwise missing episode text. Partial progress files are not imported.
