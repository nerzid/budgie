import eventlet

eventlet.monkey_patch()
import uuid
import schedule

# from managers import dialogue_managers, message_streamers, session_managers
from settings import SERVER_HOST, SERVER_PORT, SERVER_DEBUG_MODE, SECRET_KEY
from socialds.managers.dialogue_manager import DialogueManager
from socialds.message import Message
from socialds.message_streamer import MessageStreamer
from socialds.other.dst_pronouns import DSTPronoun
from socialds.scenarios import doctors_visit


from flask import Flask, request, session, sessions
import json
from flask_cors import cross_origin, CORS
from flask_socketio import SocketIO
from datetime import datetime
from socialds.examples.doctors_visit_sp import custom_sp_main, sp_main
from socialds.enums import DSAction, DSActionByType

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

dialogue_managers = {}
session_managers = {}
message_streamers = {}

active_sessions = {}
scenario_functs = {}

session_timeout = 3600


@app.route("/send-message", methods=["POST", "OPTIONS"])
@cross_origin()
def send_message():
    message = request.get_json()
    print(message)
    if "session_id" in message:
        session_id = message["session_id"]
        if session_id in dialogue_managers:
            dm = dialogue_managers[session_id]

    ds_action = message.get("ds_action")
    if ds_action == DSAction.INIT.value:
        init_session()
    elif ds_action == DSAction.USER_CHOSE_SCENARIO.value:
        scenario_id = message.get("message").get("scenario_id")
        user_chose_scenario(session_id, scenario_id)
    elif ds_action == DSAction.USER_CHOSE_AGENT.value:
        agent_id = message.get("message").get("agent_id")
        dm = dialogue_managers[session_id]
        user_chose_agent(agent_id, dm)
    elif ds_action == DSAction.START_DIALOGUE.value:
        dm = dialogue_managers[session_id]
        start_dialogue(dm)
    # elif ds_action == DSAction.USER_CHOSE_MENU_OPTION.value:
    #     menu_option = message.get("message")
    #     sender_agent_id = message.get("sender_agent_id")
    #     receiver_agent_id = message.get("receiver_agent_id")
    #     sender_agent = dm.get_agent_by_id(sender_agent_id)
    #     receiver_agent = dm.get_agent_by_id(receiver_agent_id)
    #     dm.choose_menu_option(sender_agent, menu_option, receiver_agent)
    #     dm.message_streamer.add(
    #         message=Message(
    #             ds_action=DSAction.SESSIONS_INFO.value,
    #             ds_action_by="Dialogue Manager",
    #             ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
    #             message=dm.session_manager.get_sessions_info_dict(sender_agent),
    #         )
    #     )
    elif ds_action == DSAction.USER_SENT_UTTERANCE.value:
        user_text = message.get("message")
        sender_agent_id = message.get("ds_action_by")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        matched_utterance = dm.utterances_manager.get_utterance_by_string_match(
            user_text, sender_agent
        )
        dm.communicate(
            sender=sender_agent, receiver=receiver_agent, message=matched_utterance
        )
    elif ds_action == DSAction.USER_CHOSE_UTTERANCE.value:
        utterance_str = message.get("message")
        sender_agent_id = message.get("sender_agent_id")
        utterance = dm.get_utterance_from_string(utterance_str)
        # agent_name = message.get('ds_action_by')
        sender_agent_id = message.get("ds_action_by")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        dm.communicate(sender=sender_agent, receiver=receiver_agent, message=utterance)
        dm.message_streamer.add(
            message=Message(
                ds_action=DSAction.SESSIONS_INFO.value,
                ds_action_by="Dialogue Manager",
                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                message=dm.session_manager.get_sessions_info_dict(sender_agent),
            )
        )
        dm.get_menu_options()
    elif ds_action == DSAction.USER_CHOSE_ACTIONS.value:
        actions_attrs_str = message.get("message")
        actions_attrs = json.loads(actions_attrs_str)
        sender_agent_id = message.get("ds_action_by")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        dm.communicate_with_actions(
            dm.get_actions_from_actions_attrs(actions_attrs),
            sender_agent,
            receiver_agent,
        )
        dm.message_streamer.add(
            message=Message(
                ds_action=DSAction.SESSIONS_INFO.value,
                ds_action_by="Dialogue Manager",
                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                message=dm.session_manager.get_sessions_info_dict(),
            )
        )
        # dm.get_menu_options()
    elif ds_action == DSAction.REQUEST_UTTERANCE_BY_ACTION.value:
        action_attrs_str = message.get("message")
        action_attrs = json.loads(action_attrs_str)
        sender_agent_id = message.get("ds_action_by")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        actions = dm.get_actions_from_actions_attrs(action_attrs)
        matched_utt = dm.utterances_manager.get_utterance_by_action(
            actions, sender_agent
        )
        if matched_utt is not None:
            response_text = matched_utt.text
        else:
            response_text = "["
            for action in actions:
                response_text += str(action) + " "
            response_text = response_text[:-1]
            response_text += "]"
        dm.message_streamer.add(
            message=Message(
                ds_action=DSAction.SEND_UTTERANCE_BY_ACTION.value,
                ds_action_by="Dialogue Manager",
                ds_action_by_type=DSActionByType.DIALOGUE_MANAGER.value,
                message=response_text,
            )
        )
    elif ds_action == DSAction.REQUEST_UTTERANCE_BY_STRING_MATCH.value:
        dm = dialogue_managers[session_id]
        input_text = message.get("message")
        sender_agent_id = message.get("ds_action_by")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        # dm.utterances_manager.get_utterance_by_string_match(input_text, sender_agent)
        # dm.utterances_manager.get_utterance_by_relation_match(input_text, sender_agent)
        dm.message_streamer.add(
            message=Message(
                ds_action=DSAction.SEND_UTTERANCE_BY_STRING_MATCH.value,
                ds_action_by="Dialogue Manager",
                ds_action_by_type=DSActionByType.DIALOGUE_MANAGER.value,
                message=dm.utterances_manager.get_utterance_by_string_match(
                    input_text, sender_agent
                ).text,
            )
        )
    else:
        return {"status": "no ds action present in the response"}
    return {"status": "Message received"}


def add_scenario(scenario_func_dict_id, scenario_func_dict):
    scenario_functs[scenario_func_dict_id] = scenario_func_dict


def init_session():
    session_id = str(uuid.uuid4())
    ms = MessageStreamer()
    active_sessions[session_id] = {"id": session_id, "message_streamer": ms}

    scenarios_ids_w_name = {}
    for k, v in scenario_functs.items():
        print(k)
        print(v)
        scenarios_ids_w_name[k] = v["name"]

    ms.add(
        Message(
            ds_action=DSAction.REQUEST_USER_CHOOSE_SCENARIO.value,
            ds_action_by="Dialogue Manager",
            ds_action_by_type=DSActionByType.DIALOGUE_MANAGER.value,
            message=scenarios_ids_w_name,
            session_id=session_id,
        )
    )
    stream_data(ms)


def user_chose_scenario(session_id, scenario_id):
    scenario_funct = scenario_functs[scenario_id]["funct"]
    scenario = scenario_funct()
    ms = active_sessions[session_id]["message_streamer"]
    dialogue_managers[session_id] = DialogueManager(scenario, message_streamer=ms)

    agents_ids_w_name = {}
    for agent in scenario.agents:
        agents_ids_w_name[agent.id] = agent.name

    ms.add(
        Message(
            ds_action=DSAction.REQUEST_USER_CHOOSE_AGENT.value,
            ds_action_by="Dialogue Manager",
            ds_action_by_type=DSActionByType.DIALOGUE_MANAGER.value,
            message=agents_ids_w_name,
        )
    )
    stream_data(ms)


def user_chose_agent(agent_id, dm: DialogueManager):
    chosen_agent = dm.get_agent_by_id(agent_id)
    chosen_agent.auto = False
    for agent in dm.scenario.agents:
        if agent != chosen_agent:
            agent.auto = True
    dm.renew_callback_listeners()


def start_dialogue(dm):
    dm.run()
    dm.message_streamer.add(
        Message(
            ds_action=DSAction.DIALOGUE_STARTED.value,
            ds_action_by="Dialogue Manager",
            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
            message="Dialogue has started!",
        )
    )
    dm.message_streamer.add(
        message=Message(
            ds_action=DSAction.SESSIONS_INFO.value,
            ds_action_by="Dialogue Manager",
            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
            message=dm.session_manager.get_sessions_info_dict(),
        )
    )
    dm.message_streamer.add(
        message=Message(
            ds_action=DSAction.ACTIONS_INFO.value,
            ds_action_by="Dialogue Manager",
            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
            message=dm.get_all_action_attrs(),
        )
    )
    dm.message_streamer.add(
        message=Message(
            ds_action=DSAction.EFFECTS_INFO.value,
            ds_action_by="Dialogue Manager",
            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
            message=dm.get_all_effect_attrs(),
        )
    )


def create_dm(data):
    session_id = str(uuid.uuid4())
    dm = custom_sp_main(session_id, data)
    dm.run()
    dialogue_managers[session_id] = dm
    dm.message_streamer.on_message_added.subscribe(
        start_streaming_data, dm.message_streamer
    )
    message_streamers[session_id] = dm.message_streamer
    session_managers[session_id] = dm.session_manager
    return dm


def get_dm(session_id=None):
    if session_id in dialogue_managers:
        return dialogue_managers[session_id]
    else:
        session_id = str(uuid.uuid4())
        dm = sp_main(session_id)
        dm.run()
        dialogue_managers[session_id] = dm
        dm.message_streamer.on_message_added.subscribe(
            start_streaming_data, dm.message_streamer
        )
        message_streamers[session_id] = dm.message_streamer
        session_managers[session_id] = dm.session_manager
        return dm


def remove_timed_out_dm_sessions():
    for session_id, dm in dialogue_managers.items():
        if (datetime.now() - dm.last_time_dm_used_at).total_seconds() > session_timeout:
            del dialogue_managers[session_id]
            del session_managers[session_id]
            del message_streamers[session_id]


def stream_data(message_streamer):
    with app.app_context():
        while message := next(message_streamer.stream(), None):
            print("streaming {}".format(message.message_obj))
            socketio.emit("stream_message", message.message_obj)
            print("stream success")
    message_streamer.is_streaming = False


def start_streaming_data(message_streamer):
    if not message_streamer.is_streaming:
        message_streamer.is_streaming = True
        eventlet.spawn(stream_data, message_streamer)


def add_scenarios():
    doctors_visit_id = str(uuid.uuid4())
    add_scenario(
        doctors_visit_id,
        {
            "name": doctors_visit.SP_NAME,
            "id": doctors_visit_id,
            "funct": doctors_visit.sp_main,
        },
    )


if __name__ == "__main__":
    schedule.every(1).minutes.do(remove_timed_out_dm_sessions)
    add_scenarios()
    socketio.run(
        app,
        debug=SERVER_DEBUG_MODE,
        host=SERVER_HOST,
        port=SERVER_PORT,
        use_reloader=True,
        log_output=True,
    )
