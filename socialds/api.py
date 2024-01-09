import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_cors import cross_origin, CORS
from flask_socketio import SocketIO, emit

from doctors_visit_sp import sp_main
from socialds.enums import DSAction
from socialds.managers.managers import message_streamer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
ds = sp_main()


@app.route('/send-message', methods=['POST', 'OPTIONS'])
@cross_origin()
def send_message():
    message = request.json
    print(message)
    if message.get('ds_action') == DSAction.START_DIALOGUE.value:
        print('DIALOGUE STARTS HERE!!!!!!!!!!!!')
        ds.get_menu_options()
    elif message.get('ds_action') == DSAction.USER_CHOSE_MENU_OPTION.value:
        menu_option = message.get('message')
        agent_name = message.get('ds_action_by')
        agent = ds.get_agent_by_name(agent_name)
        ds.choose_menu_option(agent, menu_option)
    elif message.get('ds_action') == DSAction.USER_CHOSE_UTTERANCE.value:
        utterance_str = message.get('message')
        utterance = ds.get_utterance_from_string(utterance_str)
        agent_name = message.get('ds_action_by')
        agent = ds.get_agent_by_name(agent_name)
        ds.choose_utterance(agent, utterance)
        ds.get_menu_options()
    else:
        return {"status": "no ds action present in the response"}
    return {"status": "Message received"}


def stream_data():
    for message in message_streamer.stream():
        print('streaming {}'.format(message))
        socketio.emit('stream_message', message)
        print('stream success')


def start_streaming_data():
    eventlet.spawn(stream_data)


if __name__ == '__main__':
    message_streamer.on_message_added.subscribe(start_streaming_data)
    ds.run()
    socketio.run(app, debug=True, port=[REDACTED_PORT])
    # asyncio.get_event_loop().run_forever()
