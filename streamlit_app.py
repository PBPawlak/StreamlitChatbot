from openai import OpenAI
import streamlit as st
import random
import time
import re

# --- MISTRZ GRY RPG: SYSTEM PROMPT ---
GAME_MASTER_PROMPT = """
Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
Twoim zadaniem jest:
- Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
- Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
- Przedstawić świat gry i rozpocząć przygodę.
- Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
- Zarządzać mechaniką gry (np. rzuty kośćmi) – ZAWSZE poproś gracza o wykonanie rzutu kością i poczekaj na wynik, który gracz wpisze lub prześle. NIE wykonuj rzutów samodzielnie.
- Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
- Prowadzić walkę turową, podając wyniki rzutów i opisując efekty.
- Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
"""

client = OpenAI(
    base_url=st.secrets["BASE_URL"],
    api_key=st.secrets["API_KEY"],
)

st.write("Streamlit RPG Game Master 🤖 – wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# --- INICJALIZACJA HISTORII CZATU ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
    ]
if "awaiting_roll" not in st.session_state:
    st.session_state.awaiting_roll = False
if "last_roll_type" not in st.session_state:
    st.session_state.last_roll_type = "d20"
if "last_roll_prompt" not in st.session_state:
    st.session_state.last_roll_prompt = ""

# --- WYŚWIETLANIE HISTORII CZATU ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
def get_messages():
    return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# --- WYSYŁANIE PROMPTU DO LLM ---
def send_to_llm(prompt):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            assistant_response = client.chat.completions.create(
                model=st.secrets["MODEL"],
                messages=get_messages()
            )
            content = None
            if assistant_response and hasattr(assistant_response, "choices") and assistant_response.choices:
                choice = assistant_response.choices[0]
                if hasattr(choice, "message") and hasattr(choice.message, "content") and choice.message.content:
                    content = choice.message.content
                elif hasattr(choice, "text") and choice.text:
                    content = choice.text
            if content:
                for chunk in content.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            else:
                message_placeholder.markdown("⚠️ Przepraszam, nie udało się uzyskać odpowiedzi od Mistrza Gry.")
                full_response = "⚠️ Przepraszam, nie udało się uzyskać odpowiedzi od Mistrza Gry."
        except Exception as e:
            message_placeholder.markdown(f"⚠️ Wystąpił błąd: {e}")
            full_response = f"⚠️ Wystąpił błąd: {e}"
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return full_response

# --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
def detect_roll_type(response):
    # Szuka fraz typu "rzuć kością d20", "rzuć d6", "rzuć k8" itd.
    match = re.search(r"d(\d+)", response.lower())
    if match:
        return f"d{match.group(1)}"
    return "d20"

def get_dice_sides(roll_type):
    # Zwraca liczbę ścianek na podstawie roll_type (np. d20 -> 20)
    try:
        return int(roll_type[1:])
    except:
        return 20

# --- OBSŁUGA DECYZJI GRACZA ---
if not st.session_state.awaiting_roll:
    prompt = st.chat_input("Co robisz jako gracz?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = send_to_llm(prompt)
        # Sprawdź, czy AI poprosiło o rzut kością
        if "rzuć kością" in response.lower() or "czas na rzut" in response.lower():
            st.session_state.awaiting_roll = True
            roll_type = detect_roll_type(response)
            st.session_state.last_roll_type = roll_type
            st.session_state.last_roll_prompt = prompt

# --- OBSŁUGA RZUTU KOŚCIĄ ---
if st.session_state.awaiting_roll:
    roll_type = st.session_state.last_roll_type
    dice_sides = get_dice_sides(roll_type)
    st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
    if st.button(f"🎲 Rzuć kością {roll_type}"):
        roll = random.randint(1, dice_sides)
        st.success(f"Wynik rzutu: {roll}")
        roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
        st.session_state.messages.append({"role": "user", "content": roll_prompt})
        send_to_llm(roll_prompt)
        st.session_state.awaiting_roll = False
        st.experimental_rerun()  # Odśwież interfejs

