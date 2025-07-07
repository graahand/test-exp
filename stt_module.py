from RealtimeSTT import AudioToTextRecorder

class STTModule:
    def __init__(self, callback, device="cpu"):
        self.callback = callback
        self.device = device
        self.recorder = AudioToTextRecorder(
            model="tiny",
            language="en",
            post_speech_silence_duration=0.7,
            min_length_of_recording=1,
            min_gap_between_recordings=0.5,
            device=self.device,
            compute_type="float32",
            wake_words="jarvis",  # Optional: enable wake word if you want
        )
        self.active = True

    def run(self):
        print(f"[STT running on: {self.device}]")
        print('Say "Jarvis" to start recording.')
        while self.active:
            try:
                # This will block until a phrase is transcribed
                transcribed_text = self.recorder.text()
                if transcribed_text:
                    self.callback(transcribed_text)
            except KeyboardInterrupt:
                print("\nSTT interrupted by user.")
                self.active = False
                break
            except Exception as e:
                print(f"Error in STT: {e}")
                continue

    def stop(self):
        self.active = False