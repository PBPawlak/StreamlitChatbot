# # # # # # # from openai import OpenAI
# # # # # # # import streamlit as st
# # # # # # # import random
# # # # # # # import time
# # # # # # # import re

# # # # # # # # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# # # # # # # GAME_MASTER_PROMPT = """
# # # # # # # Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# # # # # # # Twoim zadaniem jest:
# # # # # # # - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# # # # # # # - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# # # # # # # - Przedstawić świat gry i rozpocząć przygodę.
# # # # # # # - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# # # # # # # - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# # # # # # # - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# # # # # # # - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# # # # # # # - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# # # # # # # Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# # # # # # # """


# # # # # # # client = OpenAI(
# # # # # # #     base_url=st.secrets["BASE_URL"],
# # # # # # #     api_key=st.secrets["API_KEY"],
# # # # # # # )

# # # # # # # st.write("Streamlit RPG Game Master 🤖 – wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # # # # # # # --- INICJALIZACJA HISTORII CZATU ---
# # # # # # # if "messages" not in st.session_state:
# # # # # # #     st.session_state.messages = [
# # # # # # #         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
# # # # # # #     ]
# # # # # # # if "awaiting_roll" not in st.session_state:
# # # # # # #     st.session_state.awaiting_roll = False
# # # # # # # if "last_roll_type" not in st.session_state:
# # # # # # #     st.session_state.last_roll_type = "d20"
# # # # # # # if "last_roll_prompt" not in st.session_state:
# # # # # # #     st.session_state.last_roll_prompt = ""

# # # # # # # # --- WYŚWIETLANIE HISTORII CZATU ---
# # # # # # # for message in st.session_state.messages:
# # # # # # #     with st.chat_message(message["role"]):
# # # # # # #         st.markdown(message["content"])

# # # # # # # # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# # # # # # # def get_messages():
# # # # # # #     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # # # # # # # --- WYSYŁANIE PROMPTU DO LLM ---
# # # # # # # def send_to_llm(prompt):
# # # # # # #     with st.chat_message("user"):
# # # # # # #         st.markdown(prompt)
# # # # # # #     with st.chat_message("assistant"):
# # # # # # #         message_placeholder = st.empty()
# # # # # # #         full_response = ""
# # # # # # #         try:
# # # # # # #             assistant_response = client.chat.completions.create(
# # # # # # #                 model=st.secrets["MODEL"],
# # # # # # #                 messages=get_messages()
# # # # # # #             )
# # # # # # #             content = None
# # # # # # #             if assistant_response and hasattr(assistant_response, "choices") and assistant_response.choices:
# # # # # # #                 choice = assistant_response.choices[0]
# # # # # # #                 if hasattr(choice, "message") and hasattr(choice.message, "content") and choice.message.content:
# # # # # # #                     content = choice.message.content
# # # # # # #                 elif hasattr(choice, "text") and choice.text:
# # # # # # #                     content = choice.text
# # # # # # #             if content:
# # # # # # #                 for chunk in content.split():
# # # # # # #                     full_response += chunk + " "
# # # # # # #                     time.sleep(0.02)
# # # # # # #                     message_placeholder.markdown(full_response + "▌")
# # # # # # #                 message_placeholder.markdown(full_response)
# # # # # # #             else:
# # # # # # #                 message_placeholder.markdown("⚠️ Przepraszam, nie udało się uzyskać odpowiedzi od Mistrza Gry.")
# # # # # # #                 full_response = "⚠️ Przepraszam, nie udało się uzyskać odpowiedzi od Mistrza Gry."
# # # # # # #         except Exception as e:
# # # # # # #             message_placeholder.markdown(f"⚠️ Wystąpił błąd: {e}")
# # # # # # #             full_response = f"⚠️ Wystąpił błąd: {e}"
# # # # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # # # #     return full_response

# # # # # # # # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# # # # # # # def detect_roll_type(response):
# # # # # # #     # Szuka fraz typu "rzuć kością d20", "rzuć d6", "rzuć k8" itd.
# # # # # # #     match = re.search(r"d(\d+)", response.lower())
# # # # # # #     if match:
# # # # # # #         return f"d{match.group(1)}"
# # # # # # #     return "d20"

# # # # # # # def get_dice_sides(roll_type):
# # # # # # #     # Zwraca liczbę ścianek na podstawie roll_type (np. d20 -> 20)
# # # # # # #     try:
# # # # # # #         return int(roll_type[1:])
# # # # # # #     except:
# # # # # # #         return 20

# # # # # # # # --- OBSŁUGA DECYZJI GRACZA ---
# # # # # # # if not st.session_state.awaiting_roll:
# # # # # # #     prompt = st.chat_input("Co robisz jako gracz?")
# # # # # # #     if prompt:
# # # # # # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # #         response = send_to_llm(prompt)
# # # # # # #         # Sprawdź, czy AI poprosiło o rzut kością
# # # # # # #         if "rzuć kością" in response.lower() or "czas na rzut" in response.lower():
# # # # # # #             st.session_state.awaiting_roll = True
# # # # # # #             roll_type = detect_roll_type(response)
# # # # # # #             st.session_state.last_roll_type = roll_type
# # # # # # #             st.session_state.last_roll_prompt = prompt

# # # # # # # # --- OBSŁUGA RZUTU KOŚCIĄ ---
# # # # # # # if st.session_state.awaiting_roll:
# # # # # # #     roll_type = st.session_state.last_roll_type
# # # # # # #     dice_sides = get_dice_sides(roll_type)
# # # # # # #     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
# # # # # # #     if st.button(f"🎲 Rzuć kością {roll_type}"):
# # # # # # #         roll = random.randint(1, dice_sides)
# # # # # # #         st.success(f"Wynik rzutu: {roll}")
# # # # # # #         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
# # # # # # #         st.session_state.messages.append({"role": "user", "content": roll_prompt})
# # # # # # #         send_to_llm(roll_prompt)
# # # # # # #         st.session_state.awaiting_roll = False
# # # # # # #         st.rerun()  # Odśwież interfejs

# # # # # # import streamlit as st
# # # # # # import random
# # # # # # import time
# # # # # # import re
# # # # # # from openai import OpenAI

# # # # # # # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# # # # # # GAME_MASTER_PROMPT = """
# # # # # # Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# # # # # # Twoim zadaniem jest:
# # # # # # - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# # # # # # - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# # # # # # - Przedstawić świat gry i rozpocząć przygodę.
# # # # # # - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# # # # # # - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# # # # # # - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# # # # # # - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# # # # # # - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# # # # # # Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# # # # # # """

# # # # # # # --- KONFIGURACJA KLIENTA CHUTES.AI ---
# # # # # # client = OpenAI(
# # # # # #     base_url="https://llm.chutes.ai/v1",
# # # # # #     api_key=st.secrets["CHUTES_API_TOKEN"],
# # # # # # )

# # # # # # st.write("Streamlit RPG Game Master 🤖 – wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # # # # # # --- INICJALIZACJA HISTORII CZATU ---
# # # # # # if "messages" not in st.session_state:
# # # # # #     st.session_state.messages = [
# # # # # #         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
# # # # # #     ]
# # # # # # if "awaiting_roll" not in st.session_state:
# # # # # #     st.session_state.awaiting_roll = False
# # # # # # if "last_roll_type" not in st.session_state:
# # # # # #     st.session_state.last_roll_type = "d20"
# # # # # # if "last_roll_prompt" not in st.session_state:
# # # # # #     st.session_state.last_roll_prompt = ""

# # # # # # # --- WYŚWIETLANIE HISTORII CZATU ---
# # # # # # for message in st.session_state.messages:
# # # # # #     with st.chat_message(message["role"]):
# # # # # #         st.markdown(message["content"])

# # # # # # # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# # # # # # def get_messages():
# # # # # #     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # # # # # # --- WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM ---
# # # # # # def send_to_llm(prompt):
# # # # # #     with st.chat_message("user"):
# # # # # #         st.markdown(prompt)
# # # # # #     with st.chat_message("assistant"):
# # # # # #         message_placeholder = st.empty()
# # # # # #         full_response = ""
# # # # # #         try:
# # # # # #             response_stream = client.chat.completions.create(
# # # # # #                 model="deepseek-ai/DeepSeek-V3-0324",
# # # # # #                 messages=get_messages(),
# # # # # #                 stream=True,
# # # # # #                 max_tokens=1024,
# # # # # #                 temperature=0.9
# # # # # #             )
# # # # # #             for chunk in response_stream:
# # # # # #                 # obsługa streamingu Chutes.ai (OpenAI compatible)
# # # # # #                 delta = None
# # # # # #                 if hasattr(chunk.choices[0], "delta"):
# # # # # #                     delta = chunk.choices[0].delta
# # # # # #                 elif hasattr(chunk.choices[0], "message"):
# # # # # #                     delta = chunk.choices[0].message
# # # # # #                 if delta and hasattr(delta, "content") and delta.content:
# # # # # #                     full_response += delta.content
# # # # # #                     message_placeholder.markdown(full_response + "▌")
# # # # # #             message_placeholder.markdown(full_response)
# # # # # #         except Exception as e:
# # # # # #             full_response = f"⚠️ Błąd API: {str(e)}"
# # # # # #             message_placeholder.markdown(full_response)
# # # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # # #     return full_response

# # # # # # # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# # # # # # def detect_roll_type(response):
# # # # # #     match = re.search(r"d(\d+)", response.lower())
# # # # # #     if match:
# # # # # #         return f"d{match.group(1)}"
# # # # # #     return "d20"

# # # # # # def get_dice_sides(roll_type):
# # # # # #     try:
# # # # # #         return int(roll_type[1:])
# # # # # #     except:
# # # # # #         return 20

# # # # # # # --- OBSŁUGA DECYZJI GRACZA ---
# # # # # # if not st.session_state.awaiting_roll:
# # # # # #     prompt = st.chat_input("Co robisz jako gracz?")
# # # # # #     if prompt:
# # # # # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # #         response = send_to_llm(prompt)
# # # # # #         # Sprawdź, czy AI poprosiło o rzut kością
# # # # # #         if "rzuć kością" in response.lower() or "czas na rzut" in response.lower():
# # # # # #             st.session_state.awaiting_roll = True
# # # # # #             roll_type = detect_roll_type(response)
# # # # # #             st.session_state.last_roll_type = roll_type
# # # # # #             st.session_state.last_roll_prompt = prompt

# # # # # # # --- OBSŁUGA RZUTU KOŚCIĄ ---
# # # # # # if st.session_state.awaiting_roll:
# # # # # #     roll_type = st.session_state.last_roll_type
# # # # # #     dice_sides = get_dice_sides(roll_type)
# # # # # #     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
# # # # # #     if st.button(f"🎲 Rzuć kością {roll_type}"):
# # # # # #         roll = random.randint(1, dice_sides)
# # # # # #         st.success(f"Wynik rzutu: {roll}")
# # # # # #         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
# # # # # #         st.session_state.messages.append({"role": "user", "content": roll_prompt})
# # # # # #         send_to_llm(roll_prompt)
# # # # # #         st.session_state.awaiting_roll = False
# # # # # #         st.rerun()  # Odśwież interfejs

# # # # # import streamlit as st
# # # # # import random
# # # # # import time
# # # # # import re
# # # # # from openai import OpenAI

# # # # # # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# # # # # GAME_MASTER_PROMPT = """
# # # # # Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# # # # # Twoim zadaniem jest:
# # # # # - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# # # # # - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# # # # # - Przedstawić świat gry i rozpocząć przygodę.
# # # # # - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# # # # # - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# # # # # - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# # # # # - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# # # # # - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# # # # # Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# # # # # """

# # # # # # --- KONFIGURACJA KLIENTA CHUTES.AI ---
# # # # # client = OpenAI(
# # # # #     base_url="https://llm.chutes.ai/v1",
# # # # #     api_key=st.secrets["CHUTES_API_TOKEN"],
# # # # # )

# # # # # st.write("Streamlit RPG Game Master 🤖 – wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # # # # # --- INICJALIZACJA HISTORII CZATU ---
# # # # # if "messages" not in st.session_state:
# # # # #     st.session_state.messages = [
# # # # #         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
# # # # #     ]
# # # # # if "awaiting_roll" not in st.session_state:
# # # # #     st.session_state.awaiting_roll = False
# # # # # if "last_roll_type" not in st.session_state:
# # # # #     st.session_state.last_roll_type = "d20"
# # # # # if "last_roll_prompt" not in st.session_state:
# # # # #     st.session_state.last_roll_prompt = ""

# # # # # # --- WYŚWIETLANIE HISTORII CZATU ---
# # # # # for message in st.session_state.messages:
# # # # #     with st.chat_message(message["role"]):
# # # # #         st.markdown(message["content"])

# # # # # # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# # # # # def get_messages():
# # # # #     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # # # # # --- WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM ---
# # # # # def send_to_llm(prompt):
# # # # #     with st.chat_message("user"):
# # # # #         st.markdown(prompt)
# # # # #     with st.chat_message("assistant"):
# # # # #         message_placeholder = st.empty()
# # # # #         full_response = ""
# # # # #         try:
# # # # #             response_stream = client.chat.completions.create(
# # # # #                 model="agentica-org/DeepCoder-14B-Preview",
# # # # #                 messages=get_messages(),
# # # # #                 stream=True,
# # # # #                 max_tokens=1024,
# # # # #                 temperature=0.7
# # # # #             )
# # # # #             for chunk in response_stream:
# # # # #                 # obsługa streamingu Chutes.ai (OpenAI compatible)
# # # # #                 delta = None
# # # # #                 if hasattr(chunk.choices[0], "delta"):
# # # # #                     delta = chunk.choices[0].delta
# # # # #                 elif hasattr(chunk.choices[0], "message"):
# # # # #                     delta = chunk.choices[0].message
# # # # #                 if delta and hasattr(delta, "content") and delta.content:
# # # # #                     full_response += delta.content
# # # # #                     message_placeholder.markdown(full_response + "▌")
# # # # #             message_placeholder.markdown(full_response)
# # # # #         except Exception as e:
# # # # #             full_response = f"⚠️ Błąd API: {str(e)}"
# # # # #             message_placeholder.markdown(full_response)
# # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # #     return full_response

# # # # # # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# # # # # def detect_roll_type(response):
# # # # #     # Szuka fraz typu "rzuć d12", "rzuć kością d20", "rzuć k8", itp.
# # # # #     match = re.search(r"d(\d+)", response.lower())
# # # # #     if match:
# # # # #         return f"d{match.group(1)}"
# # # # #     return "d20"

# # # # # def get_dice_sides(roll_type):
# # # # #     try:
# # # # #         return int(roll_type[1:])
# # # # #     except:
# # # # #         return 20

# # # # # # --- OBSŁUGA DECYZJI GRACZA ---
# # # # # if not st.session_state.awaiting_roll:
# # # # #     prompt = st.chat_input("Co robisz jako gracz?")
# # # # #     if prompt:
# # # # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # # # #         response = send_to_llm(prompt)
# # # # #         # Rozszerzone wykrywanie prośby o rzut kością
# # # # #         if (
# # # # #             "rzuć kością" in response.lower()
# # # # #             or "czas na rzut" in response.lower()
# # # # #             or re.search(r"rzuć.*d\d+", response.lower())
# # # # #             or re.search(r"rzuć.*kością.*d\d+", response.lower())
# # # # #         ):
# # # # #             st.session_state.awaiting_roll = True
# # # # #             roll_type = detect_roll_type(response)
# # # # #             st.session_state.last_roll_type = roll_type
# # # # #             st.session_state.last_roll_prompt = prompt

# # # # # # --- OBSŁUGA RZUTU KOŚCIĄ ---
# # # # # if st.session_state.awaiting_roll:
# # # # #     roll_type = st.session_state.last_roll_type
# # # # #     dice_sides = get_dice_sides(roll_type)
# # # # #     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
# # # # #     if st.button(f"🎲 Rzuć kością {roll_type}"):
# # # # #         roll = random.randint(1, dice_sides)
# # # # #         st.success(f"Wynik rzutu: {roll}")
# # # # #         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
# # # # #         st.session_state.messages.append({"role": "user", "content": roll_prompt})
# # # # #         send_to_llm(roll_prompt)
# # # # #         st.session_state.awaiting_roll = False
# # # # #         st.rerun()  # Odśwież interfejs

# # # # import streamlit as st
# # # # import random
# # # # import time
# # # # import re
# # # # from openai import OpenAI

# # # # # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# # # # GAME_MASTER_PROMPT = """
# # # # Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# # # # Twoim zadaniem jest:
# # # # - Odpowiadać po Polsku
# # # # - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# # # # - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# # # # - Przedstawić świat gry i rozpocząć przygodę.
# # # # - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# # # # - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# # # # - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# # # # - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# # # # - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# # # # Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# # # # """

# # # # # --- KONFIGURACJA KLIENTA CHUTES.AI ---
# # # # client = OpenAI(
# # # #     base_url="https://llm.chutes.ai/v1",
# # # #     api_key=st.secrets["CHUTES_API_TOKEN"],
# # # # )

# # # # st.write("Streamlit RPG Game Master 🤖 – wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # # # # --- INICJALIZACJA HISTORII CZATU ---
# # # # if "messages" not in st.session_state:
# # # #     st.session_state.messages = [
# # # #         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
# # # #     ]
# # # # if "awaiting_roll" not in st.session_state:
# # # #     st.session_state.awaiting_roll = False
# # # # if "last_roll_type" not in st.session_state:
# # # #     st.session_state.last_roll_type = "d20"
# # # # if "last_roll_prompt" not in st.session_state:
# # # #     st.session_state.last_roll_prompt = ""

# # # # # --- WYŚWIETLANIE HISTORII CZATU ---
# # # # for message in st.session_state.messages:
# # # #     with st.chat_message(message["role"]):
# # # #         st.markdown(message["content"])

# # # # # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# # # # def get_messages():
# # # #     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # # # # --- WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM ---
# # # # def send_to_llm(prompt):
# # # #     with st.chat_message("user"):
# # # #         st.markdown(prompt)
# # # #     with st.chat_message("assistant"):
# # # #         message_placeholder = st.empty()
# # # #         full_response = ""
# # # #         try:
# # # #             response_stream = client.chat.completions.create(
# # # #                 model="deepseek-ai/DeepSeek-V3-0324",
# # # #                 messages=get_messages(),
# # # #                 stream=True,
# # # #                 max_tokens=1024,
# # # #                 temperature=0.9
# # # #             )
# # # #             for chunk in response_stream:
# # # #                 delta = None
# # # #                 if hasattr(chunk.choices[0], "delta"):
# # # #                     delta = chunk.choices[0].delta
# # # #                 elif hasattr(chunk.choices[0], "message"):
# # # #                     delta = chunk.choices[0].message
# # # #                 if delta and hasattr(delta, "content") and delta.content:
# # # #                     full_response += delta.content
# # # #                     message_placeholder.markdown(full_response + "▌")
# # # #             message_placeholder.markdown(full_response)
# # # #         except Exception as e:
# # # #             full_response = f"⚠️ Błąd API: {str(e)}"
# # # #             message_placeholder.markdown(full_response)
# # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # #     return full_response

# # # # # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# # # # def detect_roll_type(response):
# # # #     # Obsługuje zarówno "d12", "k12", "d20", "k8" itd.
# # # #     match = re.search(r"[dk](\d+)", response.lower())
# # # #     if match:
# # # #         return f"d{match.group(1)}"
# # # #     return "d20"

# # # # def get_dice_sides(roll_type):
# # # #     try:
# # # #         return int(roll_type[1:])
# # # #     except:
# # # #         return 20

# # # # # --- OBSŁUGA DECYZJI GRACZA ---
# # # # if not st.session_state.awaiting_roll:
# # # #     prompt = st.chat_input("Co robisz jako gracz?")
# # # #     if prompt:
# # # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # # #         response = send_to_llm(prompt)
# # # #         # Rozszerzone wykrywanie prośby o rzut kością (d/k)
# # # #         if (
# # # #             "rzuć kością" in response.lower()
# # # #             or "czas na rzut" in response.lower()
# # # #             or re.search(r"rzuć.*[dk]\d+", response.lower())
# # # #             or re.search(r"rzuć.*kością.*[dk]\d+", response.lower())
# # # #         ):
# # # #             st.session_state.awaiting_roll = True
# # # #             roll_type = detect_roll_type(response)
# # # #             st.session_state.last_roll_type = roll_type
# # # #             st.session_state.last_roll_prompt = prompt

# # # # # --- OBSŁUGA RZUTU KOŚCIĄ ---
# # # # if st.session_state.awaiting_roll:
# # # #     roll_type = st.session_state.last_roll_type
# # # #     dice_sides = get_dice_sides(roll_type)
# # # #     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
# # # #     if st.button(f"🎲 Rzuć kością {roll_type}"):
# # # #         roll = random.randint(1, dice_sides)
# # # #         st.success(f"Wynik rzutu: {roll}")
# # # #         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
# # # #         st.session_state.messages.append({"role": "user", "content": roll_prompt})
# # # #         send_to_llm(roll_prompt)
# # # #         st.session_state.awaiting_roll = False
# # # #         st.rerun()  # Odśwież interfejs

# # # import streamlit as st
# # # import random
# # # import re
# # # from openai import OpenAI

# # # # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# # # GAME_MASTER_PROMPT = """
# # # Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# # # Twoim zadaniem jest:
# # # - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# # # - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# # # - Przedstawić świat gry i rozpocząć przygodę.
# # # - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# # # - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# # # - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# # # - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# # # - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# # # Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# # # """

# # # # --- KONFIGURACJA KLIENTA CHUTES.AI ---
# # # client = OpenAI(
# # #     base_url="https://llm.chutes.ai/v1",
# # #     api_key=st.secrets["CHUTES_API_TOKEN"],
# # # )

# # # st.title("Streamlit RPG Game Master 🤖")
# # # st.write("Wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # # # --- INICJALIZACJA HISTORII CZATU ---
# # # if "messages" not in st.session_state:
# # #     st.session_state.messages = [
# # #         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
# # #     ]
# # # if "awaiting_roll" not in st.session_state:
# # #     st.session_state.awaiting_roll = False
# # # if "last_roll_type" not in st.session_state:
# # #     st.session_state.last_roll_type = "d20"
# # # if "last_roll_prompt" not in st.session_state:
# # #     st.session_state.last_roll_prompt = ""

# # # # --- KSIĘGA POSTACI I POTWORÓW ---
# # # if "characters" not in st.session_state:
# # #     st.session_state.characters = []
# # # if "monsters" not in st.session_state:
# # #     st.session_state.monsters = []

# # # # --- WYŚWIETLANIE HISTORII CZATU ---
# # # with st.expander("🗨️ Historia czatu", expanded=True):
# # #     for message in st.session_state.messages:
# # #         with st.chat_message(message["role"]):
# # #             st.markdown(message["content"])

# # # # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# # # def get_messages():
# # #     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # # # --- WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM ---
# # # def send_to_llm(prompt):
# # #     with st.chat_message("user"):
# # #         st.markdown(prompt)
# # #     with st.chat_message("assistant"):
# # #         message_placeholder = st.empty()
# # #         full_response = ""
# # #         try:
# # #             response_stream = client.chat.completions.create(
# # #                 model="deepseek-ai/DeepSeek-V3-0324",
# # #                 messages=get_messages(),
# # #                 stream=True,
# # #                 max_tokens=1024,
# # #                 temperature=0.9
# # #             )
# # #             for chunk in response_stream:
# # #                 delta = None
# # #                 if hasattr(chunk.choices[0], "delta"):
# # #                     delta = chunk.choices[0].delta
# # #                 elif hasattr(chunk.choices[0], "message"):
# # #                     delta = chunk.choices[0].message
# # #                 if delta and hasattr(delta, "content") and delta.content:
# # #                     full_response += delta.content
# # #                     message_placeholder.markdown(full_response + "▌")
# # #             message_placeholder.markdown(full_response)
# # #         except Exception as e:
# # #             full_response = f"⚠️ Błąd API: {str(e)}"
# # #             message_placeholder.markdown(full_response)
# # #     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # #     return full_response

# # # # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# # # def detect_roll_type(response):
# # #     # Obsługuje zarówno "d12", "k12", "d20", "k8" itd.
# # #     match = re.search(r"[dk](\d+)", response.lower())
# # #     if match:
# # #         return f"d{match.group(1)}"
# # #     return "d20"

# # # def get_dice_sides(roll_type):
# # #     try:
# # #         return int(roll_type[1:])
# # #     except:
# # #         return 20

# # # # --- OBSŁUGA DECYZJI GRACZA ---
# # # if not st.session_state.awaiting_roll:
# # #     prompt = st.chat_input("Co robisz jako gracz?")
# # #     if prompt:
# # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # #         response = send_to_llm(prompt)
# # #         # Rozszerzone wykrywanie prośby o rzut kością (d/k)
# # #         if (
# # #             "rzuć kością" in response.lower()
# # #             or "czas na rzut" in response.lower()
# # #             or re.search(r"rzuć.*[dk]\d+", response.lower())
# # #             or re.search(r"rzuć.*kością.*[dk]\d+", response.lower())
# # #         ):
# # #             st.session_state.awaiting_roll = True
# # #             roll_type = detect_roll_type(response)
# # #             st.session_state.last_roll_type = roll_type
# # #             st.session_state.last_roll_prompt = prompt

# # # # --- OBSŁUGA RZUTU KOŚCIĄ ---
# # # if st.session_state.awaiting_roll:
# # #     roll_type = st.session_state.last_roll_type
# # #     dice_sides = get_dice_sides(roll_type)
# # #     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
# # #     if st.button(f"🎲 Rzuć kością {roll_type}"):
# # #         roll = random.randint(1, dice_sides)
# # #         st.success(f"Wynik rzutu: {roll}")
# # #         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
# # #         st.session_state.messages.append({"role": "user", "content": roll_prompt})
# # #         send_to_llm(roll_prompt)
# # #         st.session_state.awaiting_roll = False
# # #         st.rerun()  # Odśwież interfejs

# # # # --- KSIĘGA POSTACI I POTWORÓW ---
# # # st.header("📖 Księga Postaci i Potworów")
# # # tab1, tab2 = st.tabs(["Postacie", "Potwory"])

# # # # --- GENEROWANIE POSTACI ---
# # # with tab1:
# # #     st.subheader("Stwórz nową postać")
# # #     char_desc = st.text_input("Opis postaci (np. 'elfi łucznik z Rivendell, chaotyczny dobry')", key="char_desc")
# # #     if st.button("🎲 Wygeneruj postać", key="gen_char"):
# # #         char_prompt = f"""Wygeneruj statystyki postaci do gry fabularnej na podstawie poniższego opisu.
# # # Opis: {char_desc}
# # # Podaj wynik w formacie:
# # # Imię: ...
# # # Rasa: ...
# # # Klasa: ...
# # # Charakter: ...
# # # Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
# # # Umiejętności: [lista]
# # # Wyposażenie: [lista]
# # # Krótki opis fabularny: ...
# # # """
# # #         with st.spinner("Generowanie postaci..."):
# # #             response = client.chat.completions.create(
# # #                 model="agentica-org/DeepCoder-14B-Preview",
# # #                 messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
# # #                           {"role": "user", "content": char_prompt}],
# # #                 max_tokens=512,
# # #                 temperature=0.8,
# # #             )
# # #             content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
# # #             st.session_state.characters.append(content)
# # #             st.success("Dodano postać do księgi!")

# # #     st.markdown("---")
# # #     st.subheader("Twoje postacie")
# # #     for idx, char in enumerate(st.session_state.characters):
# # #         with st.expander(f"Postać #{idx+1}"):
# # #             st.markdown(char)

# # # # --- GENEROWANIE POTWORA ---
# # # with tab2:
# # #     st.subheader("Stwórz nowego potwora")
# # #     monster_type = st.text_input("Typ potwora lub krótki opis (np. 'smok ognisty', 'goblin szaman')", key="monster_type")
# # #     if st.button("🎲 Wygeneruj potwora", key="gen_monster"):
# # #         monster_prompt = f"""Wygeneruj statblock potwora do gry fabularnej na podstawie poniższego opisu.
# # # Opis: {monster_type}
# # # Podaj wynik w formacie:
# # # Nazwa: ...
# # # Typ: ...
# # # Rozmiar: ...
# # # Punkty życia: ...
# # # Klasa pancerza: ...
# # # Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
# # # Umiejętności/specjalne ataki: [lista]
# # # Krótki opis: ...
# # # """
# # #         with st.spinner("Generowanie potwora..."):
# # #             response = client.chat.completions.create(
# # #                 model="agentica-org/DeepCoder-14B-Preview",
# # #                 messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
# # #                           {"role": "user", "content": monster_prompt}],
# # #                 max_tokens=512,
# # #                 temperature=0.8,
# # #             )
# # #             content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
# # #             st.session_state.monsters.append(content)
# # #             st.success("Dodano potwora do księgi!")

# # #     st.markdown("---")
# # #     st.subheader("Twoje potwory")
# # #     for idx, monster in enumerate(st.session_state.monsters):
# # #         with st.expander(f"Potwór #{idx+1}"):
# # #             st.markdown(monster)
# # import streamlit as st
# # import random
# # import re
# # from openai import OpenAI

# # # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# # GAME_MASTER_PROMPT = """
# # Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# # Twoim zadaniem jest:
# # - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# # - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# # - Przedstawić świat gry i rozpocząć przygodę.
# # - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# # - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# # - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# # - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# # - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# # Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# # Wszystkie odpowiedzi udzielaj wyłącznie po polsku.
# # """

# # # --- KONFIGURACJA KLIENTA CHUTES.AI ---
# # client = OpenAI(
# #     base_url="https://llm.chutes.ai/v1",
# #     api_key=st.secrets["CHUTES_API_TOKEN"],
# # )

# # st.title("Streamlit RPG Game Master 🤖")
# # st.write("Wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # # --- INICJALIZACJA HISTORII CZATU ---
# # if "messages" not in st.session_state:
# #     st.session_state.messages = [
# #         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
# #     ]
# # if "awaiting_roll" not in st.session_state:
# #     st.session_state.awaiting_roll = False
# # if "last_roll_type" not in st.session_state:
# #     st.session_state.last_roll_type = "d20"
# # if "last_roll_prompt" not in st.session_state:
# #     st.session_state.last_roll_prompt = ""

# # # --- KSIĘGA POSTACI I POTWORÓW ---
# # if "characters" not in st.session_state:
# #     st.session_state.characters = []
# # if "monsters" not in st.session_state:
# #     st.session_state.monsters = []

# # # --- WYŚWIETLANIE HISTORII CZATU ---
# # with st.expander("🗨️ Historia czatu", expanded=True):
# #     for message in st.session_state.messages:
# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# # # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# # def get_messages():
# #     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # # --- WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM ---
# # def send_to_llm(prompt):
# #     with st.chat_message("user"):
# #         st.markdown(prompt)
# #     with st.chat_message("assistant"):
# #         message_placeholder = st.empty()
# #         full_response = ""
# #         try:
# #             response_stream = client.chat.completions.create(
# #                 model="deepseek-ai/DeepSeek-V3-0324",
# #                 messages=get_messages(),
# #                 stream=True,
# #                 max_tokens=1024,
# #                 temperature=0.9
# #             )
# #             for chunk in response_stream:
# #                 delta = None
# #                 if hasattr(chunk.choices[0], "delta"):
# #                     delta = chunk.choices[0].delta
# #                 elif hasattr(chunk.choices[0], "message"):
# #                     delta = chunk.choices[0].message
# #                 if delta and hasattr(delta, "content") and delta.content:
# #                     full_response += delta.content
# #                     message_placeholder.markdown(full_response + "▌")
# #             message_placeholder.markdown(full_response)
# #         except Exception as e:
# #             full_response = f"⚠️ Błąd API: {str(e)}"
# #             message_placeholder.markdown(full_response)
# #     st.session_state.messages.append({"role": "assistant", "content": full_response})
# #     return full_response

# # # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# # def detect_roll_type(response):
# #     # Obsługuje zarówno "d12", "k12", "d20", "k8" itd.
# #     match = re.search(r"[dk](\d+)", response.lower())
# #     if match:
# #         return f"d{match.group(1)}"
# #     return "d20"

# # def get_dice_sides(roll_type):
# #     try:
# #         return int(roll_type[1:])
# #     except:
# #         return 20

# # # --- OBSŁUGA DECYZJI GRACZA ---
# # if not st.session_state.awaiting_roll:
# #     prompt = st.chat_input("Co robisz jako gracz?")
# #     if prompt:
# #         st.session_state.messages.append({"role": "user", "content": prompt})
# #         response = send_to_llm(prompt)
# #         # Rozszerzone wykrywanie prośby o rzut kością (d/k)
# #         if (
# #             "rzuć kością" in response.lower()
# #             or "czas na rzut" in response.lower()
# #             or re.search(r"rzuć.*[dk]\d+", response.lower())
# #             or re.search(r"rzuć.*kością.*[dk]\d+", response.lower())
# #         ):
# #             st.session_state.awaiting_roll = True
# #             roll_type = detect_roll_type(response)
# #             st.session_state.last_roll_type = roll_type
# #             st.session_state.last_roll_prompt = prompt

# # # --- OBSŁUGA RZUTU KOŚCIĄ ---
# # if st.session_state.awaiting_roll:
# #     roll_type = st.session_state.last_roll_type
# #     dice_sides = get_dice_sides(roll_type)
# #     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
# #     if st.button(f"🎲 Rzuć kością {roll_type}"):
# #         roll = random.randint(1, dice_sides)
# #         st.success(f"Wynik rzutu: {roll}")
# #         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
# #         st.session_state.messages.append({"role": "user", "content": roll_prompt})
# #         send_to_llm(roll_prompt)
# #         st.session_state.awaiting_roll = False
# #         st.rerun()  # Odśwież interfejs

# # # --- KSIĘGA POSTACI I POTWORÓW ---
# # st.header("📖 Księga Postaci i Potworów")
# # tab1, tab2 = st.tabs(["Postacie", "Potwory"])

# # # --- GENEROWANIE POSTACI ---
# # with tab1:
# #     st.subheader("Stwórz nową postać")
# #     char_desc = st.text_input("Opis postaci (np. 'elfi łucznik z Rivendell, chaotyczny dobry')", key="char_desc")
# #     if st.button("🎲 Wygeneruj postać", key="gen_char"):
# #         char_prompt = f"""Wygeneruj statystyki postaci do gry fabularnej na podstawie poniższego opisu.
# # Opis: {char_desc}
# # Odpowiadaj wyłącznie po polsku.
# # Podaj wynik w formacie:
# # Imię: ...
# # Rasa: ...
# # Klasa: ...
# # Charakter: ...
# # Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
# # Umiejętności: [lista]
# # Wyposażenie: [lista]
# # Krótki opis fabularny: ...
# # """
# #         with st.spinner("Generowanie postaci..."):
# #             response = client.chat.completions.create(
# #                 model="deepseek-ai/DeepSeek-V3-0324",
# #                 messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
# #                           {"role": "user", "content": char_prompt}],
# #                 max_tokens=512,
# #                 temperature=0.9,
# #             )
# #             content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
# #             st.session_state.characters.append(content)
# #             st.success("Dodano postać do księgi!")

# #     st.markdown("---")
# #     st.subheader("Twoje postacie")
# #     for idx, char in enumerate(st.session_state.characters):
# #         with st.expander(f"Postać #{idx+1}"):
# #             st.markdown(char)

# # # --- GENEROWANIE POTWORA ---
# # with tab2:
# #     st.subheader("Stwórz nowego potwora")
# #     monster_type = st.text_input("Typ potwora lub krótki opis (np. 'smok ognisty', 'goblin szaman')", key="monster_type")
# #     if st.button("🎲 Wygeneruj potwora", key="gen_monster"):
# #         monster_prompt = f"""Wygeneruj statblock potwora do gry fabularnej na podstawie poniższego opisu.
# # Opis: {monster_type}
# # Odpowiadaj wyłącznie po polsku.
# # Podaj wynik w formacie:
# # Nazwa: ...
# # Typ: ...
# # Rozmiar: ...
# # Punkty życia: ...
# # Klasa pancerza: ...
# # Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
# # Umiejętności/specjalne ataki: [lista]
# # Krótki opis: ...
# # """
# #         with st.spinner("Generowanie potwora..."):
# #             response = client.chat.completions.create(
# #                 model="deepseek-ai/DeepSeek-V3-0324",
# #                 messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
# #                           {"role": "user", "content": monster_prompt}],
# #                 max_tokens=512,
# #                 temperature=0.9,
# #             )
# #             content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
# #             st.session_state.monsters.append(content)
# #             st.success("Dodano potwora do księgi!")

# #     st.markdown("---")
# #     st.subheader("Twoje potwory")
# #     for idx, monster in enumerate(st.session_state.monsters):
# #         with st.expander(f"Potwór #{idx+1}"):
# #             st.markdown(monster)
# import streamlit as st
# import random
# import re
# from openai import OpenAI

# # --- MISTRZ GRY RPG: SYSTEM PROMPT ---
# GAME_MASTER_PROMPT = """
# Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
# Twoim zadaniem jest:
# - Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
# - Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
# - Przedstawić świat gry i rozpocząć przygodę.
# - Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
# - Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
# - Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
# - Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
# - Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
# Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
# Wszystkie odpowiedzi udzielaj wyłącznie po polsku.
# """

# # --- KONFIGURACJA KLIENTA CHUTES.AI ---
# client = OpenAI(
#     base_url="https://llm.chutes.ai/v1",
#     api_key=st.secrets["CHUTES_API_TOKEN"],
# )

# st.title("Streamlit RPG Game Master 🤖")
# st.write("Wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# # --- INICJALIZACJA HISTORII CZATU ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Witaj podróżniku! Jestem Twoim Mistrzem Gry. Czy masz ulubiony system RPG, w którym chcesz zagrać, czy chcesz, żebym coś zaproponował?"}
#     ]
# if "awaiting_roll" not in st.session_state:
#     st.session_state.awaiting_roll = False
# if "last_roll_type" not in st.session_state:
#     st.session_state.last_roll_type = "d20"
# if "last_roll_prompt" not in st.session_state:
#     st.session_state.last_roll_prompt = ""
# if "characters" not in st.session_state:
#     st.session_state.characters = []
# if "monsters" not in st.session_state:
#     st.session_state.monsters = []

# # --- KSIĘGA POSTACI I POTWORÓW NA GÓRZE STRONY ---
# st.header("📖 Księga Postaci i Potworów")
# tab1, tab2 = st.tabs(["Postacie", "Potwory"])

# # --- GENEROWANIE POSTACI ---
# with tab1:
#     st.subheader("Stwórz nową postać")
#     char_desc = st.text_input("Opis postaci (np. 'elfi łucznik z Rivendell, chaotyczny dobry')", key="char_desc")
#     if st.button("🎲 Wygeneruj postać", key="gen_char"):
#         char_prompt = f"""Wygeneruj statystyki postaci do gry fabularnej na podstawie poniższego opisu.
# Opis: {char_desc}
# Odpowiadaj wyłącznie po polsku.
# Podaj wynik w formacie:
# Imię: ...
# Rasa: ...
# Klasa: ...
# Charakter: ...
# Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
# Umiejętności: [lista]
# Wyposażenie: [lista]
# Krótki opis fabularny: ...
# """
#         with st.spinner("Generowanie postaci..."):
#             response = client.chat.completions.create(
#                 model="deepseek-ai/DeepSeek-V3-0324",
#                 messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
#                           {"role": "user", "content": char_prompt}],
#                 max_tokens=512,
#                 temperature=0.9,
#             )
#             content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
#             st.session_state.characters.append(content)
#             st.success("Dodano postać do księgi!")

#     st.markdown("---")
#     st.subheader("Twoje postacie")
#     for idx, char in enumerate(st.session_state.characters):
#         with st.expander(f"Postać #{idx+1}"):
#             st.markdown(char)

# # --- GENEROWANIE POTWORA ---
# with tab2:
#     st.subheader("Stwórz nowego potwora")
#     monster_type = st.text_input("Typ potwora lub krótki opis (np. 'smok ognisty', 'goblin szaman')", key="monster_type")
#     if st.button("🎲 Wygeneruj potwora", key="gen_monster"):
#         monster_prompt = f"""Wygeneruj statblock potwora do gry fabularnej na podstawie poniższego opisu.
# Opis: {monster_type}
# Odpowiadaj wyłącznie po polsku.
# Podaj wynik w formacie:
# Nazwa: ...
# Typ: ...
# Rozmiar: ...
# Punkty życia: ...
# Klasa pancerza: ...
# Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
# Umiejętności/specjalne ataki: [lista]
# Krótki opis: ...
# """
#         with st.spinner("Generowanie potwora..."):
#             response = client.chat.completions.create(
#                 model="deepseek-ai/DeepSeek-V3-0324",
#                 messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
#                           {"role": "user", "content": monster_prompt}],
#                 max_tokens=512,
#                 temperature=0.9,
#             )
#             content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
#             st.session_state.monsters.append(content)
#             st.success("Dodano potwora do księgi!")

#     st.markdown("---")
#     st.subheader("Twoje potwory")
#     for idx, monster in enumerate(st.session_state.monsters):
#         with st.expander(f"Potwór #{idx+1}"):
#             st.markdown(monster)

# # --- WYŚWIETLANIE HISTORII CZATU ---
# with st.expander("🗨️ Historia czatu", expanded=True):
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

# # --- FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM ---
# def get_messages():
#     return [{"role": "system", "content": GAME_MASTER_PROMPT}] + st.session_state.messages

# # --- WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM ---
# def send_to_llm(prompt):
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         try:
#             response_stream = client.chat.completions.create(
#                 model="deepseek-ai/DeepSeek-V3-0324",
#                 messages=get_messages(),
#                 stream=True,
#                 max_tokens=1024,
#                 temperature=0.9
#             )
#             for chunk in response_stream:
#                 delta = None
#                 if hasattr(chunk.choices[0], "delta"):
#                     delta = chunk.choices[0].delta
#                 elif hasattr(chunk.choices[0], "message"):
#                     delta = chunk.choices[0].message
#                 if delta and hasattr(delta, "content") and delta.content:
#                     full_response += delta.content
#                     message_placeholder.markdown(full_response + "▌")
#             message_placeholder.markdown(full_response)
#         except Exception as e:
#             full_response = f"⚠️ Błąd API: {str(e)}"
#             message_placeholder.markdown(full_response)
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
#     return full_response

# # --- FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ ---
# def detect_roll_type(response):
#     # Obsługuje zarówno "d12", "k12", "d20", "k8" itd.
#     match = re.search(r"[dk](\d+)", response.lower())
#     if match:
#         return f"d{match.group(1)}"
#     return "d20"

# def get_dice_sides(roll_type):
#     try:
#         return int(roll_type[1:])
#     except:
#         return 20

# # --- OBSŁUGA DECYZJI GRACZA ---
# if not st.session_state.awaiting_roll:
#     prompt = st.chat_input("Co robisz jako gracz?")
#     if prompt:
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         response = send_to_llm(prompt)
#         # Rozszerzone wykrywanie prośby o rzut kością (d/k)
#         if (
#             "rzuć kością" in response.lower()
#             or "czas na rzut" in response.lower()
#             or re.search(r"rzuć.*[dk]\d+", response.lower())
#             or re.search(r"rzuć.*kością.*[dk]\d+", response.lower())
#         ):
#             st.session_state.awaiting_roll = True
#             roll_type = detect_roll_type(response)
#             st.session_state.last_roll_type = roll_type
#             st.session_state.last_roll_prompt = prompt

# # --- OBSŁUGA RZUTU KOŚCIĄ ---
# if st.session_state.awaiting_roll:
#     roll_type = st.session_state.last_roll_type
#     dice_sides = get_dice_sides(roll_type)
#     st.info(f"AI poprosiło o rzut kością! Kliknij, by rzucić {roll_type}.")
#     if st.button(f"🎲 Rzuć kością {roll_type}"):
#         roll = random.randint(1, dice_sides)
#         st.success(f"Wynik rzutu: {roll}")
#         roll_prompt = f"Wynik rzutu {roll_type}: {roll}"
#         st.session_state.messages.append({"role": "user", "content": roll_prompt})
#         send_to_llm(roll_prompt)
#         st.session_state.awaiting_roll = False
#         st.rerun()  # Odśwież interfejs

import streamlit as st
import random
import re
from openai import OpenAI

# --- MISTRZ GRY RPG: SYSTEM PROMPT ---
GAME_MASTER_PROMPT = """
Jesteś Mistrzem Gry prowadzącym sesję papierowego RPG dla jednego gracza.
Twoim zadaniem jest:
- Ustalić z graczem system RPG (np. D&D, Warhammer, autorski) lub zaproponować kilka do wyboru.
- Pomóc w stworzeniu postaci (cechy, klasa, ekwipunek, tło fabularne).
- Przedstawić świat gry i rozpocząć przygodę.
- Opisywać sceny, zadawać pytania o decyzje gracza, prowadzić narrację.
- Zarządzać mechaniką gry (np. rzuty kośćmi) – NIGDY NIE WYKONUJ rzutów kością samodzielnie. ZAWSZE poproś gracza o rzut (np. "Rzuć kością d20 i podaj wynik") i poczekaj na przesłanie wyniku. NIE opisuj rezultatu testu ani nie kontynuuj narracji, dopóki gracz nie poda wyniku rzutu.
- Tworzyć wyzwania, spotkania, dialogi z NPC i dynamicznie reagować na wybory gracza.
- Prowadzić walkę turową, podając wyniki rzutów i opisując efekty tylko na podstawie wyniku podanego przez gracza.
- Zachęcaj do kreatywności i prowadź spójną, wciągającą historię.
Odpowiadaj zawsze jako Mistrz Gry. Kończ wypowiedź pytaniem lub propozycją akcji, by gracz mógł podjąć decyzję.
Wszystkie odpowiedzi udzielaj wyłącznie po polsku.
"""

# KONFIGURACJA KLIENTA CHUTES.AI
client = OpenAI(
    base_url="https://llm.chutes.ai/v1",
    api_key=st.secrets["CHUTES_API_TOKEN"],
)

st.title("Mistrz gry 🤖")
st.write("Wybierasz akcję, rzucasz kością, a AI opisuje rezultat!")

# INICJALIZACJA HISTORII CZATU I KSIĘGI
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
if "characters" not in st.session_state:
    st.session_state.characters = []
if "monsters" not in st.session_state:
    st.session_state.monsters = []

# KSIĘGA POSTACI I POTWORÓW NA GÓRZE STRONY
st.markdown('<h2 style="font-size:18px;">📖 Księga Postaci i Potworów</h2>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Postacie", "Potwory"])

# GENEROWANIE POSTACI
with tab1:
    st.markdown('<h3 style="font-size:16px;">Stwórz nową postać</h3>', unsafe_allow_html=True)
    char_desc = st.text_input("Opis postaci (np. 'elfi łucznik z Rivendell, chaotyczny dobry')", key="char_desc")
    if st.button("🎲 Wygeneruj postać", key="gen_char"):
        char_prompt = f"""Wygeneruj statystyki postaci do gry fabularnej na podstawie poniższego opisu.
Opis: {char_desc}
Odpowiadaj wyłącznie po polsku.
Podaj wynik w formacie:
Imię: ...
Rasa: ...
Klasa: ...
Charakter: ...
Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
Umiejętności: [lista]
Wyposażenie: [lista]
Krótki opis fabularny: ...
"""
        with st.spinner("Generowanie postaci..."):
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324",
                messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
                          {"role": "user", "content": char_prompt}],
                max_tokens=512,
                temperature=0.9,
            )
            content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
            st.session_state.characters.append(content)
            st.success("Dodano postać do księgi!")

    st.markdown("---")
    st.subheader("Twoje postacie")
    for idx, char in enumerate(st.session_state.characters):
        with st.expander(f"Postać #{idx+1}"):
            st.markdown(char)

# GENEROWANIE POTWORA
with tab2:
    st.subheader("Stwórz nowego potwora")
    monster_type = st.text_input("Typ potwora lub krótki opis (np. 'smok ognisty', 'goblin szaman')", key="monster_type")
    if st.button("🎲 Wygeneruj potwora", key="gen_monster"):
        monster_prompt = f"""Wygeneruj statblock potwora do gry fabularnej na podstawie poniższego opisu.
Opis: {monster_type}
Odpowiadaj wyłącznie po polsku.
Podaj wynik w formacie:
Nazwa: ...
Typ: ...
Rozmiar: ...
Punkty życia: ...
Klasa pancerza: ...
Statystyki: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma
Umiejętności/specjalne ataki: [lista]
Krótki opis: ...
"""
        with st.spinner("Generowanie potwora..."):
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324",
                messages=[{"role": "system", "content": GAME_MASTER_PROMPT},
                          {"role": "user", "content": monster_prompt}],
                max_tokens=512,
                temperature=0.9,
            )
            content = response.choices[0].message.content if hasattr(response.choices[0], "message") else response.choices[0].text
            st.session_state.monsters.append(content)
            st.success("Dodano potwora do księgi!")

    st.markdown("---")
    st.subheader("Twoje potwory")
    for idx, monster in enumerate(st.session_state.monsters):
        with st.expander(f"Potwór #{idx+1}"):
            st.markdown(monster)

# FUNKCJA: PAMIĘĆ POSTACI I POTWORÓW
def get_game_memory():
    memory = ""
    if st.session_state.characters:
        memory += "Oto dotychczasowe postacie w grze:\n"
        for idx, char in enumerate(st.session_state.characters, 1):
            memory += f"{idx}. {char}\n"
    if st.session_state.monsters:
        memory += "Oto dotychczasowe potwory w grze:\n"
        for idx, monster in enumerate(st.session_state.monsters, 1):
            memory += f"{idx}. {monster}\n"
    return memory

# FUNKCJA DO BUDOWANIA WIADOMOŚCI Z SYSTEM PROMPTEM I PAMIĘCIĄ
def get_messages():
    memory = get_game_memory()
    memory_message = {"role": "system", "content": f"Zapamiętaj te postacie i potwory na potrzeby sesji:\n{memory}"}
    return [
        {"role": "system", "content": GAME_MASTER_PROMPT},
        memory_message
    ] + st.session_state.messages

# WYŚWIETLANIE HISTORII CZATU
with st.expander("🗨️ Historia czatu", expanded=True):
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# WYSYŁANIE PROMPTU DO LLM ZE STREAMINGIEM
def send_to_llm(prompt):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response_stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324",
                messages=get_messages(),
                stream=True,
                max_tokens=1024,
                temperature=0.9
            )
            for chunk in response_stream:
                delta = None
                if hasattr(chunk.choices[0], "delta"):
                    delta = chunk.choices[0].delta
                elif hasattr(chunk.choices[0], "message"):
                    delta = chunk.choices[0].message
                if delta and hasattr(delta, "content") and delta.content:
                    full_response += delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Błąd API: {str(e)}"
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return full_response

# FUNKCJA DO WYKRYWANIA RZUTU KOŚCIĄ
def detect_roll_type(response):
    # Obsługuje zarówno "d12", "k12", "d20", "k8" itd.
    match = re.search(r"[dk](\d+)", response.lower())
    if match:
        return f"d{match.group(1)}"
    return "d20"

def get_dice_sides(roll_type):
    try:
        return int(roll_type[1:])
    except:
        return 20

# OBSŁUGA DECYZJI GRACZA
if not st.session_state.awaiting_roll:
    prompt = st.chat_input("Co robisz jako gracz?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = send_to_llm(prompt)
        # Rozszerzone wykrywanie prośby o rzut kością (d/k)
        if (
            "rzuć kością" in response.lower()
            or "czas na rzut" in response.lower()
            or re.search(r"rzuć.*[dk]\d+", response.lower())
            or re.search(r"rzuć.*kością.*[dk]\d+", response.lower())
        ):
            st.session_state.awaiting_roll = True
            roll_type = detect_roll_type(response)
            st.session_state.last_roll_type = roll_type
            st.session_state.last_roll_prompt = prompt

# OBSŁUGA RZUTU KOŚCIĄ
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
        st.rerun()  # Odśwież interfejs
