import azure.cognitiveservices.speech as sdk

def recognize_from_wav(wav_file: str, ref_text: str) -> sdk.SpeechRecognitionResult:
    # Create Speech and Push stream configs
    with open("azure_key.txt") as f:
        key = f.read()

    speech_config = sdk.SpeechConfig(subscription=key, region="eastus")
    speech_config.speech_recognition_language = "en-US"

    audio_config = sdk.audio.AudioConfig(filename=wav_file)
    recognizer = sdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Configure Pronunciation Assessment
    pron_config = sdk.PronunciationAssessmentConfig(
        reference_text=ref_text,
        grading_system=sdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=sdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=True,
    )
    # pron_config.phoneme_alphabet = "IPA"
    pron_config.enable_prosody_assessment()
    pron_config.apply_to(recognizer)

    result = recognizer.recognize_once()
    return result

def display_result(result: sdk.SpeechRecognitionResult) -> sdk.PronunciationAssessmentResult:
    pa_result = sdk.PronunciationAssessmentResult(result)

    print("\n=== PRONUNCIATION ASSESSMENT ===")
    print("Accuracy Score:      ", pa_result.accuracy_score)
    print("Completeness Score:  ", pa_result.completeness_score)
    print("Fluency Score:       ", pa_result.fluency_score)
    print("Pronunciation Score: ", pa_result.pronunciation_score)
    print("Prosody Score:       ", pa_result.prosody_score)

    print("\n=== WORD-LEVEL DETAILS ===")
    for word in pa_result.words:
        print(f"{word.word}: accuracy={word.accuracy_score}, error={word.error_type}")

        for phoneme in word.phonemes:
            print(f"  {phoneme.phoneme}: accuracy={phoneme.accuracy_score}")
    return pa_result