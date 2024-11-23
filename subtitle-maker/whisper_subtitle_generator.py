import os

from subtitle import SubtitleGenerator, SubtitleResult, Subtitle
import whisperx


class WhisperXSubtitleGenerator(SubtitleGenerator):
    __device = "cpu"
    __whisper_arch = "small"
    __batch_size = 16  # reduce if low on GPU mem
    __compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)

    def generate_subtitle(self, audio_path: str) -> SubtitleResult:
        audio, result = self.__transcribe_with_original_whisper(audio_path)
        result = self.__align_whisper_output(audio, result)

        words = sum(list(map(lambda x: x["words"], result["segments"])), [])
        words = self.__fill_no_start_and_end(words)

        subtitles: list[Subtitle] = list(map(lambda x: Subtitle(x["start"], x["end"], x["word"]), words))

        return SubtitleResult(subtitles)

    def __transcribe_with_original_whisper(self, audio_path: str):
        model_dir = os.environ.get("model_path")

        model = whisperx.load_model(
            whisper_arch=self.__whisper_arch,
            device=self.__device,
            compute_type=self.__compute_type,
            download_root=model_dir
        )

        audio = whisperx.load_audio(audio_path)

        result = model.transcribe(
            audio=audio,
            language='ko',
            batch_size=self.__batch_size
        )

        print(result["segments"])  # before alignment
        return audio, result

    def __align_whisper_output(self, audio, result):
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.__device)

        result = whisperx.align(
            transcript=result["segments"],
            model=model_a,
            align_model_metadata=metadata,
            audio=audio,
            device=self.__device,
            return_char_alignments=False
        )

        # print(result["segments"])  # after alignment
        return result

    def __fill_no_start_and_end(self, words):
        for i in range(len(words)):
            if "start" not in words[i]:
                if i == 0:
                    words[i]["start"] = 0
                else:
                    words[i]["start"] = words[i - 1]["end"]
            if "end" not in words[i]:
                if i == len(words) - 1:
                    words[i]["end"] = words[i]["start"] + 1
                else:
                    for j in range(i + 1, len(words)):
                        if "start" in words[j]:
                            words[i]["end"] = words[j]["start"]
                            break
                    else:
                        words[i]["end"] = words[i]["start"] + 1

        return words


subtitle_generator: SubtitleGenerator = WhisperXSubtitleGenerator()
