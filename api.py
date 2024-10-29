import ast
import os
import eventlet
import requests

# socket=False allows for dns name calling in docker container over bridge network
eventlet.monkey_patch(socket=False)

import uuid
import schedule

# from managers import dialogue_managers, message_streamers, session_managers
from loaded_env_variables import SERVER_HOST, SERVER_PORT, SERVER_DEBUG_MODE, SECRET_KEY, LLM_HOST, LLM_PORT, SESSION_TIMEOUT
from socialds.managers.dialogue_manager import DialogueManager
from socialds.message import Message
from socialds.message_streamer import MessageStreamer
from socialds.other.dst_pronouns import DSTPronoun
from socialds.scenarios import doctors_visit
from socialds.scenarios import eye_dialogue2 as eye_dialogue
from socialds.scenarios import eye_dialogue3 as eye_dialogue3

from flask import Flask, request, session, sessions, jsonify
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


eye_dialogue_id = None

# temporary, will be deleted later
scenarios = {}


def setup_llm(session_id):
    response = requests.post(url=LLM_HOST + ":" + str(LLM_PORT) + "/setup_vector_stores",
                             data=json.dumps({"session_id": session_id,
                                              "sp_data": get_sp_data(session_id)}),
                             headers={"Content-Type": "application/json"})
    return response


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
    if ds_action == DSAction.INIT_EYE_DIALOGUE.value:
        session_id = init_session()
        # scenario = user_chose_scenario(session_id, eye_dialogue_id)

        ms = active_sessions[session_id]["message_streamer"]

        # scenario = eye_dialogue3.sp_main(message['message'])
        scenario = eye_dialogue3.sp_main()
        dialogue_managers[session_id] = DialogueManager(scenario, message_streamer=ms)

        agents_ids_w_name = {}
        for agent in scenario.agents:
            agents_ids_w_name[agent.id] = agent.name

        dm = dialogue_managers[session_id]
        sender_agent_id = 0
        receiver_agent_id = 0
        for agent in scenario.agents:
            if agent.name == 'doctor':
                sender_agent_id = agent.id
            else:
                receiver_agent_id = agent.id
        user_chose_agent(sender_agent_id, dm)
        response = setup_llm(session_id)
        if response.json()["status"] == "success":
            print("LLM has been set up for session:{} successfully".format(session_id))

        return {
            'ds_action': DSAction.INIT_EYE_DIALOGUE.value,
            'ds_action_by': "Dialogue Manager",
            'ds_action_by_type': DSActionByType.DIALOGUE_MANAGER.value,
            # 'message': {
            #     'sender_agent_id': sender_agent_id,
            #     'receiver_agent_id': receiver_agent_id,
            # },
            'sender_agent_id': sender_agent_id,
            'receiver_agent_id': receiver_agent_id,
            'session_id': session_id,
        }
    elif ds_action == DSAction.USER_SENT_UTTERANCE_EYE_DIALOGUE.value:
        user_text = message.get("message")
        sender_agent_id = message.get("sender_agent_id")
        receiver_agent_id = message.get("receiver_agent_id")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent

        # matched_utterance = dm.utterances_manager.get_utterance_from_llm(user_text, sender_agent)
        # print('LLM matched to the utterance: ' + str(matched_utterance))
        possible_actions_lists_response = requests.post(url=LLM_HOST + ":" + str(LLM_PORT) + "/extract_actions",
                                               data=json.dumps({"session_id": session_id,
                                                                "utterance": user_text}),
                                               headers={"Content-Type": "application/json"}
                                               )
        possible_actions_lists = json.loads(possible_actions_lists_response.json()["possible_actions_lists"])

        matched_utterances = requests.post(url=LLM_HOST + ":" + str(LLM_PORT) + "/get_matching_utterances",
                                           data=json.dumps({"session_id": session_id,
                                                            "possible_actions_lists": possible_actions_lists,
                                                            "utterance": user_text}),
                                           headers={"Content-Type": "application/json"}
                                           ).json()["utterances"]
        if len(matched_utterances) == 0:
            response = 'Could you please rephrase your request or provide a new sentence?'
        else:
            matched_utterance_obj = matched_utterances[0]
            matched_utterance_dict = ast.literal_eval(matched_utterance_obj)
            matched_utterance = None
            for utterance in dm.scenario.utterances:
                if utterance.id == matched_utterance_dict["id"]:
                    matched_utterance = utterance
                    break
            if matched_utterance is None:
                raise Exception('Could not find a matching utterance')

            # dm.communicate(sender=sender_agent, receiver=receiver_agent, message=matched_utterance)
            response = dm.communicate_sync(sender=sender_agent, receiver=receiver_agent, message=matched_utterance)

        # for message in dm.message_streamer.messages.queue:
        #     if message.ds_action == DSAction.DISPLAY_UTTERANCE.value:
        #         dm.message_streamer.messages.queue.clear()
        return {'message': response}
        # dm.communicate(
        #     sender=sender_agent, receiver=receiver_agent, message=matched_utterance
        # )
    elif ds_action == DSAction.INIT.value:
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
        # matched_utterance = dm.utterances_manager.get_utterance_from_llm(user_text, sender_agent)['message']['content']
        # dm.message_streamer.add(
        #     message=Message(
        #         ds_action=DSAction.DISPLAY_UTTERANCE.value,
        #         ds_action_by="Dialogue Manager",
        #         ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
        #         message=matched_utterance
        #     )
        # )
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
        input_text = message.get("message").replace('"', "")
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
    elif ds_action == DSAction.REQUEST_UTTERANCE_BY_LLM.value:
        dm = dialogue_managers[session_id]
        input_text = message.get("message").replace('"', "")
        sender_agent_id = message.get("ds_action_by")
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_other_agent(sender_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        message = dm.utterances_manager.get_utterance_from_llm(input_text, sender_agent).text
        dm.message_streamer.add(
            message=Message(
                ds_action=DSAction.SEND_UTTERANCE_BY_STRING_MATCH.value,
                ds_action_by="Dialogue Manager",
                ds_action_by_type=DSActionByType.DIALOGUE_MANAGER.value,
                message=message,
            )
        )
    else:
        return {"status": "no ds action present in the response"}
    return {"status": "Message received"}


@app.route("/get-sp", methods=["POST", "OPTIONS"])
@cross_origin()
def get_sp():
    message = request.get_json()
    sp_name = message.get("sp_name")
    if sp_name is None or sp_name == "doctors visit":
        sp = doctors_visit.sp_main()
    elif sp_name == "eye dialogue":
        import socialds.scenarios.eye_dialogue3 as scenario
        sp = scenario.sp_main()
        # sp = eye_dialogue.sp_main()
    scenarios[sp.id] = sp
    action_schemes = []

    res_dict = sp.to_dict()
    for action in sp.actions:
        action_name = action.__name__
        action_doc = action.__init__.__doc__
        if action_doc is None:
            continue
        pieces = action_doc.split("\n")
        desc = pieces[1].strip()
        action_args = {}
        for _ in pieces[3:-1]:
            _ = _.strip()
            if _ == "":
                continue
            arg_name, arg_desc = _.split(":")
            action_args[arg_name.strip()] = arg_desc.strip()
        action_dict = {
            "action_name": action_name,
            "desc": desc,
            "action_args": action_args,
        }
        action_schemes.append(action_dict)
    res_dict["action_schemas"] = action_schemes

    # result = json.dumps(res_dict)
    return jsonify(res_dict)


def get_sp_data(session_id):
    scenario = dialogue_managers[session_id].scenario
    action_schemes = []

    res_dict = scenario.to_dict()
    for action in scenario.actions:
        action_name = action.__name__
        action_doc = action.__init__.__doc__
        if action_doc is None:
            continue
        pieces = action_doc.split("\n")
        desc = pieces[1].strip()
        action_args = {}
        for _ in pieces[3:-1]:
            _ = _.strip()
            if _ == "":
                continue
            arg_name, arg_desc = _.split(":")
            action_args[arg_name.strip()] = arg_desc.strip()
        action_dict = {
            "action_name": action_name,
            "desc": desc,
            "action_args": action_args,
        }
        action_schemes.append(action_dict)
    res_dict["action_schemas"] = action_schemes

    # result = json.dumps(res_dict)
    return res_dict

@app.route("/get_dict", methods=["POST", "OPTIONS"])
@cross_origin()
def get_object_dict():
    message = request.get_json()
    scenario_id = message.get("id")
    scenario = scenarios[scenario_id]


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
    return session_id


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
    return scenario


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
        if (datetime.now() - dm.last_time_dm_used_at).total_seconds() > SESSION_TIMEOUT:
            del dialogue_managers[session_id]
            del session_managers[session_id]
            del message_streamers[session_id]


def stream_data(message_streamer):
    return
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

    global eye_dialogue_id
    eye_dialogue_id = str(uuid.uuid4())
    add_scenario(
        eye_dialogue_id,
        {
            "name": eye_dialogue.SP_NAME,
            "id": eye_dialogue_id,
            "funct": eye_dialogue.sp_main,
        },
    )


if __name__ == "__main__":
    schedule.every(1).minutes.do(remove_timed_out_dm_sessions)
    add_scenarios()
    ssl_context = ('[REDACTED_PATH]', '[REDACTED_PATH]')
    socketio.run(
        app,
        debug=SERVER_DEBUG_MODE,
        host=SERVER_HOST,
        port=SERVER_PORT,
        use_reloader=True,
        log_output=True,
        certfile='[REDACTED_PATH]',
        keyfile='[REDACTED_PATH]'
    )
