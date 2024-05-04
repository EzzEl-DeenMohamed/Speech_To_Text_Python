import speech_recognition as sr
import re


def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please start speaking...")

        # Listen for speech with a timeout to wait for user to finish speaking
        try:
            audio = r.listen(source, phrase_time_limit=20, timeout=20)  # Adjust timeout as needed
            print("You have finished speaking.")

            # Attempt to recognize the speech
            try:
                outputText = r.recognize_google(audio)
                print("You have said:\n" + outputText)

                # Define the regular expression pattern
                pattern = re.compile(r'create(?:\s+a)?(?:\s+new)?\s+(\w+)', re.IGNORECASE)

                # Find all occurrences of the words after "create" in the string
                matches = re.findall(pattern, outputText)

                if matches:
                    # Extract the first match, which has the highest priority
                    word_after_create = matches[0]
                    print("Word after 'create':", word_after_create)
                else:
                    print("No word found after 'create'")

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

        except sr.WaitTimeoutError:
            print("Timeout reached. No speech detected.")
        except Exception as e:
            print("Error: " + str(e))


if __name__ == "__main__":
    main()
