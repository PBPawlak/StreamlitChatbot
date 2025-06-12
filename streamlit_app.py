# ver1 ---------------------------------------------------------------------------------------------------------------------------------------------------
# from openai import OpenAI
# import streamlit as st
# import time

# from pyexpat.errors import messages

# client = OpenAI(
#   base_url=st.secrets["BASE_URL"],
#   api_key=st.secrets["API_KEY"],
# )
# # response = client.responses.create(
# #     model="nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
# #     instructions="You are a coding assistant that talks like a pirate.",
# #     input="How do I check if a Python object is an instance of a class?",
# # )

# st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

# st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         assistant_response = client.chat.completions.create(model=st.secrets["MODEL"], messages=st.session_state.messages)
#                 # Simulate stream of response with milliseconds delay
#         for chunk in assistant_response.choices[0].message.content.split():
#             full_response += chunk + " "
#             time.sleep(0.05)
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": full_response})

# ver2 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# from openai import OpenAI
# import streamlit as st
# import time

# # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# GAME_MASTER_PROMPT = """
# Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# Twoim zadaniem jest:
# - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# - Przedstawić świat gry i rozpocząć przygodę.
# - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# - Zarządzać mechaniką gry (np. rzuty kośćmi – sam generuj wyniki, opisuj rezultaty).
# - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty.
# - Zachęcać do kreatywności i prowadzić spójną, wciągającą historię.
# Odpowiadaj zawsze jako Mistrz Gry. Zawsze kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# """

# client = OpenAI(
#   base_url=st.secrets["BASE_URL"],
#   api_key=st.secrets["API_KEY"],
# )

# st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

# st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")

# # --- INICJALIZACJA HISTORII CZATU ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
#     ]

# # --- WYŚWIETLANIE HISTORII CZATU ---
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# def get_messages():
#     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # --- OBSŁUGA WEJŚCIA UŻYTKOWNIKA ---
# if prompt := st.chat_input("Co robisz jako gracz?"):
#     # Dodaj wiadomość użytkownika do historii
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Wyświetl wiadomość użytkownika
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Wyświetl odpowiedź Mistrza Gry (LLM)
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         assistant_response = client.chat.completions.create(
#             model=st.secrets["MODEL"],
#             messages=get_messages()
#         )
#         # Symulacja "pisania" odpowiedzi
#         for chunk in assistant_response.choices[0].message.content.split():
#             full_response += chunk + " "
#             time.sleep(0.05)
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     # Dodaj odpowiedź asystenta do historii
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
# 
# ver3 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# from openai import OpenAI
# import streamlit as st
# import time

# # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# GAME_MASTER_PROMPT = """
# Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# Twoim zadaniem jest:
# - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# - Przedstawić świat gry i rozpocząć przygodę.
# - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# - Zarządzać mechaniką gry (np. rzuty kośćmi – sam generuj wyniki, opisuj rezultaty).
# - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty.
# - Zachęcać do kreatywności i prowadzić spójną, wciągającą historię.
# Odpowiadaj zawsze jako Mistrz Gry. Zawsze kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# """

# client = OpenAI(
#     base_url=st.secrets["BASE_URL"],
#     api_key=st.secrets["API_KEY"],
# )

# st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

# st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")

# # --- INICJALIZACJA HISTORII CZATU ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
#     ]

# # --- DODATKOWE ZMIENNE DO OBSŁUGI PONAWIANIA ---
# if "last_prompt" not in st.session_state:
#     st.session_state.last_prompt = None
# if "last_response_failed" not in st.session_state:
#     st.session_state.last_response_failed = False

# # --- WYŚWIETLANIE HISTORII CZATU ---
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# def get_messages():
#     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # --- PONÓW PRÓBĘ PRZYCISK ---
# def retry_last_prompt():
#     if st.session_state.last_prompt:
#         process_prompt(st.session_state.last_prompt, is_retry=True)

# # --- OBSŁUGA WEJŚCIA UŻYTKOWNIKA ---
# def process_prompt(prompt, is_retry=False):
#     st.session_state.last_prompt = prompt
#     st.session_state.last_response_failed = False
#     if not is_retry:
#         st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         try:
#             assistant_response = client.chat.completions.create(
#                 model=st.secrets["MODEL"],
#                 messages=get_messages()
#             )
#             content = None
#             if assistant_response and hasattr(assistant_response, "choices") and assistant_response.choices:
#                 choice = assistant_response.choices[0]
#                 if hasattr(choice, "message") and hasattr(choice.message, "content") and choice.message.content:
#                     content = choice.message.content
#                 elif hasattr(choice, "text") and choice.text:
#                     content = choice.text
#             if content:
#                 for chunk in content.split():
#                     full_response += chunk + " "
#                     time.sleep(0.05)
#                     message_placeholder.markdown(full_response + "▌")
#                 message_placeholder.markdown(full_response)
#             else:
#                 st.session_state.last_response_failed = True
#                 message_placeholder.markdown("⚠️ Przepraszam, nie udało się uzyskać odpowiedzi od Mistrza Gry. Spróbuj ponownie klikając przycisk poniżej.")
#                 full_response = "⚠️ Przepraszam, nie udało się uzyskać odpowiedzi od Mistrza Gry. Spróbuj ponownie klikając przycisk poniżej."
#         except Exception as e:
#             st.session_state.last_response_failed = True
#             message_placeholder.markdown(f"⚠️ Wystąpił błąd: {e}\nSpróbuj ponownie klikając przycisk poniżej.")
#             full_response = f"⚠️ Wystąpił błąd: {e}\nSpróbuj ponownie klikając przycisk poniżej."
#     st.session_state.messages.append({"role": "assistant", "content": full_response})

# # --- GŁÓWNA LOGIKA ---
# prompt = st.chat_input("Co robisz jako gracz?")
# if prompt:
#     process_prompt(prompt)

# # --- PRZYCISK PONÓW PRÓBĘ W PRZYPADKU NIEPOWODZENIA ---
# if st.session_state.last_response_failed:
#     st.button("🔄 Ponów próbę", on_click=retry_last_prompt)

# ver4 ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from openai import OpenAI
import streamlit as st
import time
import random

# --- SYSTEM PROMPT MISTRZA GRY ---
GAME_MASTER_PROMPT = """
Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
Twoim zadaniem jest:
- Opisywać świat, sytuacje i wyzwania.
- Pytać gracza o decyzje i czekać na jego wybór.
- Jeśli do rozstrzygnięcia akcji potrzebny jest rzut kością, napisz wyraźnie: "Czas na rzut kością! Kliknij przycisk, aby rzucić." i NIE opisuj jeszcze wyniku.
- Po rzucie kością opisz rezultat akcji, biorąc pod uwagę wynik rzutu (który otrzymasz jako kolejną wiadomość od gracza, np. "Wynik rzutu: 12").
- Nigdy nie rzucaj kością samodzielnie – zawsze czekaj na wynik od gracza.
- Zawsze kończ wypowiedź pytaniem lub propozycją akcji.
"""

client = OpenAI(
    base_url=st.secrets["BASE_URL"],
    api_key=st.secrets["API_KEY"],
)

st.write("Streamlit RPG Game Master 🤖 – najpierw wybierasz akcję, potem rzucasz kością, a AI opisuje rezultat!")

# --- INICJALIZACJA HISTORII CZATU ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Witaj podróżniku! Opowiedz, co chcesz zrobić jako pierwszy krok w przygodzie."}
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

# --- OBSŁUGA DECYZJI GRACZA ---
if not st.session_state.awaiting_roll:
    prompt = st.chat_input("Co robisz jako gracz?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = send_to_llm(prompt)
        # Sprawdź, czy AI poprosiło o rzut kością
        if "Czas na rzut kością" in response:
            st.session_state.awaiting_roll = True
            st.session_state.last_roll_type = "d20"
            st.session_state.last_roll_prompt = prompt

# --- OBSŁUGA RZUTU KOŚCIĄ ---
if st.session_state.awaiting_roll:
    st.info("AI poprosiło o rzut kością! Kliknij poniżej, by rzucić.")
    if st.button("🎲 Rzuć kością d20"):
        roll = random.randint(1, 20)
        st.success(f"Wynik rzutu: {roll}")
        roll_prompt = f"Wynik rzutu: {roll}"
        st.session_state.messages.append({"role": "user", "content": roll_prompt})
        send_to_llm(roll_prompt)
        st.session_state.awaiting_roll = False
        st.experimental_rerun()  # Kluczowe: natychmiast odśwież interfejs

