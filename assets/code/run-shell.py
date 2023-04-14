@app.post("/shell/")
async def exec_shell(request: Request):
    """
    Triggers a shell command.
    Body needs to have a "command" key with 
    the command to be executed as value.
    """
    body = await request.json()
    if 'command' in body:
        command_list = body['command'].split()
        message = run_command(command_list)
        return {"message": message}
    else:
        return {"message": "No command sent."}