from pyperdeck import Hyperdeck
import streamlit as st
import telnetlib
from time import sleep

clips = []

@st.cache_resource
def Initialize(IPAdress):
    deck = Hyperdeck(IPAdress)
    st.markdown('CONNECTED')
    return deck

def Record(filename):
    deck.record(filename)

def Stop():
    deck.stop()

def Play(speed, loop, single):
    deck.play(speed, loop, single)

def PlayRangeTimeCode(in_timecode, out_timecode):
    deck.playrange_timecode(in_timecode, out_timecode)

def GoToTimecode(in_timecode):
    deck.go_to_timecode(in_timecode)

def GoToClip(id):
    deck.go_to_clip(id)

def ClearTimecode():
    deck.clear_playrange()

def ClearFrame():
    Frame = None


def MoveTimecode(frame):
    deck.go_within_timeline(frame)

@st.cache_data
def ClipsInfo(clips, IPAdress):
    st.session_state.info = True
    tn = telnetlib.Telnet(IPAdress, 9993)
    tn.write(b"clips get\n")
    sleep(2)
    tn.write(b"quit\n")

    log = tn.read_all().decode('ascii')
    clip_lines = log.split("\n")
    start_index = clip_lines.index([line for line in clip_lines if line.startswith("1:")][0])

        # "1:"から始まる行から最後の行までの範囲のクリップ情報を取得
    target_clips = clip_lines[start_index:]

        # 結果を出力
    for clip in target_clips:
        clip = f"{clip}  \n"
        clips.append(clip)
        st.markdown(clip)

####

if "connect" not in st.session_state:
    st.session_state.connect = False

if "timecode" not in st.session_state:
    st.session_state.timecode = False

if "clip" not in st.session_state:
    st.session_state.clip = False

if "max_frame" not in st.session_state:
    st.session_state.max_frame = False

if "plus" not in st.session_state:
    st.session_state.plus = False

if "minus" not in st.session_state:
    st.session_state.minus = False

if "info" not in st.session_state:
    st.session_state.info = False

st.title('HyperDeck UI')

with st.form('IP Form'):
    IPAdress = st.text_input('IPAdress', placeholder='192.')
    connect_button = st.form_submit_button(':red[CONNECT]')
    if connect_button or st.session_state.connect:
        try:
            deck = Initialize(IPAdress)
            st.session_state.connect = True
        except:
            st.error('Cannot connect to the HyperDeck')

col1, col2, col3 = st.columns(3)
with col1:
    filename = st.text_input('FileName', placeholder='optional')
    record_button = st.button('record')
with col2:
    st.markdown('<div style="padding: 43px;"></div>', unsafe_allow_html=True)
    stop_button = st.button('stop')
    if stop_button:
        Stop()


st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    timecode = st.checkbox('Select Timecode')
    if timecode:
        in_timecode = st.text_input('In Timecode', placeholder='00:00:00:00')
        out_timecode = st.text_input('Out Timecode', placeholder='00:00:30:00')
        minicol1, minicol2 = st.columns(2)
        with minicol1:
            timecode_button = st.button('Select')
        if timecode_button:
            try:
                PlayRangeTimeCode(in_timecode, out_timecode)
            except:
                try:
                    GoToTimecode(in_timecode)
                except:
                    st.error('Timecode is not correct')
            st.markdown('Timecode Applied')
        with minicol2:
            clear_timecode_button = st.button('clear')
        if clear_timecode_button:
            ClearTimecode()
            st.markdown('Timecode Cleared')
with col2:
    speed = st.number_input('Speed', -5000, 5000, 100)
    loop = st.checkbox('Loop')
    single = st.checkbox('Single Clip')
    play_button = st.button('play')

with col3:
    st.markdown('<div style="padding: 83px;"></div>', unsafe_allow_html=True)
    stop_button = st.button('stop', key=1)
    if stop_button:
        Stop()

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    clips_info = st.button('clips info')
    if clips_info or st.session_state.info:
        ClipsInfo(clips, IPAdress)

with col2:
    clip_btn = st.button('Go to a clip')
    if clip_btn or st.session_state.clip:
        st.session_state.clip = True
        id = st.number_input('clip_id', 1, 100, 1)
        GoToClip(id)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    btn = st.checkbox("Frame")
    if btn:
        #st.session_state.timecode = True
        # max_frame = st.text_input('Max Frame')
        # frame_btn = st.button('apply')
        st.session_state.max_frame = True
        frame = st.number_input('clip_id', min_value=0)

        MoveTimecode(frame)

if record_button:
    Record(filename)
if stop_button:
    Stop()
if play_button:
    Play(speed, loop, single)