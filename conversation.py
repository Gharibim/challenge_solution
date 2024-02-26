from pydantic_models import AddAfterModel
import time
import uuid

def take_action(messages, action):
    if action.add:
        new_message = {
            "id": uuid.uuid4(),  
            "timestamp": time.time(),  
            "role": "assistant",  
            "content": action.add.content,
            "tool_calls": [],
            "tool_call_id": None,
            "name": None
        }
        target_id = action.add.after_message_id if isinstance(action.add, AddAfterModel) else action.add.before_message_id
        for index, message in enumerate(messages):
            if message['id'] == target_id:
                if isinstance(action.add, AddAfterModel):
                    messages.insert(index + 1, new_message)
                else:
                    messages.insert(index, new_message)
                break
    if action.delete:
        messages = [message for message in messages if message["id"] not in action.delete]
    if action.modify:
        for modification in action.modify:
            for message in messages:
                if message["id"] == modification.message_id:
                    message["content"] = modification.content
                    break
    return messages
