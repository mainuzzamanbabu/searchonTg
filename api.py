from flask import Flask, request, jsonify
from telethon import TelegramClient, errors
import asyncio

# Replace with your Telegram API credentials
api_id = '29365646'
api_hash = 'fb087115721f14a2c56ce22eb0b5f62a'
channel_id =2094043966
app = Flask(__name__)

@app.route('/search_channel', methods=['POST'])
async def search_channel():
    try:
        # Extract search text from request body
        search_text = request.json.get('search_text')
          # Optional, use default if not provided

        # Validate search text and channel ID (if provided)
        if not search_text:
            return jsonify({'status': 'error', 'message': 'Missing required field: search_text'})
        if channel_id and not isinstance(channel_id, int):
            return jsonify({'status': 'error', 'message': 'Invalid channel ID format'})

        # Create Telegram client asynchronously to avoid blocking the main thread
        async with TelegramClient('session_name', api_id, api_hash) as client:
            await client.start()

            try:
                found_messages = []
                async for message in client.iter_messages(channel_id or CHANNEL_ID, search=search_text):
                    found_messages.append(message.text)

                # Return success response with found messages
                return jsonify({'status': 'success', 'messages': found_messages})

            except errors.ChannelInvalidError:
                return jsonify({'status': 'error', 'message': 'Invalid channel ID'})
            except errors.PeerIdInvalidError:
                return jsonify({'status': 'error', 'message': 'Invalid search query'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Unexpected error: {str(e)}'})

    except asyncio.TimeoutError:
        return jsonify({'status': 'error', 'message': 'Connection timed out'})

# Define a default channel ID (optional, remove if using only user-provided channels)
CHANNEL_ID = 2094043966  # Replace with your default channel ID if applicable

if __name__ == '__main__':
    app.run(debug=True, port=5001)
