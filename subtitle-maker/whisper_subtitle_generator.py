from subtitle import SubtitleGenerator, SubtitleResult
import whisperx


class WhisperXSubtitleGenerator(SubtitleGenerator):
    __device = "cuda"
    __whisper_arch = "large-v2"
    __batch_size = 16  # reduce if low on GPU mem
    __compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

    def generate_subtitle(self, audio_path: str) -> SubtitleResult:
        model, audio, result = self.__transcribe_with_original_whisper(audio_path)

        result = self.__align_whisper_output(audio, result)

        # 3. Assign speaker labels
        diarize_model = whisperx.DiarizationPipeline(use_auth_token="YOUR_HF_TOKEN", device=self.__device)

        # add min/max number of speakers if known
        diarize_segments = diarize_model(audio)
        # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

        result = whisperx.assign_word_speakers(diarize_segments, result)
        print(diarize_segments)
        print(result["segments"])  # segments are now assigned speaker IDs

    def __transcribe_with_original_whisper(self, audio_path: str):
        model = whisperx.load_model(self.__whisper_arch, self.__device, compute_type=self.__compute_type)
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=self.__batch_size)

        print(result["segments"])  # before alignment
        return model, audio, result

    def __align_whisper_output(self, audio, result):
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.__device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, self.__device, return_char_alignments=False)

        print(result["segments"])  # after alignment
        return result

subtitle_generator: SubtitleGenerator = WhisperXSubtitleGenerator()