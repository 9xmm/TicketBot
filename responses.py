def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'help':
        return 'I currently have no commands that you have access to!'

    else:
        return
