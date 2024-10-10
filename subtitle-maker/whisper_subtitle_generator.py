from subtitle import SubtitleGenerator, SubtitleResult, Subtitle
import whisperx


class WhisperXSubtitleGenerator(SubtitleGenerator):
    __device = "cpu"
    __whisper_arch = "large-v2"
    __batch_size = 16  # reduce if low on GPU mem
    __compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)

    def generate_subtitle(self, audio_path: str) -> SubtitleResult:
        audio, result = self.__transcribe_with_original_whisper(audio_path)
        # result = self.__align_whisper_output(audio, result) # 단어 별 스탬프가 필요하면 사용

        segments = result["segments"]
        subtitles: list[Subtitle] = list(map(lambda x: Subtitle(x["start"], x["end"], x["text"]), segments))

        return SubtitleResult(subtitles)

    def __transcribe_with_original_whisper(self, audio_path: str):
        model_dir = f"/Users/octoping/Documents/audio"

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

    # 단어 별 스탬프가 필요하면 사용
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


subtitle_generator: SubtitleGenerator = WhisperXSubtitleGenerator()
