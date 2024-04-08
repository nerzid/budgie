import eventlet
import uuid
import schedule
# from managers import dialogue_managers, message_streamers, session_managers
from settings import SERVER_HOST, SERVER_PORT, SERVER_DEBUG_MODE, SECRET_KEY
from socialds.message import Message
from socialds.other.dst_pronouns import DSTPronoun

eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask_socketio import SocketIO
from datetime import datetime
from socialds.examples.doctors_visit_sp import sp_main
from socialds.enums import DSAction, DSActionByType

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

dialogue_managers = {}
session_managers = {}
message_streamers = {}

session_timeout = 3600


@app.route('/send-message', methods=['POST', 'OPTIONS'])
@cross_origin()
def send_message():
    message = request.json
    print(message)
    if "session_id" in message:
        dm = get_dm(message["session_id"])
    else:
        dm = get_dm()
    dm.last_time_dm_used_at = datetime.now()
    if message.get('ds_action') == DSAction.START_DIALOGUE.value:
        # print("SESSION ID")
        print(dm.dm_id)
        dm.get_menu_options()
        dm.message_streamer.add(Message(ds_action=DSAction.DIALOGUE_STARTED.value,
                                        ds_action_by='Dialogue Manager',
                                        ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                        message='Session is sent',
                                        session_id=dm.dm_id,
                                        sender_agent_id=str(dm.agents[0].agent_id),
                                        receiver_agent_id=str(dm.agents[1].agent_id)))
        dm.message_streamer.add(message=Message(ds_action=DSAction.SESSIONS_INFO.value, ds_action_by="Dialogue Manager",
                                                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                message=dm.session_manager.get_sessions_info_dict(dm.agents[0])))
        dm.message_streamer.add(message=Message(ds_action=DSAction.ACTIONS_INFO.value, ds_action_by="Dialogue Manager",
                                                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                message=dm.get_all_action_attrs()))
    elif message.get('ds_action') == DSAction.USER_CHOSE_MENU_OPTION.value:
        menu_option = message.get('message')
        sender_agent_id = message.get('sender_agent_id')
        receiver_agent_id = message.get('receiver_agent_id')
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_agent_by_id(receiver_agent_id)
        dm.choose_menu_option(sender_agent, menu_option, receiver_agent)
        dm.message_streamer.add(message=Message(ds_action=DSAction.SESSIONS_INFO.value, ds_action_by="Dialogue Manager",
                                                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                message=dm.session_manager.get_sessions_info_dict(sender_agent)))
    elif message.get('ds_action') == DSAction.USER_CHOSE_UTTERANCE.value:
        utterance_str = message.get('message')
        sender_agent_id = message.get('sender_agent_id')
        receiver_agent_id = message.get('receiver_agent_id')
        utterance = dm.get_utterance_from_string(utterance_str)
        # agent_name = message.get('ds_action_by')
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_agent_by_id(receiver_agent_id)
        dm.communicate(sender=sender_agent, receiver=receiver_agent, message=utterance)
        dm.message_streamer.add(message=Message(ds_action=DSAction.SESSIONS_INFO.value, ds_action_by="Dialogue Manager",
                                                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                message=dm.session_manager.get_sessions_info_dict(sender_agent)))
        dm.get_menu_options()
    elif message.get('ds_action') == DSAction.USER_CHOSE_ACTIONS.value:
        actions = message.get('message')
        sender_agent_id = message.get('sender_agent_id')
        receiver_agent_id = message.get('receiver_agent_id')
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_agent_by_id(receiver_agent_id)
        dm.communicate_with_actions(actions, sender_agent, receiver_agent)
        dm.message_streamer.add(message=Message(ds_action=DSAction.SESSIONS_INFO.value, ds_action_by="Dialogue Manager",
                                                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                message=dm.session_manager.get_sessions_info_dict(sender_agent)))
        # dm.get_menu_options()

    elif message.get('ds_action') == DSAction.REQUEST_UTTERANCE_BY_ACTION.value:
        action_attrs = message.get('message')
        sender_agent_id = message.get('sender_agent_id')
        receiver_agent_id = message.get('receiver_agent_id')
        sender_agent = dm.get_agent_by_id(sender_agent_id)
        receiver_agent = dm.get_agent_by_id(receiver_agent_id)
        sender_agent.pronouns[DSTPronoun.YOU] = receiver_agent
        receiver_agent.pronouns[DSTPronoun.YOU] = sender_agent
        dm.message_streamer.add(
            message=Message(ds_action=DSAction.SEND_UTTERANCE_BY_ACTION.value, ds_action_by="Dialogue Manager",
                            ds_action_by_type=DSActionByType.DIALOGUE_MANAGER.value,
                            message=dm.utterances_manager.get_utterance_by_action(
                                dm.get_actions_from_actions_attrs(action_attrs), sender_agent).text))
    else:
        return {"status": "no ds action present in the response"}
    return {"status": "Message received"}


def get_dm(session_id=None):
    if session_id in dialogue_managers:
        return dialogue_managers[session_id]
    else:
        session_id = str(uuid.uuid4())
        dm = sp_main(session_id)
        dm.run()
        dialogue_managers[session_id] = dm
        dm.message_streamer.on_message_added.subscribe(start_streaming_data, dm.message_streamer)
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
            print('streaming {}'.format(message.message_obj))
            socketio.emit('stream_message', message.message_obj)
            print('stream success')
    message_streamer.is_streaming = False


def start_streaming_data(message_streamer):
    if not message_streamer.is_streaming:
        message_streamer.is_streaming = True
        eventlet.spawn(stream_data, message_streamer)


if __name__ == '__main__':
    schedule.every(1).minutes.do(remove_timed_out_dm_sessions)
    socketio.run(app, debug=SERVER_DEBUG_MODE, host=SERVER_HOST, port=SERVER_PORT)
