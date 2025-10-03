!pip install azure-cognitiveservices-speech
import os, sys, textwrap
import azure.cognitiveservices.speech as speechsdk
from IPython.display import Audio, display

# ====== CONFIGURE THESE ======
AZURE_SPEECH_KEY = ""
AZURE_SPEECH_REGION = "centralindia"  # e.g., "centralindia", "eastus"
OUT_FILE = "news_mono.mp3"
os.environ["AZURE_SPEECH_KEY"] = ""
os.environ["AZURE_SPEECH_REGION"] = "centralindia"


# ====== Build the SSML for two speakers ======
# Voices: en-IN-NeerjaNeural (S1 host), en-IN-PrabhatNeural (S2 analyst).
# You can swap these for any available voices in your region.

SSML = textwrap.dedent("""\
<speak version="1.0"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts"
       xml:lang="en-IN">

  <!-- HOST (Female) -->
  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="chat" styledegree="0.8">
      <prosody rate="medium" pitch="+0%">
        Today on <emphasis level="moderate">Civic Lens</emphasis>, India’s democratic conversation takes center stage.
      </prosody>
    </mstts:express-as>
    <break time="500ms"/>
  </voice>

  <!-- ANALYST (Male) -->
  <voice name="en-IN-PrabhatNeural">
    <mstts:express-as style="assistant" styledegree="0.6">
      <prosody rate="medium" pitch="-2%">
        Congress leader Rahul Gandhi says India’s democracy is “under threat,” calling it a “wholesale attack” by the BJP-led central government during an interaction at EIA University in Colombia.
      </prosody>
    </mstts:express-as>
    <break time="350ms"/>
  </voice>

  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="calm" styledegree="0.7">
      <prosody rate="medium" pitch="+1%">
        The BJP hit back, calling him a <emphasis level="strong">Leader of Propaganda</emphasis>, criticizing him for “once again” denigrating Indian democracy on a foreign platform.
      </prosody>
    </mstts:express-as>
    <break time="550ms"/>
  </voice>

  <!-- SEGMENT 2 — RSS @ 100 -->
  <voice name="en-IN-PrabhatNeural">
    <mstts:express-as style="chat" styledegree="0.7">
      <prosody rate="medium" pitch="-1%">
        Meanwhile, the Rashtriya Swayamsevak Sangh — the RSS — is marking its centenary.
      </prosody>
    </mstts:express-as>
    <break time="300ms"/>
    <mstts:express-as style="assistant" styledegree="0.5">
      <prosody rate="medium" pitch="0%">
        Prime Minister Narendra Modi praised its contributions to nation-building and social service.
      </prosody>
    </mstts:express-as>
    <break time="550ms"/>
  </voice>

  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="calm" styledegree="0.8">
      <prosody rate="slow" pitch="-1%">
        But the celebrations come with controversy.
      </prosody>
    </mstts:express-as>
    <break time="300ms"/>
    <mstts:express-as style="chat" styledegree="0.7">
      <prosody rate="medium" pitch="+1%">
        Tamil Nadu Chief Minister M. K. Stalin criticized the government’s release of a commemorative stamp and coin for the centenary, calling it a “grave insult to our Constitution.”
      </prosody>
    </mstts:express-as>
    <break time="550ms"/>
  </voice>

  <voice name="en-IN-PrabhatNeural">
    <mstts:express-as style="assistant" styledegree="0.6">
      <prosody rate="medium" pitch="-2%">
        Critics allege the RSS promotes a <emphasis level="strong">divisive ideology</emphasis> and abstained from the freedom struggle.
      </prosody>
    </mstts:express-as>
    <break time="300ms"/>
    <mstts:express-as style="chat" styledegree="0.7">
      <prosody rate="medium" pitch="-1%">
        Kerala Chief Minister Pinarayi Vijayan went further, comparing it to <emphasis level="moderate">Zionists in Israel</emphasis>.
      </prosody>
    </mstts:express-as>
    <break time="700ms"/>
  </voice>

  <!-- SEGMENT 3 — What’s at stake -->
  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="chat" styledegree="0.8">
      <prosody rate="medium" pitch="+0%">
        As the country marks the RSS centenary, deeper questions surface.
      </prosody>
    </mstts:express-as>
    <break time="300ms"/>
    <mstts:express-as style="assistant" styledegree="0.6">
      <prosody rate="medium" pitch="-1%">
        What is the organization’s role in Indian democracy, and how has it shaped the country’s social fabric?
      </prosody>
    </mstts:express-as>
    <break time="550ms"/>
  </voice>

  <voice name="en-IN-PrabhatNeural">
    <mstts:express-as style="chat" styledegree="0.7">
      <prosody rate="medium" pitch="-1%">
        Supporters highlight grassroots discipline, volunteerism, and nation-building. Critics warn of majoritarianism, institutional capture, and erosion of pluralism.
      </prosody>
    </mstts:express-as>
    <break time="550ms"/>
  </voice>

  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="calm" styledegree="0.7">
      <prosody rate="medium" pitch="+1%">
        The debate often centers on process: institutional independence, space for dissent, tone of political discourse, and treatment of minorities and opposition.
      </prosody>
    </mstts:express-as>
    <break time="450ms"/>
  </voice>

  <voice name="en-IN-PrabhatNeural">
    <mstts:express-as style="assistant" styledegree="0.6">
      <prosody rate="medium" pitch="-2%">
        And on symbolism: which milestones receive state recognition — shaping public memory.
      </prosody>
    </mstts:express-as>
    <break time="700ms"/>
  </voice>

  <!-- CLOSING -->
  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="chat" styledegree="0.8">
      <prosody rate="medium" pitch="+0%">
        From university halls in Colombia to ceremonies at home, India’s democratic story is being argued in public — loudly.
      </prosody>
    </mstts:express-as>
    <break time="500ms"/>
  </voice>

  <voice name="en-IN-PrabhatNeural">
    <mstts:express-as style="assistant" styledegree="0.6">
      <prosody rate="medium" pitch="-1%">
        We’ll keep tracking the claims, the counterclaims, and what they signal for India’s institutions.
      </prosody>
    </mstts:express-as>
    <break time="400ms"/>
  </voice>

  <voice name="en-IN-NeerjaNeural">
    <mstts:express-as style="chat" styledegree="0.8">
      <prosody rate="medium" pitch="+1%">
        This is <emphasis level="moderate">Civic Lens</emphasis>. Thank you for listening.
      </prosody>
    </mstts:express-as>
    <break time="300ms"/>
    <mstts:express-as style="calm" styledegree="0.7">
      <prosody rate="medium" pitch="-1%">
        <emphasis level="reduced">Stay informed.</emphasis>
      </prosody>
    </mstts:express-as>
    <break time="700ms"/>
  </voice>

</speak>
""")

# ====== Synthesize to file ======
def synthesize_ssml_to_file(ssml: str, out_path: str):
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise RuntimeError("Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION.")

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    # Choose an output format (MP3 here). Other options: WAV in many sample rates/bit rates.
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
    )

    # Note: We're using multi-voice SSML, so do NOT set a single voice here;
    # the <voice> tags inside SSML control the speakers.

    audio_config = speechsdk.audio.AudioConfig(filename=out_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,
                                              audio_config=audio_config)

    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ Synth complete: {out_path}")
    else:
        print("❌ Synthesis failed:", result.reason)
        if result.error_details:
            print("Details:", result.error_details)
        raise RuntimeError("Synthesis failed.")

# Run synthesis
synthesize_ssml_to_file(SSML, OUT_FILE)

# Play in Colab
display(Audio(OUT_FILE))
